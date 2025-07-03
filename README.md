Censo Mágico de Eldoria



Este proyecto fue desarrollado como solución a los problemas de identidad y movilidad en el reino ficticio de Eldoria, como parte del curso de Computación Paralela y Distribuida.



Contexto



En un mundo mágico donde la tecnología apenas comienza a asomar entre hechizos y dragones, el rey Aurelius IV ha confiado en un grupo de estudiantes para resolver dos desafíos cruciales:



1\. Establecer un sistema de identificación ciudadana confiable.

2\. Mejorar las rutas de comunicación entre ciudades y aldeas.



Solución Implementada



Usando tecnologías modernas como Dask y Pandas, se proceso un censo masivo con mas de 100 millones de ciudadanos y sus desplazamientos habituales.



Se desarrollo un sistema que permite:

\- Calcular la cantidad y el porcentaje de personas por estrato social.

\- Determinar la edad promedio y mediana por especie y genero.

\- Estimar la proporción etaria en distintos rangos de edad.

\- Construir pirámides de edad por especie.

\- Calcular el índice de dependencia poblacional.

\- Detectar los 10.000 pueblos con mas viajes, base para mejorar la red de caminos.



Tecnologías y Librerías



\- Python 3

\- Dask (procesamiento paralelo)

\- Pandas

\- Matplotlib



Estructura del Proyecto



.

├── Trabajo\_computacion\_paralela.py   # Código principal

├── Problema.txt                      # Descripción del problema y solución

├── eldoria.csv                       # Archivo de entrada con el censo (link de descarga adjuntado)

├── top\_pueblos.csv                   # Salida con los 10,000 pueblos mas conectados

├── README.txt                        # Este archivo



Como Ejecutar



1\. Instala las dependencias:



&nbsp;  pip install dask pandas matplotlib



2\. Asegúrate de tener eldoria.csv en el mismo directorio.



3\. Ejecuta el script:



&nbsp;  python Trabajo\_computacion\_paralela.py



4\. Se generaran estadísticas y gráficos poblacionales, además de un archivo top\_pueblos.csv.



Preguntas Respondidas



\- ¿Cuantas personas pertenecen a cada estrato social?

\- ¿Que porcentaje de la poblacion pertenece a cada estrato?

\- ¿Cual es la edad promedio y mediana por especie y genero?

\- ¿Como se distribuye la poblacion por rangos etarios?

\- ¿Como es la piramide de edad por especie?

\- ¿Cual es el indice de dependencia del reino?

\- ¿Cuales son los 10.000 poblados con mas viajes?



Descarga de base de datos Eldoria

https://drive.google.com/file/d/13vO9SLQo2UsbxYzJ2WL\_IuyVD5Btkxq5/view

