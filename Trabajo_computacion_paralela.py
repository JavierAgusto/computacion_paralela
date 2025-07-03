import dask
import dask.dataframe as dd
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import time

# Configuración para Dask
dask.config.set(scheduler='threads', num_workers=2)

# ============ Funciones ============

def imprimir_tiempo(mensaje, inicio):
    print(f"\n{mensaje}: {time.time() - inicio:.2f} segundos")

def mediana_ponderada(grupo):
    grupo = grupo.sort_values("EDAD")
    grupo["ACUM"] = grupo["CANTIDAD"].cumsum()
    total = grupo["CANTIDAD"].sum()
    return grupo.loc[grupo["ACUM"] >= total / 2, "EDAD"].iloc[0]

def proporcion_por_rango_etario(df):
    def categorizar_edad(edad):
        if edad < 18:
            return "Menor de 18"
        elif edad <= 35:
            return "18-35"
        elif edad <= 60:
            return "36-60"
        else:
            return "60+"

    df["RANGO_ETARIO"] = df["EDAD"].apply(categorizar_edad)
    totales = df.groupby(["ESPECIE", "GENERO"])["CANTIDAD"].sum().rename("TOTAL")
    rangos = df.groupby(["ESPECIE", "GENERO", "RANGO_ETARIO"])["CANTIDAD"].sum().rename("CUENTA")
    
    resultado = pd.merge(rangos.reset_index(), totales.reset_index(), on=["ESPECIE", "GENERO"])
    resultado["%"] = (resultado["CUENTA"] / resultado["TOTAL"] * 100).round(2)

    print("\nProporción por rango etario (%):")
    for (especie, genero), grupo in resultado.groupby(["ESPECIE", "GENERO"]):
        print(f"\n{especie} - {genero}")
        for _, fila in grupo.iterrows():
            print(f"  {fila['RANGO_ETARIO']}: {fila['%']}%")

def graficar_piramides(df):
    df = df.copy()
    df["EDAD"] = df["EDAD"].astype(int)
    especies = df["ESPECIE"].unique()

    for especie in especies:
        datos = df[df["ESPECIE"] == especie]
        edades = sorted(datos["EDAD"].unique())

        hombres = datos[datos["GENERO"] == "MACHO"].groupby("EDAD")["CANTIDAD"].sum()
        mujeres = datos[datos["GENERO"] == "HEMBRA"].groupby("EDAD")["CANTIDAD"].sum()

        valores_h = [-hombres.get(e, 0) for e in edades]
        valores_m = [mujeres.get(e, 0) for e in edades]

        plt.figure(figsize=(10, 6))
        plt.barh(edades, valores_h, label="Masculino", color="blue")
        plt.barh(edades, valores_m, label="Femenino", color="pink")
        plt.xlabel("Población")
        plt.ylabel("Edad")
        plt.title(f"PIRÁMIDE DE EDAD - {especie}")
        plt.legend()
        plt.tight_layout()
        plt.show()

def calcular_indice_dependencia_total(df):
    menores_15 = df[df["EDAD"] < 15]["CANTIDAD"].sum()
    mayores_64 = df[df["EDAD"] > 64]["CANTIDAD"].sum()
    edad_trabajo = df[(df["EDAD"] >= 15) & (df["EDAD"] <= 64)]["CANTIDAD"].sum()

    if edad_trabajo == 0:
        print("\nNo hay población en edad de trabajar.")
        return

    indice = ((menores_15 + mayores_64) / edad_trabajo) * 100
    print(f"\nÍndice de Dependencia (total): {indice:.2f}%")

def top_10000_pueblos_con_mas_viajes():
    print("\nProcesando los 10.000 pueblos con más viajes...")

    viajes = dd.read_csv(
        "eldoria.csv",
        sep=';',
        quotechar='"',
        dtype=str,
        usecols=["CP ORIGEN", "CP DESTINO"],
        blocksize="256MB"
    )

    pueblos = dd.concat([viajes["CP ORIGEN"], viajes["CP DESTINO"]]).rename("poblado_id")
    conteo = pueblos.value_counts().compute().reset_index()
    conteo.columns = ["poblado_id", "frecuencia"]

    top_10000 = conteo.sort_values(by="frecuencia", ascending=False).head(10000)
    top_10000.to_csv("top_pueblos.csv", index=False)

    print("\n--- Top 10.000 Pueblos con más Viajes ---")
    print(top_10000.head(10))

# ============ PROCESO PRINCIPAL ============

if __name__ == "__main__":
    inicio = time.time()

    df = dd.read_csv(
        "eldoria.csv",
        sep=';',
        quotechar='"',
        dtype=str,
        usecols=["CP ORIGEN", "ESPECIE", "GENERO", "FECHA NACIMIENTO"],
        blocksize="256MB"
    )

    conteo = df["CP ORIGEN"].str[0].value_counts().compute().sort_index()
    print("\n¿Cuántas personas por estrato social?")
    for estrato, cantidad in conteo.items():
        print(f"  Estrato {estrato}: {cantidad:,} personas")

    total = conteo.sum()
    print("\n¿Qué porcentaje representa cada estrato?")
    for estrato, cantidad in conteo.items():
        porcentaje = (cantidad / total) * 100
        print(f"  Estrato {estrato}: {porcentaje:.2f}%")

    df["FECHA NACIMIENTO"] = dd.to_datetime(df["FECHA NACIMIENTO"].str.split("T").str[0], errors="coerce")
    hoy = datetime.now()
    df["EDAD"] = ((hoy - df["FECHA NACIMIENTO"]).dt.days // 365)
    df = df.dropna(subset=["ESPECIE", "GENERO", "EDAD"])

    resumen = df.groupby(["ESPECIE", "GENERO", "EDAD"]).size().reset_index()
    resumen = resumen.rename(columns={0: "CANTIDAD"}).persist()
    resumen_pd = resumen.compute()
    resumen_pd["GENERO"] = resumen_pd["GENERO"].str.upper().str.strip()

    imprimir_tiempo("Tiempo total Dask", inicio)

    # Edad promedio y mediana
    edad_promedio = resumen_pd.groupby(["ESPECIE", "GENERO"]).apply(
        lambda g: (g["EDAD"] * g["CANTIDAD"]).sum() / g["CANTIDAD"].sum()
    ).round(2)
    edad_mediana = resumen_pd.groupby(["ESPECIE", "GENERO"]).apply(mediana_ponderada)

    print("\nEdad Promedio por Especie y Género:")
    print(edad_promedio)
    print("\nEdad Mediana por Especie y Género:")
    print(edad_mediana)

    proporcion_por_rango_etario(resumen_pd)
    calcular_indice_dependencia_total(resumen_pd)
    graficar_piramides(resumen_pd)
    top_10000_pueblos_con_mas_viajes()
