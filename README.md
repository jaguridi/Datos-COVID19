# Datos-COVID19
El objetivo de la Mesa de Datos COVID-19 liderada por el Ministerio de Ciencia, Tecnología, Conocimiento e Innovación es disponer la información epidemiológica de nuestro país para promover el uso de datos para investigación científica, clínica y para soluciones innovadoras que contribuyan a la toma de decisiones de las autoridades y la ciudadanía frente a esta pandemia. Como primer resultado de este equipo técnico, se disponen los datos epidemiológicos provenientes del Ministerio de Salud (MINSAL), documentados y abiertos para el análisis de la comunidad, en concordancia con la [Ley Nº 19.628](https://www.leychile.cl/Navegar?idNorma=141599). 

Ver http://www.minciencia.gob.cl/COVID19 para más información.

# Data Products

[Data Product 1 - Casos totales por comuna incremental](output/producto1): Archivo con valores separados por coma (csv) que concatena historia de publicaciones de MINSAL sobre casos confirmados totales por comuna. Contiene las columnas 'Región', ‘Código Región’, 'Comuna', ‘Código comuna’, 'Población', múltiples columnas correspondientes a '[fecha]', y una columna 'Tasa'. [Ver más](output/producto1).

[Data Product 2 - Casos totales por comuna](output/producto2): Archivos con valores separados por coma (csv) con la información de casos confirmados notificados a nivel comunal por cada informe publicado. Cada archivo contiene las columnas 'Región', ‘Código Región’, 'Comuna', ‘Código comuna’, 'Población' y 'Casos Confirmados'. [Ver más](output/producto2).

[Data Product 3 - Casos totales por región incremental](output/producto3): Archivo con valores separados por coma (csv) que concatena historia de publicaciones de casos totales por parte de MINSAL. El archivo contiene una columna 'Región', seguida por columnas correspondientes a '[fecha]'. Estas últimas columnas, ‘[fecha]’, contienen los 'Casos Confirmados' reportados por el Ministerio de Salud de Chile en cada una de las fechas que se indican en las respectivas columnas. [Ver más](output/producto3).

[Data Product 4 - Casos totales por región](output/producto4) (un archivo por informe): Serie de archivos que dan cuenta del total de casos confirmados, casos recuperados, % de casos totales y casos fallecidos en cada una de las regiones de Chile, según residencia. Cada uno de los archivos corresponde a la información diaria que reporta el Ministerio de Salud del país. Existe variabilidad en los campos según la fecha. [Ver más](output/producto4).

[Data Product 5 - Totales Nacionales Diarios](output/producto5): Set de 2 archivos sobre casos a nivel nacional. El primero de ellos (TotalesNacionales.csv) incluye los casos nuevos confirmados, totales o acumulados, recuperados, fallecidos a nivel nacional y activos según fecha de diagnóstico, reportados diariamente por el Ministerio de Salud desde el 03-03-2020. El segundo (recuperados.csv) contiene sólo los casos recuperados. [Ver más](output/producto5).

[Data Product 6 (contribuido) - Enriquecimiento del Data Product 2](output/producto6): Set de 2 archivos, en formato CSV y JSON, que dan cuenta de la tasa de incidencia acumulada y los casos confirmados acumulados en cada una de las comunas de Chile, según residencia, conforme a los informes epidemiológicos publicados por el Ministerio de Salud del país. Esto es una mejora derivada del producto 2, al colocar varios archivos de aquel producto en un solo archivo. [Ver más](output/producto6).

[Data Product 7 - Exámenes PCR por región](output/producto7): Set de 2 archivos que dan cuenta del número de exámenes PCR realizados por región reportados diariamente por el Ministerio de Salud, desde el 09-04-2020. El primer archivo (PCR.csv) contiene las columnas ‘Región’, ‘Código Región’ y ‘Población’, seguidas por columnas correspondientes a ‘[Fecha]’. Estas últimas columnas, ‘[Fecha]’ indican el número de exámenes realizados por región, desde el 09-04-2020 hasta la fecha. El segundo archivo (PCR_T.csv) es la versión traspuesta del primer archivo. [Ver más](output/producto7).

[Data Product 8 - Pacientes en UCI por región](output/producto8): Set de 2 archivos que dan cuenta del número de pacientes en UCI por región reportados diariamente por el Ministerio de Salud, desde el 01-04-2020. El primer archivo (UCI.csv) contiene las columnas ‘Región’, ‘Código Región’ y ‘Población’, y múltiples columnas correspondientes a ‘[Fecha]’. Estas últimas columnas, ‘[Fecha]’ indican el número de pacientes en UCI por región, desde el 01-04-2020 hasta la fecha. El segundo archivo (UCI_T.csv) es la versión traspuesta del primer archivo. Estos valores están separados entre sí por comas (csv). [Ver más](output/producto8).

[Data Product 9 - Pacientes en UCI por grupo de edad](output/producto9): Set de 2 archivos que dan cuenta del número de pacientes en UCI por grupos etarios (<=39; 40-49; 50-59; 60-69; y >=70) reportados diariamente por el Ministerio de Salud, desde el 01-04-2020. El primer archivo (HospitalizadosUCIEtario.csv) contiene la columna ‘Grupo de edad’, seguida por columnas correspondientes a ‘[Fecha]’. Estas últimas columnas, ‘[Fecha]’, indican el número de pacientes en UCI por grupo etario, desde el 01-04-2020 hasta la fecha. El segundo archivo (HospitalizadosUCIEtario_T.csv) es la versión traspuesta del primer archivo. [Ver más](output/producto9).

[Data Product 10 - Fallecidos por grupo de edad](output/producto10): Set de 2 archivos que dan cuenta del número de fallecidos por grupos etarios (<=39; 40-49; 50-59; 60-69; 70-79; 80-89; y >=90) reportados diariamente por el Ministerio de Salud, desde el 09-04-2020. El primer archivo (FallecidosEtario.csv) contiene la columna ‘Grupo de edad’, seguida por columnas correspondientes a ‘[Fecha]’. Estas últimas columnas, ‘[Fecha]’, indican el número de personas fallecidas por grupo etario, desde el 09-04-2020 hasta la fecha. El segundo archivo (FallecidosEtario_T.csv) es la versión traspuesta del primer archivo. Estos valores están separados entre sí por comas (csv). [Ver más](output/producto10).

[Data Product 11 (contribuido) - Enriquecimiento del Data Product 4](output/producto11): El [Data Product 4](output/producto4) con todos los datos compilados en formato CSV y JSON, en un solo archivo, llamados producto4.csv y producto4.json respectivamente. Los archivos contienen las columnas ‘Región’, ‘Nuevos Casos’, ‘Casos Confirmados’, ‘Fallecidos’, ‘Fecha’, ‘Región ID’, ‘Población’ y ‘Tasa’. Estos valores están separados entre sí por comas (csv), y organizados en tuplas en el caso del JSON. [Ver más](output/producto11).

[Data Product 12 (contribuido) - Enriquecimiento del Data Product 7](output/producto12): El [Data Product 7](output/producto7) con todos los datos compilados en formato CSV y JSON, en un solo archivo, llamados producto7.csv y producto7.json respectivamente. Los archivos contienen las columnas ‘Región’, ‘Población’, ‘Fecha’, ‘PCR Realizados’, ‘Región ID’, y ‘Tasa’. Estos valores están separados entre sí por comas (csv), y organizados en tuplas en el JSON. [Ver más](output/producto12).

[Data Product 13 - Casos nuevos por región incremental](output/producto13): Set de 2 archivos que dan cuenta del número de casos nuevos por día según resultado del diagnóstico, por región de residencia, reportados por el Ministerio de Salud desde el 03-03-2020. El primer archivo (CasosNuevosCumulativo.csv) contiene la columna ‘Región’, seguida por columnas correspondientes a ‘[Fecha]’. Estas últimas columnas, ‘[Fecha]’, indican el número de casos nuevos acumulativos, por región, desde el 03-03-2020 hasta la fecha. El segundo archivo (CasosNuevosCumulativo_T.csv) es la versión traspuesta del primer archivo. Estos valores están separados entre sí por comas (csv). [Ver más](output/producto13).

[Data Product 14 - Fallecidos por región incremental](output/producto14): Set de 2 archivos que dan cuenta del número de fallecidos por día, según región de residencia, y concatena la historia de los reportes del Ministerio de Salud desde el 22-03-2020. El primer archivo (FallecidosCumulativo.csv) contiene la columna ‘Región’, seguida por columnas correspondientes a ‘[Fecha]’. Estas últimas columnas, ‘[Fecha]’, indican el número de fallecidos acumulativo, por región, desde el 22-03-2020 hasta la fecha. El segundo archivo (FallecidosCumulativo_T.csv) es la versión traspuesta del primer archivo. Estos valores están separados entre sí por comas (csv). [Ver más](output/producto14).

[Data Product 15 - Casos nuevos por fecha de inicio de síntomas por comuna](output/producto15): Set de 3 archivos que dan cuenta de los casos nuevos por fecha de inicio de sus síntomas en cada una de las comunas de Chile, según residencia. Refleja la información del último informe epidemiológico publicado por el Ministerio de Salud del país. Se indexan estos casos según semana epidemiológica reportada en el informe, con fechas incluidas en los archivos. [Ver más](output/producto15).

[Data Product 16 - Casos por genero y grupo de edad](output/producto16): 2 archivos con valores separados por coma (csv), el primero corresponde a casos totales separados por genero y rango etario (valores reportados por el MINSAL), y el segundo a la serie de tiempo de los datos anteriores. Contiene los campos 'Grupo de Edad', 'Sexo', '[fecha]', donde esta última columna contiene 'Casos totales' reportada para un rango etario y sexo por informe epidemiológico.

[Data Product 17 - PCR acumulado e informado en el último día por tipo de establecimientos](output/producto17): archivo con valores separados por coma (csv), corresponde al numero de test realizados por establecimiento, y al numero informado en las últimas 24 horas. Contiene los campos 'Tipo de establecimiento', 'exámenes' que contiene 2 categorías: 'realizados' para el total acumulado e 'informados en el último día', y '[fecha]' que contiene la cantidad reportada para ambas categorías.

[Data Product 18 - Tasa de incidencia historica por comuna y total regional](output/producto18): archivo con valores separados por coma (csv), corresponde a la tasa de incidencia por comuna y total regional, reportado por el MINSAL. Contiene los campos 'Región', 'Comuna', 'Población', '[fecha]', donde esta última columna contiene la 'tasa de incidencia' reportada para comunas y total regional por informe epidemiológico.

[Data product 19 - Casos activos por fecha de inicio de síntomas y comuna](output/producto19): archivo con valores separados por coma (csv), corresponde a el total de personas que mantienen capacidad de contagio, reportado por el MINSAL. Contiene los campos 'Región', 'Comuna', 'Población', '[fecha]', donde la última columna tiene los 'Casos activos' reportados en cada publicación de Epidemiología. **Nota: Casos activos en este reporte (a diferencia del reporte en el producto 5) corresponde al resultado de la investigación epidemiológica y considera activos a casos durante los primeros 14 días después de la fecha de inicio de sus síntomas**

[Data Product 20 - Ventiladores a nivel nacional](output/producto20): archivo con valores separados por coma (csv), corresponde a el total nacional de ventiladores, los ocupados y los disponibles reportado por el MINSAL. Contiene los campos 'Estado' (con valores total, disponibles, ocupados), '[fecha]', donde esta última columna contiene los valores reportados a nivel nacional.

[Data Product 21 - Sintomas por Casos Confirmados e informado en el último día](output/producto21): 4 archivos con valores separados por coma (csv). 2 archivos corresponden a los síntomas informados por personas confirmadas con COVID-19, y 2 archivos a los síntomas informados por personas hospitalizadas por COVID-19, ambos en números acumulados. Contienen los campos 'Sintomas' y '[fecha]' que contiene la cantidad de casos que reportan cada síntoma. **Nota: No todos los informes de situación COVID - 19 de EPI MINSAL contienen información sobre los síntomas**.

[Data Product 22 - Hospitalizados por grupo de edad](output/producto22): 2 archivos con valores separados por coma (csv), el primero corresponde al reporte de hospitalizados por grupo de edad, y el segundo, a la serie de tiempo de los datos anteriores. Contiene los campos 'Grupo de edad', '[fecha]', donde esta última columna contiene el número de 'Hospitalizados' reportados acumulados como resultado de la investigación epidemiológica.

[Data product 23 - Pacientes críticos](output/producto23): 2 archivos con valores separados por coma (csv), el primero corresponde al reporte diario de la cantidad de pacientes críticos, y el segundo, a la serie de tiempo de los datos anteriores. Contiene los campos 'Pacientes críticos', '[fecha]', donde esta última columna contiene el número reportado diariamente.

[Data Product 24 - Hospitalización de pacientes en sistema integrado](output/producto24): 2 archivos con valores separados por coma (csv), el primero corresponde al reporte diario de la cantidad de pacientes en cama Básica, Media, UCI o en UTI, y el segundo, a la serie de tiempo de los datos anteriores. Contiene los campos 'Tipo de Cama' (con las categorías 'Basica', 'Media', 'UCI', 'UTI', '[fecha]', donde esta última columna contiene el número de ocupación por día reportado por la Unidad de Gestión de Camas Críticas de MINSAL para cada categoría. 

[Data Product 25 - Casos actuales por fecha de inicio de síntomas y comuna](output/producto25): archivo con valores separados por coma (csv), corresponde al total de personas confirmadas cuya fecha de inicio de síntomas en la notificación es menor o igual a 14 días a la fecha del reporte epidemiológico (MINSAL), considera los casos confirmados vivos y fallecidos. Contiene los campos 'Región', 'Comuna', 'Población', '[fecha]', donde la última columna tiene los 'Casos actuales' reportados en cada publicación de Epidemiología. 

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
