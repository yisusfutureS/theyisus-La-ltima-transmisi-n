"""Motor del alcance inicial: elecciones, estado, finales y reinicio."""
from copy import deepcopy
from cargador import validar_historia

class ErrorEleccion(ValueError):
    pass

class Motor:

    def __init__(self, historia):
        self._historia = validar_historia(historia)
        self._escenas = {e['id']: e for e in self._historia['escenas']}
        self.reiniciar()

    @property
    def escena_actual(self):
        return deepcopy(self._escenas[self._actual])

    @property
    def variables(self):
        return self._variables.copy()

    def opciones_disponibles(self):
        return [deepcopy(o) for o in self._escenas[self._actual]['opciones'] if all((self._variables[n] == v for n, v in o['condiciones'].items()))]

    @property
    def bloqueada(self):
        return not self._escenas[self._actual]['final'] and (not self.opciones_disponibles())

    def elegir(self, identificador):
        opcion = next((o for o in self.opciones_disponibles() if o['id'] == identificador), None)
        if opcion is None:
            raise ErrorEleccion(f'Opción inexistente o no habilitada: {identificador}')
        self._variables.update(opcion['efectos'])
        self._actual = opcion['destino']

    def reiniciar(self):
        self._actual = self._historia['inicio']
        self._variables = self._historia['variables'].copy()
