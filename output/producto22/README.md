# Descripción
Este producto da cuenta del número acumulado del total de pacientes hospitalizados por rango de edad y género. También, en otro archivo, da cuenta del número acumulado de pacientes internados en la Unidad de Cuidados Intensivos (UCI) por rango de edad. Se concatena la historia de los informes de Situación Epidemiológica publicados por el Ministerio de Salud del país.

Se entiende por paciente en hospitalización la persona que cumple con los criterios de definición de caso sospechoso con una muestra positiva de SARS-CoV-2 que ha sido ingresado en el sistema integrado y reportado por EPIVIGILA.

*Nota aclaratoria 1:* El archivo contempla el número acumulado de pacientes hospitalizados.

*Nota aclaratoria 2:* Previo al 23 de marzo del 2020, los informes de situación Epidemiológica del Ministerio de Salud no entregaban datos sobre la distribución del número de pacientes hospitalizados por rango etario.

*Nota aclaratoria 3:* Los informes de Situación Epidemiológica con fecha de publicación posterior al 21 de abril presentan un cambio en los rangos etarios. Por esta razón, los archivos se publican con el sufijo '_Post20200422'

# Fuente
Informes de Situación Epidemiológica publicados períodicamente por el departamento de Epidemiología del Ministerio de Salud con los datos reportados por EPIVIGILA. Ver en: http://epi.minsal.cl/informes-covid-19/
 
# Frecuencia de actualización
Diaria.

# Columnas y Valores
2 archivos con valores separados por coma (csv), el primero corresponde al reporte de hospitalizados por grupo de edad, y el segundo, a la serie de tiempo de los datos anteriores. Contiene los campos 'Grupo de edad', '[fecha]', donde esta última columna contiene el número de 'Hospitalizados' reportados acumulados como resultado de la investigación epidemiológica desglosado además por género.

2 archivos con valores separados por coma (csv) con formato similar a los anteriores, pero correspondiente a los pacientes internados en la Unidad de Cuidados Intensivos. Estos archivos no tienen deglose por género.

4 archivos que contienen los campos de los archivos anteriores, pero con fecha posterior al 21 de abril del 2020. Estos archivos tienen rangos etarios distintos a los publicados antes de esta fecha.
