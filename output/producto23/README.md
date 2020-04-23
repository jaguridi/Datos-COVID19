# Descripción
Este producto da cuenta del número de pacientes hospitalizados en la Unidad de Cuidados Intensivos (UCI) y se consideran en situación médica crítica. Se concatena la historia de reportes diarios publicados por el Ministerio de Salud del país.

Se entiende por paciente en hospitalización la persona que cumple con los criterios de definición de caso sospechoso con una muestra positiva de SARS-CoV-2 que ha sido ingresado en el sistema integrado y reportado por la Unidad de Gestión Centralizada de Camas (UGCC).

*Nota aclaratoria 1:* El archivo contempla el número de pacientes internados en UCI en condición crítica, reportado al día.

*Nota aclaratoria 2:* Previo al 23 de marzo del 2020, los reportes diarios del Ministerio de Salud no entregaban datos sobre el número de pacientes en UCI en situación crítica.

# Fuente
Reportes diarios publicados períodicamente por el Ministerio de Salud con los datos reportados por la Unidad de Gestión de Camas Críticas. Ver en: https://www.gob.cl/coronavirus/cifrasoficiales/#reportes
# Frecuencia de actualización
Diaria.

# Columnas y Valores
2 archivos con valores separados por coma (csv), el primero corresponde al reporte diario de la cantidad de pacientes críticos, y el segundo, a la serie de tiempo de los datos anteriores. Contiene los campos 'Pacientes críticos', '[fecha]', donde esta última columna contiene el número reportado diariamente.
