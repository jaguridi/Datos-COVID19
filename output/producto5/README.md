# DP5 - Totales Nacionales Diarios: Descripción
Set de 2 archivos sobre casos a nivel nacional. El primero de ellos (TotalesNacionales.csv) incluye los casos nuevos confirmados, totales o acumulados, recuperados, fallecidos a nivel nacional y activos según fecha de diagnóstico, reportados diariamente por el Ministerio de Salud desde el 03-03-2020. El segundo (recuperados.csv) contiene sólo los casos recuperados.

Se entiende por caso confirmado la persona que cumple con los criterios de definición de caso sospechoso con una muestra positiva de SARS-CoV-2.

Se entiende por caso nuevo sin síntomas por casos que han sido confirmados COVID-19 positivos pero no tienen manifestación clínica de la enfermedad. La autoridad de salud indicó que estos casos se han testeado por cercanía con contagiados de diversas índoles.

Se entiende por casos totales o acumulados el número total de casos confirmados desde el primer caso confirmado hasta la fecha de elaboración del reporte o informe. 

Se entiende en este reporte por casos recuperados las proyección de personas que tras ser confirmadas de COVID-19, han estado en cuarentena pasando 14 días sin síntomas. Para proyectar casos recuperados considerando la fecha de inicio de síntomas, se puede utilizar el [producto 15: Casos nuevos por fecha de inicio de sintomas](https://github.com/MinCiencia/Datos-COVID19/tree/master/output/producto15).

Se entiende en este reporte por casos activos la diferencia entre el total de casos confirmados y (personas recuperadas y personas fallecidas). Para calcular casos activos considerando la fecha de inicio de síntomas, se puede utilizar el [producto 15: Casos nuevos por fecha de inicio de sintomas](https://github.com/MinCiencia/Datos-COVID19/tree/master/output/producto15).

# Columnas y valores
El primer archivo (TotalesNacionales.csv) contiene las filas ‘Fecha’, ‘Casos nuevos’, ‘Casos totales’, ‘Casos recuperados’, ‘Fallecidos’ y ‘Casos activos’. El segundo archivo (recuperados.csv) contiene las filas ‘Fecha’ y ‘Recuperados’. Estos valores están separados entre sí por comas (csv).

# Fuente
Ministerio de Salud. Ver en:
https://www.minsal.cl/nuevo-coronavirus-2019-ncov/casos-confirmados-en-chile-covid-19/

# Frecuencia de actualización
Actualización diaria. 

# Notas aclaratorias

**Nota aclaratoria 1**:  Los reportes del Ministerio de Salud informan del último día contabilizado para efectos de la elaboración de cada uno de ellos, habitualmente con corte a las 21 hrs. 

**Nota aclaratoria 2**: Previo al 15 de abril de 2020 los reportes del Ministerio de Salud no entregaban datos de confirmados notificados en comunas con bajo número de casos, para proteger la identidad de las personas contagiadas.

**Nota aclaratoria 3**: Casos activos en este reporte (a diferencia del reporte en el [producto 19](../producto19) corresponde al resultado de restar fallecidos y personas recuperadas al total de casos diagnosticados. Las personas recuperadas son casos que tras ser confirmados, ha estado en cuarentena pasando 14 días sin síntomas.

