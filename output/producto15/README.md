# Descripción
Archivo que da cuenta de los casos nuevos por fecha de inicio de sus síntomas en cada una de las comunas de Chile, según residencia. Refleja la información del último informe epidemiológico publicado por el Ministerio de Salud del país.

Se entiende por fecha de inicio de síntomas el momento de la manifestación clínica de la enfermedad.

Se entiende por comuna de residencia la comuna que la persona declara como su vivienda habitual. 

**Nota aclaratoria 1:** Los datos son provisorios a la fecha del último reporte, pues se van actualizando retroactivamente a medida que se confirman casos y evoluciona la vigilancia e investigación epidemiológica desarrollada por el Departamento de Epidemiología del Ministerio de Salud del país.

**Nota aclaratoria 2:** El archivo no contempla los casos con región o comuna desconocida, es decir, aquellos casos en que no se registró la región de vivienda habitual en la notificación o bien son casos con domicilio en el extranjero. 

**Nota aclaratoria 3:** Los informes epidemiológicos del Ministerio de Salud informan del último día contabilizado para efectos de la elaboración de cada uno de ellos, habitualmente con corte a las 21 hrs. 

**Nota aclaratoria 4:** Previo al 15 de abril de 2020 los informes epidemiológicos del Ministerio de Salud no entregaban datos de confirmados notificados en comunas con bajo número de casos, para proteger la identidad de las personas contagiadas. 

# Fuente
Informes epidemiológicos publicados periódicamente por el Ministerio de Salud de Chile. Ver en:
https://www.minsal.cl/nuevo-coronavirus-2019-ncov/informe-epidemiologico-covid-19/

A su vez, el Ministerio de Salud utiliza como fuente para la elaboración de estos informes el Sistema de notificación EPIVIGILA, del Departamento de Epidemiología, DIPLAS. 

# Frecuencia de actualización

Cada 2 a 3 días.

# Columnas y valores

3 archivos con valores separados por coma (csv), el primero reporta el total de casos nuevos por fecha inicio de síntomas por comuna, para casos confirmados por semana epidemiológica, el segundo la serie de tiempo de los datos anteriores y el tercero indica las fechas que marcan los inicios y términos de cada semana semana epidemiológica. El primer archivo contiene los campos 'Región', 'Comuna', 'Población', '[semana epidemiológica]', donde la última columna contiene el 'Total de casos nuevos con inicio de síntomas en esa semana para casos confirmados' reportados en cada comuna, para cada semana epidemiológica. 
