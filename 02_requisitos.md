# 2. Requisitos de la versión final

Las necesidades oficiales N01–N06 se transcriben de la imagen suministrada
por el estudiante. La correspondencia completa está al final de este documento
y en docs/06_trazabilidad.md.

## Requisitos funcionales

| ID | Comportamiento | Criterio de aceptación |
|---|---|---|
| RF01 | Cargar una narración desde la ruta JSON recibida. | Al cargar ambas historias incluidas se crean partidas sin modificar código; I1. |
| RF02 | Inicializar la escena y las variables con los valores del archivo. | Una nueva partida comienza en E1 con ambas variables falsas; U5. |
| RF03 | Mostrar solamente opciones cuyas condiciones de igualdad se cumplan todas. | E3 ofrece exactamente activar con código y cortar cuando conoce_origen es verdadero; si es falso, activar sin verificar y cortar; U2/U3. |
| RF04 | Rechazar IDs inexistentes o de opciones no habilitadas. | Intentar activar_codigo sin conocer el origen produce ErrorEleccion y deja escena y variables intactas; U3. |
| RF05 | Asignar todos los efectos de la elección válida. | Investigar establece conoce_origen verdadero y activar establece confia_en_la_voz verdadero; U2 e I1. |
| RF06 | Avanzar al destino de una elección válida conservando el resto del estado. | Revisar lleva a E2; investigar a E3; activar o cortar al final correspondiente; I1. |
| RF07 | Reconocer las escenas finales y no ofrecer avance desde ellas. | E4, E5 y E6 tienen final verdadero y cero opciones disponibles; I1. |
| RF08 | Rechazar historias que incumplan estructura, referencias, unicidad o tipos. | U1 rechaza las categorías de carga exigidas, incluido destino E99; no se crea sesión jugable. |
| RF09 | Informar errores de carga con causa y localización identificable. | Cada categoría de RNF02 informa campo, ID o archivo y motivo; main muestra el mensaje sin traceback de aplicación. |
| RF10 | Informar cuando una escena no final no tiene opciones habilitadas. | U4 confirma bloqueada verdadero; la interfaz muestra el bloqueo y ofrece reiniciar. |
| RF11 | Reiniciar en el estado original. | Después de investigar, reiniciar devuelve E1 y ambas variables falsas; U5. |

## Requisitos no funcionales

| ID | Umbral | Procedimiento y evidencia |
|---|---|---|
| RNF01, modificabilidad | Completar la segunda historia con cero cambios en motor, cargador e interfaz. | Comparar SHA-256 antes y después; herramientas/verificar_rnf.py, evidencias/evidencia_rnf.json:RNF01. |
| RNF02, claridad de errores | Nueve variantes de carga con causa y ubicación identificable. | Introducir cada defecto y comprobar mensajes; evidencias/evidencia_rnf.json:RNF02. |
| RNF03, confiabilidad | Tres ejecuciones de ocho escenarios con cero fallos y errores. | U1–U6, I1 e I2; evidencias/evidencia_rnf.json:RNF03. |

## Tres preguntas, respuestas o supuestos

1. ¿Se permite volver a una escena anterior? Existe conflicto entre la escritora
   y el diseñador. La guía establece no implementar retroceso en el alcance inicial;
   la solicitud de cambio lo reemplaza por un retroceso de una elección válida.
2. ¿Cómo se combinan varias condiciones? Supuesto: todas deben cumplirse (Y lógico).
   Un objeto de condiciones vacío, representada por {}, habilita siempre la opción.
3. ¿Qué sucede ante un bloqueo? La guía exige informar y permitir reiniciar.

## Trazabilidad

RF01 y RF08–RF09: cargador.py, U1 e I1. RF02 y RF11: Motor.reiniciar, U5.
RF03: Motor.opciones_disponibles, U2/U3. RF04–RF06: Motor.elegir, U2/U3/I1.
RF07: escenas finales e interfaz, I1. RF10: Motor.bloqueada e interfaz, U4.
Los cinco modelos incluidos se enlazan en docs/06_trazabilidad.md.

## Requisitos del cambio

| ID | Comportamiento | Aceptación |
|---|---|---|
| RF12 | Deshacer restaura exactamente escena y todas las variables previas a la última elección válida. | Investigar y deshacer devuelve E2 con conoce_origen falso; I1 verifica también regreso desde E4, E5 y E6; U6/I1. |
| RF13 | Permitir un solo nivel de retroceso, renovado por una elección válida posterior. | Tras deshacer, otro intento devuelve falso y no cambia nada; continuar después habilita otro retroceso; U6. |
| RF14 | Mantener el respaldo ante entradas inválidas. | Intentos inexistentes o no habilitados no sustituyen el respaldo; aún se puede deshacer investigar; U6. |
| RF15 | Iniciar sin retroceso y eliminarlo al reiniciar. | Al crear la partida y después de reiniciar puede_deshacer es falso; U5/U6. |

## Descomposición atómica de RF08

RF08 agrupa la validación; las siguientes unidades son requisitos verificables
por separado y mantienen el identificador padre para lectura de la matriz.

| ID | Comportamiento | Aceptación |
|---|---|---|
| RF08a | Rechazar lectura o estructura incorrecta. | U1 rechaza archivo ausente, JSON roto y raíz lista. |
| RF08b | Rechazar campos obligatorios ausentes. | U1 rechaza titulo ausente y nombra el campo. |
| RF08c | Rechazar inicio inexistente. | U1 rechaza inicio E99. |
| RF08d | Rechazar IDs de escenas duplicados. | U1 rechaza una segunda E1. |
| RF08e | Rechazar IDs de opciones duplicados dentro de una escena. | U1 rechaza revisar repetido en E1; I2 admite IDs iguales en escenas distintas. |
| RF08f | Rechazar destinos inexistentes. | U1 rechaza destino E99; consola no abre sesión. |
| RF08g | Rechazar variables no declaradas en condiciones o efectos. | U1 rechaza variable otra en ambos campos. |
| RF08h | Rechazar valores no booleanos en variables, condiciones o efectos. | U1 rechaza texto false e integer 1. |
| RF08i | Rechazar cantidad de opciones incompatible con final. | U1 rechaza final con opciones y no final vacía. |


## Presentación de la escena actual

| ID | Comportamiento | Criterio de aceptación |
|---|---|---|
| RF16 | Presentar el texto de la escena actual al iniciar y después de cada elección válida o reinicio. | La consola muestra el ID y texto de la escena vigente; main.py lee escena_actual y lo imprime en cada iteración. Evidencia: demo/transcripcion_consola.txt. |

RF16 explicita un comportamiento ya implementado en ambas versiones, sin cambiar
el programa. RF12–RF15 se reservan para la solicitud de cambio y solo aplican a V2.

## Correspondencia con las necesidades oficiales

| ID | Necesidad oficial | Requisitos que la atienden |
|---|---|---|
| N01 | Los escritores necesitan distribuir relatos en archivos independientes y definir dónde y con qué información comienza cada partida. | RF01, RF02 |
| N02 | Los lectores necesitan leer la escena actual y ver únicamente decisiones compatibles con la información obtenida. | RF03, RF16 |
| N03 | Elegir debe producir las consecuencias indicadas en el relato y llevar al destino previsto. Los errores de entrada no deben alterar la partida. | RF04, RF05, RF06 |
| N04 | La experiencia debe recordar durante la partida qué ha ocurrido para que las elecciones posteriores tengan consecuencias coherentes. | RF05, RF06; RF03 utiliza ese estado |
| N05 | El lector necesita reconocer el desenlace y comenzar otra partida sin conservar información de la anterior. | RF07, RF11 |
| N06 | El escritor necesita saber por qué un archivo no es válido antes de que alguien lo juegue. Los errores mínimos se precisan en la sección de validación. | RF08a–RF08i, RF09 (RF08 agrupa validación) |

RF10 deriva de la regla adicional de bloqueo indicada en la guía.
RF12–RF15 derivan de la solicitud de cambio, no de una redefinición de N01–N06.
