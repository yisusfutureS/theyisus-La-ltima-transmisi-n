"""Interfaz de consola; ejecutar: python src/main.py datos/la_ultima_transmision.json"""
import sys
from cargador import cargar_historia, ErrorHistoria
from motor import Motor, ErrorEleccion


def main():
    if len(sys.argv) != 2:
        print('Uso: python src/main.py archivo.json')
        return 1
    try:
        motor = Motor(cargar_historia(sys.argv[1]))
    except ErrorHistoria as error:
        print(f'No se puede iniciar: {error}')
        return 1
    while True:
        escena = motor.escena_actual
        print(f"\n[{escena['id']}] {escena['texto']}")
        if escena['final']:
            print('FIN. Puedes deshacer, reiniciar o salir.')
        elif motor.bloqueada:
            print('Bloqueo: no hay opciones habilitadas. Puedes reiniciar.')
        for opcion in motor.opciones_disponibles():
            print(f"  {opcion['id']}: {opcion['texto']}")
        print('Comandos: :deshacer, :reiniciar, :salir')
        try:
            entrada = input('> ').strip()
        except (EOFError, KeyboardInterrupt):
            print('\nSesión terminada.')
            return 0
        if entrada == ':salir':
            return 0
        if entrada == ':reiniciar':
            motor.reiniciar()
        elif entrada == ':deshacer':
            if not motor.deshacer():
                print('No hay una decisión disponible para deshacer.')
        else:
            try:
                motor.elegir(entrada)
            except ErrorEleccion as error:
                print(error)


if __name__ == '__main__':
    sys.exit(main())
