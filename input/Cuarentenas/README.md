# Descripción
Archivo en bruto en formato GeoJSON que contiene la delimitación de las zonas de cuarentena establecidas por el Plan de Acción por Coronavirus del Gobierno de Chile

Las zonas de cuarentena se establecen como una medida sanitaria en una extensión territorial definida que implica que las personas deben permanecer en sus domicilios habituales hasta que la autoridad disponga lo contrario.

Los criterios para la definir la cuarentena son:
- Velocidad de Propagación de la Enfermedad
- Densidad de casos por km2
- Perfil etáreo de la población del territorio (adultos mayores y personas con enfermedades crónicas)
- Vulnerabilidad Social

**Nota:** La cartografía de delimitación de cuarentenas es de caracter referencial cuyos límites son obtenidos en base a fuentes oficiales para límites comunales y áreas urbanas.

# Fuente
Plan de Acción del Gobierno de Chile para el COVID-19. Ver en:
https://www.gob.cl/coronavirus/plandeaccion/

API Externa de Respaldo de Servicios para consulta.
https://covid19.soporta.cl/datasets/0b944d9bf1954c71a7fae96bdddee464_1?geometry=-75.445%2C-34.423%2C-64.991%2C-32.822

# Frecuencia de Actualización
Dos veces a la semana: días martes para cambios en áreas, días jueves para cambio de estado de las cuarentenas.

# Columnas y valores
El archivo posee una estructura GeoJSON (https://geojson.org/) con las siguientes propiedades:
- Nombre: Nombre descriptivo de la zona de cuarentena.
- Estado: Valor codificado para estado de la cuarentena [1] Activa, [2] No-Activa, [3] Futura, [99] Sin Información.
- Alcance: Valor codificado para el alcance territorial de la cuarentena [1] Comuna completa, [2] Área Urbana Completa, [3] Área Rural Completa, [4] Sector Específico.
- FInicio: Fecha y hora de inicio en formato EPOCH (milisegundos).
- FTermino: Fecha y hora de término en formato EPOCH (milisegundos).
- Cut_Com: Código Único Territorial de comuna asociada.
- Detalle: Observaciones adicionales al alcance de la cuarentena.
- Shape_Area: Superficie en m2.
- Shape_Length: Perímetro en m2.