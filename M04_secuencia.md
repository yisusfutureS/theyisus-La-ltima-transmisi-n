# M04 secuencia



```mermaid
sequenceDiagram
    actor L as Lector
    participant UI as main.py
    participant C as cargador.py
    participant M as Motor
    L->>UI: Ejecutar con ruta JSON
    UI->>C: cargar_historia(ruta)
    alt Contenido inválido
        C-->>UI: ErrorHistoria con causa y campo
        UI-->>L: Mensaje; no se crea partida
    else Contenido válido
        C-->>UI: historia validada
        UI->>M: Motor(historia)
        M->>C: validar_historia(historia)
        M->>M: reiniciar()
        UI->>M: escena_actual / opciones_disponibles()
        M-->>UI: escena y opciones habilitadas
        UI-->>L: Presentar información
        L->>UI: ID de opción
        UI->>M: elegir(id)
        M->>M: Buscar entre opciones habilitadas
        alt ID inválido o no habilitado
            M-->>UI: ErrorEleccion sin modificar sesión
            UI-->>L: Mostrar error y continuar
        else Elección válida
            M->>M: Copiar escena y variables en respaldo único
            M->>M: Aplicar efectos y cambiar destino
            UI->>M: Consultar escena y opciones nuevas
            UI-->>L: Nueva escena, final o bloqueo
        end
    end
    opt Usuario solicita deshacer, incluso desde final
        L->>UI: :deshacer
        UI->>M: deshacer()
        alt Existe respaldo
            M->>M: Restaurar escena y todas las variables
            M->>M: Consumir respaldo
            M-->>UI: True
        else No existe respaldo
            M-->>UI: False sin cambios
        end
        UI-->>L: Estado restaurado o mensaje
    end
```
