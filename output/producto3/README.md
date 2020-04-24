# Descripción
Archivo que da cuenta de los casos totales diarios confirmados por laboratorio en cada una de las regiones de Chile, según residencia, y concatena la información reportada por el Ministerio de Salud del país.

Se entiende por caso confirmado la persona que cumple con los criterios de definición de caso sospechoso con una muestra positiva de SARS-CoV-2.

Se entiende por región de residencia la región que la persona declara como su vivienda habitual. 

Se entiende por porcentaje de casos totales el porcentaje del número total de casos registrados en el país. 

**Nota aclaratoria 1:** El archivo no contempla los casos con región o comuna desconocida, es decir, aquellos casos en que no se registró la región de vivienda habitual en la notificación o bien son casos con domicilio en el extranjero.

**Nota aclaratoria 2:**  Los reportes del Ministerio de Salud informan del último día contabilizado para efectos de la elaboración de cada uno de ellos, habitualmente con corte a las 21 hrs. 

**Nota aclaratoria 3:** Previo al 15 de abril de 2020 los reportes del Ministerio de Salud no entregaban datos de confirmados notificados en comunas con bajo número de casos, para proteger la identidad de las personas contagiadas. 

# Fuente
Ministerio de Salud. Ver en:
https://www.minsal.cl/nuevo-coronavirus-2019-ncov/casos-confirmados-en-chile-covid-19/

# Frecuencia de Actualización
Actualización diaria. 

# Columnas y valores
El archivo contiene una columna 'Región', seguida por columnas correspondientes a '[fecha]'. Esta últimas columnas, ‘[fecha]’, contienen los 'Casos Confirmados' reportados por el Ministerio de Salud de Chile en cada una de las fechas que se indican en las respectivas columnas. Estos valores están separados entre sí por comas (csv).
