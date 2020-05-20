# DP24 - Hospitalización de pacientes COVID-19 en sistema integrado: Descripción
Este producto da cuenta del número de pacientes en hospitalización con diagnóstico COVID-19 según el tipo de cama que ocupan: Básica, Media, UTI y UCI. Se concatena la historia de reportes diarios publicados por el Ministerio de Salud del país.

Se entiende por paciente en hospitalización la persona que cumple con los criterios de definición de caso sospechoso con una muestra positiva de SARS-CoV-2 que ha sido ingresado en el sistema integrado y reportado por la Unidad de Gestión Centralizada de Camas (UGCC).

# Columnas y valores
El archivo CamasHospital_Diario.csv, corresponde al reporte diario de la cantidad de pacientes en camas (Básica, Media, UCI o en UTI). Contiene las columnas 'Tipo de Cama', y una serie de columnas '[Fecha]', donde estas contiene el número de ocupación por día, por tipo de cama. El archivo CamasHospital_Diario_T.csv es la versión traspuesta (serie de tiempo) del primer archivo. Todos estos valores están separados entre sí por comas (csv).

# Fuente
Reportes diarios publicados períodicamente por el Ministerio de Salud con los datos reportados por la Unidad de Gestión de Camas Críticas. Ver en: https://www.gob.cl/coronavirus/cifrasoficiales/#reportes

# Frecuencia de actualización
Actualización diaria.

# Notas aclaratorias

**Nota aclaratoria 1:** El archivo contempla la cantidad de camas hospitalarias ocupadas al día.

**Nota aclaratoria 2:** Previo al 16 de abril, los reportes diarios del Ministerio de Salud no entregaban datos sobre la ocupación de camas de hospitalización.
