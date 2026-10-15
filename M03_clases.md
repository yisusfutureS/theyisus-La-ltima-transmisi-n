# M03 clases

Historia, Escena y Opcion son estructuras conceptuales implementadas como diccionarios JSON; no se afirman clases Python inexistentes. Cargador y Consola representan módulos. Motor sí es una clase Python. escena_actual, variables y bloqueada son propiedades.

```mermaid
classDiagram
    class Historia {
      titulo: str
      inicio: str
      variables: dict
      escenas: list
    }
    class Escena {
      id: str
      texto: str
      final: bool
      opciones: list
    }
    class Opcion {
      id: str
      texto: str
      destino: str
      condiciones: dict
      efectos: dict
    }
    class Motor {
      _historia: dict
      _escenas: dict
      _actual: str
      _variables: dict
      _anterior: tuple_or_None
      puede_deshacer()
      deshacer()
      escena_actual()
      variables()
      opciones_disponibles()
      bloqueada()
      elegir(id)
      reiniciar()
    }
    class Cargador {
      cargar_historia(ruta)
      validar_historia(datos)
    }
    class Consola {
      main()
    }
    Historia "1" *-- "1..*" Escena
    Escena "1" *-- "0..*" Opcion
    Opcion --> Escena : destino por ID
    Motor --> Historia : copia validada
    Consola --> Cargador : carga
    Consola --> Motor : usa
    Motor --> Cargador : valida entrada
```
