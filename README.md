# Datos-COVID19
El objetivo de la Mesa de Datos COVID-19 del Ministerio de Ciencia, Tecnología, Conocimiento e Innovación es usar información del Ministerio de Salud para acelerar la preparación de evidencia científica que apoye la toma de decisiones de las autoridades y la ciudadanía. Como primer resultado, esta mesa dispone los datos epidemiológicos públicos en un formato estándar de datos abiertos, que eperamos sea útil para análisis, en concordancia con la Ley Nº 19.628. 

Ver http://www.minciencia.gob.cl/COVID19 para más información.

## Como funciona?
En cuanto a los archivos a nivel comunal: Transcribimos los datos publicados por el Ministerio de Salud en pdf en:
https://www.minsal.cl/nuevo-coronavirus-2019-ncov/informe-epidemiologico-covid-19/
A partir de esa transcripción se genera un archivo csv, ubicado en la carpeta input.
Este se procesa con el código en src, para generar los archivos csv en output.

En cuanto a los archivos a nivel regional: Hacemos scrapping de tabla en https://www.minsal.cl/nuevo-coronavirus-2019-ncov/casos-confirmados-en-chile-covid-19/ y generamos archivo csv por día.

## Encabezados
[data product 1](output/producto1): 'Region', 'Comuna', 'Poblacion', '[fecha]', incrementando la ultima columna cada vez que MINSAL publica con el valor de casos confirmados por comuna. 

[data product 2](output/producto2) : 'Region', 'Comuna', 'Poblacion', 'Casos Confirmados', un archivo por fecha de publicación del Ministerio de Salud

data product 3 [encabezado(explicación, si es necesaria)]: [en desarrollo]


[data product 4](output/producto4):  Para archivos posteriores a 31/3 ('Region', 'Casos Nuevos', '%Casos Totales', 'Fallecidos'), para archivoa anteriores ('Region', 'Casos Nuevos', 'Recuperados', 'Fallecidos') 
