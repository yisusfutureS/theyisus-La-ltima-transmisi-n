# Análisis e implementación del cambio

## Decisión recibida

El lector puede deshacer su última elección válida. Deben restaurarse la escena y
todas las variables anteriores. Solo hay un nivel: deshacer consume el respaldo
hasta una nueva elección válida. Inicio y reinicio no permiten retroceder. Una
opción inválida no modifica sesión ni respaldo. Desde E4/E5/E6 se vuelve a E3.
Esta decisión sustituye el acuerdo inicial sin retroceso.

## Versión de partida e impacto

La V1 se identifica mediante VERSION y los SHA-256 de evidencias/base_v1.json.
El historial local actual identifica commits V1 y V2; no representa la hora 6.

| Artefacto | Cambio | Evidencia |
|---|---|---|
| RF | Añadir RF12–RF15 | docs/02_requisitos.md |
| Motor | Respaldo único; deshacer; disponibilidad; limpieza en reinicio | src/motor.py |
| Interfaz | Comando :deshacer y mensaje cuando no hay respaldo | src/main.py |
| Cargador y JSON | Contrato conservado; sin campos nuevos | Comparación de huellas V1/V2 |
| Modelos | UC07, respaldo en clase, secuencia de restauración, transiciones desde final | docs/modelos/M02–M05 |
| Backlog | Incorporar B08 | docs/03_proceso.md |
| Pruebas | Añadir U6; extender U5 e I1 | tests/test_motor.py |
| RNF y trazabilidad | Ocho escenarios y referencias al cambio | docs/06_trazabilidad.md; evidencias/ |

## Implementación

elegir valida antes de mutar. Si la elección es válida guarda (_actual,
_variables.copy()), asigna efectos y avanza. deshacer restaura ese par y elimina
el respaldo; no existe rehacer ni pila de estados. reiniciar lo elimina también.
Como las variables son booleanas, una copia simple del dict es suficiente.

## Aceptación y resultados

U6 comprueba restauración exacta, entrada inválida que preserva el respaldo,
segundo intento sin cambios y nueva elección que vuelve a habilitar retroceso.
U5 comprueba inicio/reinicio sin respaldo; I1 comprueba el regreso desde E4/E5/E6.
El ejemplo revisar → investigar → deshacer → continuar muestra en E3 activar sin
verificar y cortar. La demostración registra ese flujo y la restauración desde E5.
Resultados reales en evidencias/ y demo/; no se crea una prueba nueva de resultado
esperado sin ejecutarla.
