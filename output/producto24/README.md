# Descripción
Este producto da cuenta del número de pacientes en hospitalización según el tipo de cama que ocupan: Básica, Media, UTI y UCI. Se concatena la historia de reportes diarios publicados por el Ministerio de Salud del país.

Se entiende por paciente en hospitalización la persona que cumple con los criterios de definición de caso sospechoso con una muestra positiva de SARS-CoV-2 que ha sido ingresado en el sistema integrado y reportado por la Unidad de Gestión Centralizada de Camas (UGCC).

**Nota aclaratoria 1:** El archivo contempla la cantidad de camas hospitalarias ocupadas al día.

**Nota aclaratoria 2:** Previo al 16 de abril, los reportes diarios del Ministerio de Salud no entregaban datos sobre la ocupación de camas de hospitalización.

# Fuente
Reportes diarios publicados períodicamente por el Ministerio de Salud con los datos reportados por la Unidad de Gestión de Camas Críticas. Ver en: https://www.gob.cl/coronavirus/cifrasoficiales/#reportes
# Frecuencia de actualización
Diaria.
# Columnas y Valores
2 archivos con valores separados por coma (csv), el primero corresponde al reporte diario de la cantidad de pacientes en camas Básicas, Media, UCI o en UTI, y el segundo, a la serie de tiempo de los datos anteriores. Contiene los campos 'Tipo de Cama' (con las categorías 'Básicas', 'Media', 'UCI', 'UTI', '[fecha]', donde esta última columna contiene el número de ocupación por día
