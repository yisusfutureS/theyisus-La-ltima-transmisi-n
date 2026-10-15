# 1. Problema, actores, alcance y riesgos

## Problema

El colectivo necesita ofrecer ficción interactiva cuyas decisiones cambien el
desarrollo y el final. La escritora debe editar contenido sin modificar Python,
y la coordinadora necesita detectar errores antes de abrir una partida.
El motor interpreta escenas, condiciones y efectos desde archivos JSON.

## Actores e interesados

- Lector: consulta escenas, elige opciones, alcanza finales y reinicia.
- Escritora: edita el JSON fuera del programa; no existe editor visual.
- Diseñador: define condiciones y consecuencias.
- Coordinadora: necesita funcionamiento verificable y errores identificables.
- Equipo desarrollador: implementa, verifica y mantiene la solución.

## Alcance

Carga y validación JSON, inicio, presentación de escenas y opciones habilitadas,
elecciones válidas, rechazo de entradas inválidas, efectos booleanos, finales,
bloqueos y reinicio. Las historias se intercambian sin modificar el motor.
Incluye deshacer una última elección válida. No incluye persistencia, cuentas, internet, base de datos ni multimedia.

## Conflicto pendiente

La escritora quiere permitir retroceder siempre y el diseñador prefiere decisiones
irreversibles. Pregunta: ¿debe permitirse retroceder y con qué consecuencias sobre
las variables? El acuerdo provisional explícito de la guía es no implementar
retroceso en el alcance inicial. La solicitud posterior autoriza un nivel de retroceso y reemplaza este acuerdo.

## Dos riesgos

| Riesgo | Probabilidad / impacto | Mitigación |
|---|---|---|
| Referencias o tipos incorrectos en el contenido. | Media / alto. | Validar antes de iniciar y localizar el defecto en el mensaje; U1. |
| Una opción oculta se ejecuta enviando su ID directamente. | Media / alto. | Validar en el motor contra las opciones habilitadas; U3. |

## Calidad y responsabilidad

Prioridad 1: confiabilidad de estado y elecciones, porque un error altera la
historia. Prioridad 2: claridad de errores, porque el contenido lo edita una
persona no programadora. Prioridad 3: modificabilidad, para publicar otra historia
sin editar el motor. Los umbrales están en RNF01–RNF03.

Se decide presentar resultados reales, declarar pendientes y uso de IA, y no
atribuir al grupo aportes, fechas o evidencias que no puedan comprobarse.
