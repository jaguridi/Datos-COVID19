# DP22 - Hospitalizados por grupo de edad: Descripción
Este producto, que consiste de varios archivos, da cuenta del número acumulado del total de pacientes hospitalizados por rango de edad y género. También da cuenta del número acumulado de pacientes internados en la Unidad de Cuidados Intensivos (UCI) por rango de edad. Se concatena la historia de los informes de Situación Epidemiológica publicados por el Ministerio de Salud del país.

Se entiende por paciente en hospitalización la persona que cumple con los criterios de definición de caso sospechoso con una muestra positiva de SARS-CoV-2 que ha sido ingresado en el sistema integrado y reportado por EPIVIGILA.

# Columnas y valores
El archivo HospitalizadosEtario_Acumulado.csv contiene las columnas 'Grupo de edad','Sexo' y una serie de columnas con '[Fecha]', donde para cada fila con rango etareo (en bloques de 15 años), se indica por fecha la cantidad acumulada de hospitalizados por género. En el archivo HospitalizadosUCI_Acumulado.csv está la columa 'Grupo de edad' y una serie de columnas con '[Fecha]', donde para cada fila con rango etareo (en bloques distintos al primero), se reportan los hospitalizados UCI acumulados. Este último no tiene desglose por género. Cada archivo tiene una versión traspuesta (serie de tiempo) con el sufijo "\_T". Existe una versión adicional con el sufijo '\_Post20200422' debido a un cambio en los rangos etareos (con sus respectivas versiones en series de tiempo). 

# Fuente
Informes de Situación Epidemiológica publicados períodicamente por el departamento de Epidemiología del Ministerio de Salud con los datos reportados por EPIVIGILA. Ver en: http://epi.minsal.cl/informes-covid-19/
 
# Frecuencia de actualización
Actualización diaria.

# Notas aclaratorias

**Nota aclaratoria 1:** El archivo contempla el número acumulado de pacientes hospitalizados.

**Nota aclaratoria 2:** Previo al 23 de marzo del 2020, los informes de situación Epidemiológica del Ministerio de Salud no entregaban datos sobre la distribución del número de pacientes hospitalizados por rango etario.

**Nota aclaratoria 3:** Los informes de Situación Epidemiológica con fecha de publicación posterior al 21 de abril presentan un cambio en los rangos etarios. Por esta razón, hay dos escalas para los dichos rangos.

**Nota aclaratoria 4:** Los informes de situación Epidemiológica del Ministerio de Salud se publican con fecha del día de corte. Los datos en este repositorio cotejan las fechas indicadas en el texto de la fuente utilizada con las dadas en el reporte diario e informe Epidemiológico del Ministerio de Salud.

