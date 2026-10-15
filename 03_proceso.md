# Proceso y agilidad — V1

Responsable de la entrega: Jesus Espitia. Proyecto preparado con asistencia de
Codex; el alcance de la ayuda y los aportes se declaran en docs/08_aportes_fuentes.md.

## Proceso y alternativa

Proceso incremental con tablero Kanban. Se prepara una base funcional, se ejecutan
pruebas y se revisan resultados antes del siguiente incremento. Alternativa:
cascada; se descarta porque el ejercicio anuncia un cambio dentro del plazo.

## Backlog

| ID | Resultado | Prioridad | Dependencias | Evidencia |
|---|---|---|---|---|
| B01 | Problema y requisitos | Alta | Guía y rúbrica | docs/01_problema.md; 02_requisitos.md |
| B02 | Contrato y cargador | Crítica | B01 | src/cargador.py; U1 |
| B03 | Motor y consola | Crítica | B02 | src/motor.py; main.py; U2–U5 |
| B04 | Dos historias | Alta | B03 | datos/; I1/I2 |
| B05 | Cinco modelos y arquitectura | Alta | B01–B03 | docs/modelos/; 04_arquitectura.md |
| B06 | Pruebas, RNF y evidencia | Crítica | B02–B04 | evidencias/ |
| B07 | Documentación, demostración y ZIP | Alta | B05/B06 | README; demo/ |

## Tablero y evolución real

`evidencias/tablero_inicio.json` registra el inicio de esta preparación;
`evidencias/tablero_final.json` registra el resultado verificado. Son estados
locales fechados de esta sesión, no capturas inventadas de GitHub ni de la hora 6.
Al publicar, trasladar las tareas al tablero: Por hacer → En progreso → En revisión
→ Terminado. Los pendientes humanos permanecen En revisión.

## Prácticas

1. Separación de responsabilidades aplicada en cuatro componentes: contenido,
   validación, sesión e interfaz; demostrada al ejecutar otra historia.
2. Regresión automatizada aplicada al comprobar condiciones, efectos, errores,
   reinicio y recorridos completos tras cada cambio.

Alternativa descartada: verificación exclusivamente manual, porque no cubre
de forma repetible las entradas inválidas y las variables ocultas del estado.

## Definición de terminado

Requisito con aceptación, implementación consistente, pruebas que pasan, evidencia
conservable, documentación/modelos/trazabilidad actualizados y revisión del responsable.
Para entregar: descomprimir y ejecutar desde el README, nombres completos y
aportes confirmados, video accesible y comprobante de publicación del aula.

## Aprendizaje y mejora

Durante la preparación previa, un temporal de pruebas no pudo escribirse por
permisos del entorno. La corrección usa TemporaryDirectory dentro del proyecto.
Acción de mejora: repetir pruebas desde el ZIP extraído, con archivos temporales
controlados; la revisión final registra esa ejecución.

## Revisión del responsable

Jesus Espitia confirmó la revisión personal del informe y el código, la ejecución
de la aplicación y las pruebas y la comprobación de funcionamiento. El tablero
final registra esta confirmación; los pendientes externos permanecen separados.
