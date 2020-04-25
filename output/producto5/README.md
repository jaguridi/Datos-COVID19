# Descripción
Set de 2 archivos sobre casos a nivel nacional. El primero de ellos (TotalesNacionales.csv) incluye los casos nuevos confirmados, totales o acumulados, recuperados, fallecidos a nivel nacional y activos según fecha de diagnóstico, reportados diariamente por el Ministerio de Salud desde el 03-03-2020. El segundo (recuperados.csv) contiene sólo los casos recuperados.

Se entiende por caso confirmado la persona que cumple con los criterios de definición de caso sospechoso con una muestra positiva de SARS-CoV-2.

Se entiende por casos totales o acumulados el número total de casos confirmados desde el primer caso confirmado hasta la fecha de elaboración del reporte o informe. 

Se entiende en este reporte por casos recuperados las personas que tras ser confirmadas de COVID-19, han estado en cuarentena pasando 14 días sin síntomas. Para calcular casos recuperados considerando la fecha de inicio de síntomas, se puede utilizar el [producto 15: Casos nuevos por fecha de inicio de sintomas](https://github.com/MinCiencia/Datos-COVID19/tree/master/output/producto15).

Se entiende en este reporte por casos activos la diferencia entre el total de casos confirmados y (personas recuperadas y personas fallecidas). Para calcular casos activos considerando la fecha de inicio de síntomas, se puede utilizar el [producto 15: Casos nuevos por fecha de inicio de sintomas](https://github.com/MinCiencia/Datos-COVID19/tree/master/output/producto15).

# Columnas y valores
El primer archivo (TotalesNacionales.csv) contiene las filas ‘Fecha’, ‘Casos nuevos’, ‘Casos totales’, ‘Casos recuperados’, ‘Fallecidos’ y ‘Casos activos’. El segundo archivo (recuperados.csv) contiene las filas ‘Fecha’ y ‘Recuperados’. Estos valores están separados entre sí por comas (csv).

# Fuente
Ministerio de Salud. Ver en:
https://www.minsal.cl/nuevo-coronavirus-2019-ncov/casos-confirmados-en-chile-covid-19/

# Frecuencia de actualización
Actualización diaria. 

# Notas Aclaratorias

**Nota aclaratoria 1**:  Los reportes del Ministerio de Salud informan del último día contabilizado para efectos de la elaboración de cada uno de ellos, habitualmente con corte a las 21 hrs. 

**Nota aclaratoria 2**: Previo al 15 de abril de 2020 los reportes del Ministerio de Salud no entregaban datos de confirmados notificados en comunas con bajo número de casos, para proteger la identidad de las personas contagiadas.

