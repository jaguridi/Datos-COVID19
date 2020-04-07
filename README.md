# Datos-COVID19
El objetivo de la Mesa de Datos COVID-19 del Ministerio de Ciencia, Tecnología, Conocimiento e Innovación es disponer información del Ministerio de Salud (MINSAL) para acelerar la preparación de evidencia científica que apoye la toma de decisiones de las autoridades y la ciudadanía. Como primer resultado, esta mesa dispone los datos epidemiológicos que han sido publicados en un formato estándar de datos abiertos, útil para análisis, en concordancia con la Ley Nº 19.628. 

## Como funciona?
En cuanto a los archivos a nivel comunal: Transcribimos los datos publicados por el Ministerio de Salud en pdf en:
https://www.minsal.cl/nuevo-coronavirus-2019-ncov/informe-epidemiologico-covid-19/
A partir de esa transcripción se genera un archivo csv, ubicado en la carpeta input.
Este se procesa con el código en src, para generar los archivos csv en output.

En cuanto a los archivos a nivel regional: [en desarrollo]

## Encabezados
[data product 1](output/producto1): 'Region', 'Comuna', 'Poblacion', '[fecha]', incrementando la ultima columna cada vez que MINSAL publica con el valor de casos confirmados por comuna. 

[data product 2](output/producto2) [encabezado(explicación, si es necesaria)]: 'Region', 'Comuna', 'Poblacion', 'Casos Confirmados', un archivo por fecha

data product 3 [encabezado(explicación, si es necesaria)]: [en desarrollo]

data product 4 [encabezado(explicación, si es necesaria)]: [en desarrollo]

data product 5 [encabezado(explicación, si es necesaria)]: [en desarrollo]
