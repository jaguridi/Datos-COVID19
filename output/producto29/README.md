# DP29 - Cuarentenas Activas e Históricas: Descripción
Set de 3 archivos en formato csv que contiene la identificación y características de las zonas de cuarentena establecidas por el Plan de Acción por Coronavirus del Gobierno de Chile.

Las zonas de cuarentena se establecen como una medida sanitaria en una extensión territorial definida que implica que las personas deben permanecer en sus domicilios habituales hasta que la autoridad disponga lo contrario.

Los criterios para la definir la cuarentena son:

- Velocidad de Propagación de la Enfermedad
- Densidad de casos por km2
- Perfil etáreo de la población del territorio (adultos mayores y personas con enfermedades crónicas)
- Vulnerabilidad Social

Los archivos incluidos en el presente DP son:
- Cuarentenas-Activas.csv (Cuarentenas actualmente vigentes y futuras)
- Cuarentenas-Historicas.csv (Cuarentenas ya cumplidas incluyendo cambios dentro de una misma comuna)
- Cuarentenas-Totales.csv (Suma de cuarentenas vigentes e históricas)

# Columnas y valores

- Nombre: Nombre descriptivo de la zona de cuarentena.
- Estado: Valor codificado para estado de la cuarentena: Activa, No Activa, Futura, Sin Información.
- Alcance: Valor codificado para el alcance territorial de la cuarentena Comuna completa, Área Urbana Completa, Área Rural Completa, Sector Específico.
- FInicio: Fecha y hora de inicio en tiempo UTC.
- FTermino: Fecha y hora de término en tiempo UTC.
- Cut_Com: Código Único Territorial de comuna asociada.
- Detalle: Observaciones adicionales al alcance de la cuarentena.
- Shape_Area: Superficie en m2.
- Shape_Length: Perímetro en m.

# Fuente
Plan de Acción del Gobierno de Chile para el COVID-19. Ver en: https://www.gob.cl/coronavirus/plandeaccion/

API Externa de Respaldo de Servicios para consulta. https://covid19.soporta.cl/datasets/0b944d9bf1954c71a7fae96bdddee464_1?geometry=-105.067%2C-44.515%2C-45.784%2C-32.531

# Frecuencia de actualización

Dos veces a la semana: días martes para cambios en áreas, días jueves para cambio de estado de las cuarentenas.

# Notas aclaratorias

**Nota aclaratoria 1:** La cartografía de delimitación de cuarentenas es de caracter referencial cuyos límites son obtenidos en base a fuentes oficiales para límites comunales y áreas urbanas y pueden ser encontradas en formato GeoJSON [aqui](input/Cuarentenas).