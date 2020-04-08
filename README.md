# Datos-COVID19
El objetivo de la Mesa de Datos COVID-19 liderada por el Ministerio de Ciencia, Tecnología, Conocimiento e Innovación es disponer la información epidemiológica de nuestro país para promover el uso de datos para investigación científica, clínica y para soluciones innovadoras que contribuyan a la toma de decisiones de las autoridades y la ciudadanía frente a esta pandemia. Como primer resultado de este equipo técnico, se disponen los datos epidemiológicos provenientes del Ministerio de Salud (MINSAL), documentados y abiertos para el análisis de la comunidad, en concordancia con la Ley Nº 19.628. 

Ver http://www.minciencia.gob.cl/COVID19 para más información.

# Data Products
[data product 1: Casos totales por comuna incremental](output/producto1): archivo con valores separados por coma (csv) que concatena historia de publicaciones de MINSAL sobre casos totales por comuna. Contiene los campos 'Región', 'Comuna', 'Población', '[fecha]', donde la última columna tiene los 'Casos Confirmados' reportados en cada publicación.

[data product 2: Casos totales por comuna](output/producto2) (un archivo por informe): archivos con valores separados por coma (csv) con la información a nivel comunal por cada informe publicado. Cada archivo contiene los campos 'Región', 'Comuna', 'Población', 'Casos Confirmados'.

[data product 3: Casos totales por región incremental](output/producto3): archivo con valores separados por coma (csv) que concatena historia de publicaciones de casos totales por parte de MINSAL. Contiene los campos 'Región', '[fecha]', este último con el valor de la columna 'Casos totales' reportados por el MINSAL diariamente.

[data product 4: Casos totales por región](output/producto4) (un archivo por informe): archivos con valores separados por coma (csv) con la información a nivel regional publicada diariamente por MINSAL, las columnas varían a mediada que MINSAL dispone la información. Los campos para archivos posteriores a 31/3  son 'Región', 'Casos Nuevos', 'Casos totales', '%Casos Totales', 'Fallecidos'; para archivos anteriores son 'Región', 'Casos Nuevos', 'Casos totales', 'Recuperados'.  

## Como funciona?
En cuanto a los archivos a nivel comunal: Transcribimos los datos publicados por el Ministerio de Salud en pdf en:
https://www.minsal.cl/nuevo-coronavirus-2019-ncov/informe-epidemiologico-covid-19/
A partir de esa transcripción se genera un archivo csv, ubicado en la carpeta input.
Este se procesa con el código en src, para generar los archivos csv en output.

En cuanto a los archivos a nivel regional: Hacemos scrapping de tabla en https://www.minsal.cl/nuevo-coronavirus-2019-ncov/casos-confirmados-en-chile-covid-19/ y generamos archivo csv por día.

![dataUpdate](https://github.com/MinCiencia/Datos-COVID19/workflows/dataUpdate/badge.svg)

# Contacto
Si encuentras errores, por favor repórtalos [acá](https://github.com/MinCiencia/Datos-COVID19/issues)
Si has creado una solución que permita facilitar el trabajo con estos datos, algún análisis, o simplemente tienes una solicitud de data product considerando los datos que MINSAL hace públicos hoy, escríbenos a darancibia@minciencia.gob.cl
