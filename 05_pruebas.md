# Plan de pruebas y resultados

| Caso | Entrada | Resultado esperado y aserciones |
|---|---|---|
| U1 | Historia válida y variantes de error | Inicio E1; assertRaisesRegex verifica causa/campo para cada defecto. |
| U2 | revisar, investigar | E3; conoce_origen verdadero; conjunto exacto activar_codigo/cortar. |
| U3 | revisar, continuar, activar_codigo, activar_sin_verificar | Rechazo del ID oculto; no avance; luego E5. |
| U4 | Condición imposible con variables iniciales | Bloqueo verdadero; rechazo de elección; reinicio a E1. |
| U5 | revisar, investigar, reiniciar | E1 y todas las variables iniciales. |
| I1 | JSON real, rutas de E4/E5/E6 y segunda historia | Finales verdaderos y sin avance; segunda historia llega a S5. |
| I2 | Segunda historia, O2; O1/O2; O1/O1; O3/O1 | S3/S4/S5 alcanzables; desde O3, O1 oculta y rechazada. |

## Cobertura de errores

| Categoría | Evidencia |
|---|---|
| Archivo ilegible / estructura incorrecta | U1: ruta inexistente, JSON roto, raíz no objeto. |
| Campo obligatorio ausente | U1: campo titulo ausente. |
| Inicio inexistente | U1: inicio E99. |
| IDs duplicados en su ámbito | U1: escena repetida y opción repetida; I2 admite IDs de opción iguales en escenas distintas. |
| Destino inexistente | U1: destino E99; prueba de consola rechaza antes de jugar. |
| Variable no declarada | U1: condiciones y efectos con variable otra. |
| Valor no booleano | U1: condiciones/efectos con 1 y variable inicial con texto false. |
| Opciones incompatibles con final | U1: no final vacía y final con opciones. |
| No final sin opciones habilitadas | U4 y comprobación de consola. |

RNF02 desglosa la duplicación de escenas y opciones en dos diagnósticos de carga;
el bloqueo se verifica aparte durante ejecución. No se confunden validación
estática y disponibilidad de opciones durante una partida.

## Ejecución reproducible

Desde la raíz: `python -m unittest discover -s tests -v`,
`python herramientas/verificar_rnf.py` y `python herramientas/comprobar_consola.py`.
Resultados reales: evidencias/evidencia_pruebas.txt, evidencia_rnf.json y
evidencia_consola.txt. evidencias/verificacion_zip.txt comprueba el paquete extraído.
No se infiere ausencia de cualquier defecto a partir de esta cobertura.
