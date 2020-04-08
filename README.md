# Datos-COVID19
El objetivo de la Mesa de Datos COVID-19 del Ministerio de Ciencia, Tecnología, Conocimiento e Innovación es disponer Datos de Salud provenientes del Ministerio de Salud (MINSAL) para que la comunidad pueda construir soluciones interoperables, disponibles para fines de investigación e innovación y apoyar la toma de decisiones de las autoridades y la ciudadanía. Como primer resultado y como contribución a obtener el máximo aprendizaje de esta crisis, se dispondrán de datos epidemiológicos públicos, bien documentado, abiertos para el análisis de la comunidad y en concordancia con la Ley Nº 19.628. 

Ver http://www.minciencia.gob.cl/COVID19 para más información.

## Como funciona?
En cuanto a los archivos a nivel comunal: Transcribimos los datos publicados por el Ministerio de Salud en pdf en:
https://www.minsal.cl/nuevo-coronavirus-2019-ncov/informe-epidemiologico-covid-19/
A partir de esa transcripción se genera un archivo csv, ubicado en la carpeta input.
Este se procesa con el código en src, para generar los archivos csv en output.

En cuanto a los archivos a nivel regional: Hacemos scrapping de tabla en https://www.minsal.cl/nuevo-coronavirus-2019-ncov/casos-confirmados-en-chile-covid-19/ y generamos archivo csv por día.

## Encabezados
[data product 1](output/producto1): 'Region', 'Comuna', 'Poblacion', '[fecha]', incrementando la ultima columna cada vez que MINSAL publica con el valor de casos confirmados por comuna. 

[data product 2](output/producto2): 'Region', 'Comuna', 'Poblacion', 'Casos Confirmados', un archivo por fecha de publicación del Ministerio de Salud

[data product 3](output/producto3): Corresponde al total de la columna 'Casos totales' reportados por el MINSAL, agregando una columna por día.

[data product 4](output/producto4):  Para archivos posteriores a 31/3 ('Region', 'Casos Nuevos', 'Casos totales', '%Casos Totales', 'Fallecidos'), para archivos anteriores ('Region', 'Casos Nuevos', 'Casos totales', 'Recuperados') 


![dataUpdate](https://github.com/MinCiencia/Datos-COVID19/workflows/dataUpdate/badge.svg)

# Contacto
Si encuentras errores, por favor repórtalos [acá](https://github.com/MinCiencia/Datos-COVID19/issues)
Si has creado una solución que permita facilitar el trabajo con estos datos, algún análisis, o simplemente tienes una solicitud de data product considerando los datos que MINSAL hace públicos hoy, escríbenos a darancibia@minciencia.gob.cl
