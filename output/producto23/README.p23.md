[data product 23: Pacientes críticos](output/producto23): Archivo que da cuenta de los pacientes hospitalizados en la Unidad de Cuidados Intensivos (UCI) y se encuentran en situación crítica. Este producto concatena la historia de los reportes diarios publicados por el Ministerio de Salud del país.

Se entiende por paciente hopitalizado a aquel que cumple con los criterios de definición de caso sospechoso con una muestra positiva de SARS-CoV2, y que ha sido ingresado en el sistema integrado hospitalario.

**Nota aclaratoria**: Previo al 26 de marzo del 2020, los reportes diarios del Ministerio de Salud no entregaban datos de hospitalización de pacientes en UCI en situación crítica.


2 archivos con valores separados por coma (csv), el primero corresponde al reporte diario de la cantidad de pacientes críticos, y el segundo, a la serie de tiempo de los datos anteriores. Contiene los campos 'Pacientes críticos', '[fecha]', donde esta última columna contiene el número reportado diariamente.
