# La última transmisión — V2

**Responsable de la entrega: Jesus Espitia.**

Motor de ficción interactiva en Python. V2 incluye deshacer una última decisión válida, restaurando escena y variables.
Contenido y reglas se leen de JSON; no hay rutas de esta historia codificadas en el motor.

## Instalación y ejecución

Requiere Python 3.10 o posterior; no hay dependencias externas para jugar, probar
o repetir mediciones. Descomprime y abre una terminal junto a este README.
En Windows puedes usar py en lugar de python.

```text
python src/main.py datos/la_ultima_transmision.json
python src/main.py datos/segunda_historia.json
python -m unittest discover -s tests -v
python herramientas/verificar_rnf.py
python herramientas/comprobar_consola.py
python herramientas/demostrar.py
```

Escribe un ID visible. Comandos: :deshacer, :reiniciar y :salir.
Una entrada inválida produce un mensaje y permite continuar. En un final puedes
deshacer, reiniciar o salir. Un bloqueo informa que no hay opciones habilitadas.

## Documentación para leer

| Punto | Archivo |
|---|---|
| Informe completo | [INFORME.md](INFORME.md) |
| Problema, actores, alcance, riesgos y calidad | [01](docs/01_problema.md) |
| RF, RNF, aceptación y preguntas | [02](docs/02_requisitos.md) |
| Proceso, backlog, tablero y terminado | [03](docs/03_proceso.md) |
| Cinco modelos | [Modelos](docs/modelos/README.md) |
| Arquitectura y decisiones | [04](docs/04_arquitectura.md) |
| Plan y resultados de pruebas | [05](docs/05_pruebas.md) |
| Trazabilidad | [06](docs/06_trazabilidad.md) |
| Análisis del cambio | [07](docs/07_cambio.md) |
| Aportes y fuentes | [08](docs/08_aportes_fuentes.md) |
| Revisión de la rúbrica y pendientes | [09](docs/09_revision_final.md) |

## Historias y rutas

E4: revisar → investigar → activar_codigo. E5: revisar → continuar →
activar_sin_verificar. E6: revisar → investigar → cortar.
Segunda historia, El último algoritmo: O2 lleva a S3; O1/O2 a S4; O1/O1 a S5.
Llegar a S2 mediante O3 oculta O1.

## Formato JSON

Raíz: titulo, inicio, variables y escenas. Escena: id, texto, final y opciones.
Opción: id, texto, destino, condiciones y efectos. Textos e IDs: cadenas no vacías.
Variables, condiciones y efectos: objetos de valores booleanos; todas las
condiciones deben cumplirse y {} habilita siempre. Los efectos asignan valores.
IDs de escenas únicos; IDs de opciones únicos dentro de una escena. Inicio y
destinos existentes. Final: cero opciones; no final: al menos una definida.
El contenido inválido se rechaza antes de jugar. Guarda JSON en UTF-8.
Para otra historia: python src/main.py datos/otra_historia.json.

## Evidencia y demostración

8 escenarios automatizados correctos; tres RNF verificados localmente.
Resultados en evidencias/. Demo en demo/demostracion.avi: video sin audio que
presenta salidas reales de ejecución con texto explicativo.
También se incluye una vista HTML y transcripción para leerla sin reproductor AVI.

