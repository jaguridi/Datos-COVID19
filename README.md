# Datos-COVID19
El objetivo de la Mesa de Datos COVID-19 liderada por el Ministerio de Ciencia, Tecnología, Conocimiento e Innovación es disponer la información epidemiológica de nuestro país para promover el uso de datos para investigación científica, clínica y para soluciones innovadoras que contribuyan a la toma de decisiones de las autoridades y la ciudadanía frente a esta pandemia. Como primer resultado de este equipo técnico, se disponen los datos epidemiológicos provenientes del Ministerio de Salud (MINSAL), documentados y abiertos para el análisis de la comunidad, en concordancia con la [Ley Nº 19.628](https://www.leychile.cl/Navegar?idNorma=141599). 

Ver http://www.minciencia.gob.cl/COVID19 para más información.

# Data Products

[Data Product 1: Casos totales por comuna incremental](output/producto1): Archivo con valores separados por coma (csv) que concatena historia de publicaciones de MINSAL sobre casos confirmados totales por comuna. Contiene las columnas 'Región', ‘Código Región’, 'Comuna', ‘Código comuna’, 'Población', múltiples columnas correspondientes a '[fecha]', y una columna 'Tasa'. [Ver más](output/producto1).

[Data Product 2: Casos totales por comuna](output/producto2): Archivos con valores separados por coma (csv) con la información de casos confirmados notificados a nivel comunal por cada informe publicado. Cada archivo contiene las columnas 'Región', ‘Código Región’, 'Comuna', ‘Código comuna’, 'Población' y 'Casos Confirmados'. [Ver más](output/producto2).

[Data Product 3: Casos totales por región incremental](output/producto3): Archivo con valores separados por coma (csv) que concatena historia de publicaciones de casos totales por parte de MINSAL. El archivo contiene una columna 'Región', seguida por columnas correspondientes a '[fecha]'. Estas últimas columnas, ‘[fecha]’, contienen los 'Casos Confirmados' reportados por el Ministerio de Salud de Chile en cada una de las fechas que se indican en las respectivas columnas. [Ver más](output/producto3).

[Data Product 4: Casos totales por región](output/producto4) (un archivo por informe): Serie de archivos que dan cuenta del total de casos confirmados, casos recuperados, % de casos totales y casos fallecidos en cada una de las regiones de Chile, según residencia. Cada uno de los archivos corresponde a la información diaria que reporta el Ministerio de Salud del país. Existe variabilidad en los campos según la fecha. [Ver más](output/producto4).

[Data Product 5: Totales Nacionales Diarios](output/producto5): Set de 2 archivos sobre casos a nivel nacional. El primero de ellos (TotalesNacionales.csv) incluye los casos nuevos confirmados, totales o acumulados, recuperados, fallecidos a nivel nacional y activos según fecha de diagnóstico, reportados diariamente por el Ministerio de Salud desde el 03-03-2020. El segundo (recuperados.csv) contiene sólo los casos recuperados. [Ver más](output/producto5).

[Data Product 6 (contribuido): Enriquecimiento del Data Product 2](output/producto6/bulk): Set de 2 archivos, en formato CSV y JSON, que dan cuenta de la tasa de incidencia acumulada y los casos confirmados acumulados en cada una de las comunas de Chile, según residencia, conforme a los informes epidemiológicos publicados por el Ministerio de Salud del país. Esto es una mejora derivada del producto 2, al colocar varios archivos de aquel producto en un solo archivo. [Ver más](output/producto6).

[data product 7: Exámenes PCR por región](output/producto7): 2 archivos con valores separados por coma (csv), el primero corresponde al reporte de exámenes PCR realizados, y el segundo, a la serie de tiempo de los datos anteriores, por región. Contiene los campos 'Región', 'Población', '[fecha]', este último con el valor de 'Exámenes PCR' reportados por el MINSAL diariamente. **Nota: el dato no refleja la cantidad de muestras por región, en algunos casos se toman más muestras que la capacidad de exámenes PCR que tiene la región, por ende se envían a laboratorios fuera de la región** 

[data product 8: Pacientes en UCI por región](output/producto8): 2 archivos con valores separados por coma (csv), el primero corresponde al reporte de hospitalizados UCI, y el segundo, a la serie de tiempo de los datos anteriores, por región. Contiene los campos ''Grupo de edad', '[fecha]', donde esta última columna contiene 'Pacientes en UCI' reportados por día.

[data product 9: Pacientes en UCI por grupo de edad](output/producto9): 2 archivos con valores separados por coma (csv), el primero corresponde al reporte de serie de tiempo de hospitalizados UCI, y el segundo, a la serie de tiempo de los datos anteriores, por grupo de edad. Contiene los campos 'Grupo de edad', '[fecha]', donde esta última columna contiene 'Pacientes en UCI' reportados por día por grupo de edad.

[data product 10: Fallecidos por grupo de edad](output/producto10): 2 archivos con valores separados por coma (csv), el primero corresponde al reporte de serie de tiempo de fallecidos, y el segundo, a la serie de tiempo de los datos anteriores, por rango etario. Contiene los campos ''Grupo de edad', '[fecha]', donde esta última columna contiene 'Fallecidos' reportados por día.

[data product 11 [contributed]: enriquecimiento del data product4](output/producto11/bulk): producto4 con todos los datos compilados en formato CSV y JSON, llamados producto4.csv y producto4.json respectivamente.

[data product 12 [contributed]: enriquecimiento del data product7](output/producto12/bulk): producto7 con todos los datos compilados en formato CSV y JSON, llamados producto7.csv y producto7.json respectivamente.

[data product 13: Casos nuevos por región incremental](output/producto13): 2 archivos con valores separados por coma (csv), el primero corresponde a casos nuevos por región con los valores diarios reportados por el MINSAL, y el segundo a la serie de tiempo de los datos anteriores. Contiene los campos 'Región', '[fecha]', donde esta última columna contiene 'Casos Nuevos' reportados por región.

[data product 14: Fallecidos por región incremental](output/producto14): 2 archivos con valores separados por coma (csv), el primero corresponde a casos fallecidos por región con los valores diarios reportados por el MINSAL, y el segundo a la serie de tiempo de los datos anteriores. Contiene los campos 'Región', '[fecha]', donde esta última columna contiene 'Fallecidos' reportados por región.

[data product 15: Casos nuevos por fecha de inicio de síntomas por comuna](output/producto15): 3 archivos con valores separados por coma (csv), el primero reporta el total de casos nuevos por fecha inicio de síntomas por comuna, para casos confirmados por semana epidemiológica, el segundo la serie de tiempo de los datos anteriores y el tercero indica las fechas que marcan los inicios y términos de cada semana semana epidemiológica. El primer archivo contiene los campos 'Región', 'Comuna', 'Población', '[semana epidemiológica]', donde la última columna contiene el 'Total de casos nuevos con inicio de síntomas en esa semana para casos confirmados' reportados en cada comuna, para cada semana epidemiológica. **Nota: acorde a lo informado por Epidemiología MINSAL, la fecha de inicio de síntomas corresponde al momento de la manifestación clínica de la enfermedad, y son provisorios a la fecha del último reporte, pues se van actualizando retroactivamente a medida que se confirman casos y evoluciona la investigación epidemiológica**

[data product 16: Casos por genero y grupo de edad](output/producto16): 2 archivos con valores separados por coma (csv), el primero corresponde a casos totales separados por genero y rango etario (valores reportados por el MINSAL), y el segundo a la serie de tiempo de los datos anteriores. Contiene los campos 'Grupo de Edad', 'Sexo', '[fecha]', donde esta última columna contiene 'Casos totales' reportada para un rango etario y sexo por informe epidemiológico.

[data product 17: PCR acumulado e informado en el último día por tipo de establecimientos](output/producto17): archivo con valores separados por coma (csv), corresponde al numero de test realizados por establecimiento, y al numero informado en las últimas 24 horas. Contiene los campos 'Tipo de establecimiento', 'exámenes' que contiene 2 categorías: 'realizados' para el total acumulado e 'informados en el último día', y '[fecha]' que contiene la cantidad reportada para ambas categorías.

[data product 18: Tasa de incidencia historica por comuna y total regional](output/producto18): archivo con valores separados por coma (csv), corresponde a la tasa de incidencia por comuna y total regional, reportado por el MINSAL. Contiene los campos 'Región', 'Comuna', 'Población', '[fecha]', donde esta última columna contiene la 'tasa de incidencia' reportada para comunas y total regional por informe epidemiológico.

[data product 19: Casos activos por fecha de inicio de síntomas y comuna](output/producto19): archivo con valores separados por coma (csv), corresponde a el total de personas que mantienen capacidad de contagio, reportado por el MINSAL. Contiene los campos 'Región', 'Comuna', 'Población', '[fecha]', donde la última columna tiene los 'Casos activos' reportados en cada publicación de Epidemiología. **Nota: Casos activos en este reporte (a diferencia del reporte en el producto 5) corresponde al resultado de la investigación epidemiológica y considera activos a casos durante los primeros 14 días después de la fecha de inicio de sus síntomas**

[data product 20: Ventiladores a nivel nacional](output/producto20): archivo con valores separados por coma (csv), corresponde a el total nacional de ventiladores, los ocupados y los disponibles reportado por el MINSAL. Contiene los campos 'Estado' (con valores total, disponibles, ocupados), '[fecha]', donde esta última columna contiene los valores reportados a nivel nacional.

[data product 21: Sintomas por Casos Confirmados e informado en el último día](output/producto21): 4 archivos con valores separados por coma (csv). 2 archivos corresponden a los síntomas informados por personas confirmadas con COVID-19, y 2 archivos a los síntomas informados por personas hospitalizadas por COVID-19, ambos en números acumulados. Contienen los campos 'Sintomas' y '[fecha]' que contiene la cantidad de casos que reportan cada síntoma. **Nota: No todos los informes de situación COVID - 19 de EPI MINSAL contienen información sobre los síntomas**.

[data product 22: Hospitalizados por grupo de edad](output/producto22): 2 archivos con valores separados por coma (csv), el primero corresponde al reporte de hospitalizados por grupo de edad, y el segundo, a la serie de tiempo de los datos anteriores. Contiene los campos 'Grupo de edad', '[fecha]', donde esta última columna contiene el número de 'Hospitalizados' reportados acumulados como resultado de la investigación epidemiológica.

[data product 23: Pacientes críticos](output/producto23): 2 archivos con valores separados por coma (csv), el primero corresponde al reporte diario de la cantidad de pacientes críticos, y el segundo, a la serie de tiempo de los datos anteriores. Contiene los campos 'Pacientes críticos', '[fecha]', donde esta última columna contiene el número reportado diariamente.

[data product 24: Hospitalización de pacientes en sistema integrado](output/producto24): 2 archivos con valores separados por coma (csv), el primero corresponde al reporte diario de la cantidad de pacientes en cama Básica, Media, UCI o en UTI, y el segundo, a la serie de tiempo de los datos anteriores. Contiene los campos 'Tipo de Cama' (con las categorías 'Basica', 'Media', 'UCI', 'UTI', '[fecha]', donde esta última columna contiene el número de ocupación por día reportado por la Unidad de Gestión de Camas Críticas de MINSAL para cada categoría. 

[data product 25: Casos actuales por fecha de inicio de síntomas y comuna](output/producto25): archivo con valores separados por coma (csv), corresponde al total de personas confirmadas cuya fecha de inicio de síntomas en la notificación es menor o igual a 14 días a la fecha del reporte epidemiológico (MINSAL), considera los casos confirmados vivos y fallecidos. Contiene los campos 'Región', 'Comuna', 'Población', '[fecha]', donde la última columna tiene los 'Casos actuales' reportados en cada publicación de Epidemiología. 

**Nota: La fecha otorgada a cada reporte corresponde a la publicación por MINSAL. Habitualmente refleja el registro del día anterior, salvo que se indique lo contrario**


## Como funciona?
En cuanto a los archivos a nivel comunal: Transcribimos los datos publicados por el Ministerio de Salud en pdf en:
https://www.minsal.cl/nuevo-coronavirus-2019-ncov/informe-epidemiologico-covid-19/
A partir de esa transcripción se genera un archivo csv, ubicado en la carpeta input.
Este se procesa con el código en src, para generar los archivos csv en output.

En cuanto a los archivos a nivel regional: Hacemos scraping de tabla en https://www.minsal.cl/nuevo-coronavirus-2019-ncov/casos-confirmados-en-chile-covid-19/ y generamos archivo csv por día.

![dataUpdate](https://github.com/MinCiencia/Datos-COVID19/workflows/dataUpdate/badge.svg)

# Contacto
Si encuentras errores, por favor repórtalos [acá](https://github.com/MinCiencia/Datos-COVID19/issues). La automatización de este proceso y disposición de datos ha sido inicializada por el equipo del Data Observatory (http://www.dataobservatory.net), estan todos invitados a colaborar.
Si has creado una solución que permita facilitar el trabajo con estos datos, algún análisis, o simplemente tienes una solicitud de data product considerando los datos que MINSAL hace públicos hoy, escríbenos a darancibia@minciencia.gob.cl

## Agradecimientos

Geógrafo Virginia Behm - académica Escuela de Salud Pública U. Chile.

Miguel A. Bustos Valdebenito | Estudiante Dr. Ing. Mec. - U.Chile | Mtr. Ing. Ind. - UAI  | Ing. Civil y Ejec. Mec. - U. de Santiago

Annabella Zapata y Carlos Navarrete, Chilecracia y Datawheel
