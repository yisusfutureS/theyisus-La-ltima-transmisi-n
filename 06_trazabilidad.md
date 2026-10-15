# Matriz de trazabilidad

## Necesidades oficiales y cobertura

Fuente: docs/fuentes/necesidades_oficiales.png.

| ID | Necesidad oficial | Requisitos que la atienden |
|---|---|---|
| N01 | Los escritores necesitan distribuir relatos en archivos independientes y definir dónde y con qué información comienza cada partida. | RF01, RF02 |
| N02 | Los lectores necesitan leer la escena actual y ver únicamente decisiones compatibles con la información obtenida. | RF03, RF16 |
| N03 | Elegir debe producir las consecuencias indicadas en el relato y llevar al destino previsto. Los errores de entrada no deben alterar la partida. | RF04, RF05, RF06 |
| N04 | La experiencia debe recordar durante la partida qué ha ocurrido para que las elecciones posteriores tengan consecuencias coherentes. | RF05, RF06; RF03 utiliza ese estado |
| N05 | El lector necesita reconocer el desenlace y comenzar otra partida sin conservar información de la anterior. | RF07, RF11 |
| N06 | El escritor necesita saber por qué un archivo no es válido antes de que alguien lo juegue. Los errores mínimos se precisan en la sección de validación. | RF08a–RF08i, RF09 (RF08 agrupa validación) |

RF10 atiende además la regla explícita de bloqueo.

## Requisitos, modelos, código y evidencia

Los modelos M01–M05 están en docs/modelos/. Las funciones U/I están en
tests/test_motor.py y su resultado está en evidencias/evidencia_pruebas.txt.

| Requisito | Necesidad / origen | Modelos | Archivos | Verificación localizable |
|---|---|---|---|---|
| RF01 | N01 | M01/M02/M04 | src/cargador.py | tests/test_motor.py: I1/I2 |
| RF02 | N01 | M02/M03/M04/M05 | src/motor.py; src/main.py | tests/test_motor.py: U5 |
| RF03 | N02, N04 | M02/M03/M04/M05 | src/motor.py; src/main.py | tests/test_motor.py: U2/U3 |
| RF04 | N03 | M02/M03/M04/M05 | src/motor.py; src/main.py | tests/test_motor.py: U3 |
| RF05 | N03, N04 | M02/M03/M04/M05 | src/motor.py; src/main.py | tests/test_motor.py: U2/I1 |
| RF06 | N03, N04 | M02/M03/M04/M05 | src/motor.py; src/main.py | tests/test_motor.py: I1 |
| RF07 | N05 | M02/M03/M04/M05 | src/motor.py; src/main.py | tests/test_motor.py: I1 |
| RF08 | N06 | M01/M02/M04 | src/cargador.py | tests/test_motor.py: U1 |
| RF09 | N06 | M01/M02/M04 | src/cargador.py | tests/test_motor.py: U1; consola |
| RF10 | Regla explícita de bloqueo de la guía; complementa N02/N05 | M02/M03/M04/M05 | src/motor.py; src/main.py | tests/test_motor.py: U4; consola |
| RF11 | N05 | M02/M03/M04/M05 | src/motor.py; src/main.py | tests/test_motor.py: U5 |
| RF16 | N02 | M01/M02/M04 | src/main.py; motor.py:escena_actual | demo/transcripcion_consola.txt |
| RNF01 | N01 | M01/M03; arquitectura | datos/; src/ | evidencias/evidencia_rnf.json:RNF01 |
| RNF02 | N06 | M02/M04 | src/cargador.py; main.py | evidencias/evidencia_rnf.json:RNF02.casos |
| RNF03 | N02–N05 | M04/M05 | tests/; src/ | evidencias/evidencia_rnf.json:RNF03.ejecuciones |

## Detalle de RF08

RF08a–RF08i se vinculan individualmente con N06, M02/M04,
src/cargador.py:validar_historia (RF08a también cargar_historia), y sus variantes
U1 identificadas por datos y mensajes en tests/test_motor.py. Resultado conjunto
en evidencias/evidencia_pruebas.txt; diagnósticos RNF02 en evidencia_rnf.json.
