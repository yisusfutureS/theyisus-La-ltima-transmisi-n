"""Mediciones locales reproducibles; genera evidencia sin servicios externos."""
import hashlib
import io
import json
import platform
import unittest
from contextlib import redirect_stdout
from copy import deepcopy
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from cargador import cargar_historia, validar_historia, ErrorHistoria
from motor import Motor

RAIZ = Path(__file__).resolve().parents[1]


def huellas():
    return {n: hashlib.sha256((RAIZ / "src" / n).read_bytes()).hexdigest()
            for n in ['motor.py', 'cargador.py', 'main.py']}


def main():
    antes = huellas()
    motor = Motor(cargar_historia(RAIZ / 'datos/segunda_historia.json'))
    motor.elegir('O1')
    motor.elegir('O1')
    modificabilidad = motor.escena_actual['final'] and antes == huellas()
    datos = cargar_historia(RAIZ / 'datos/la_ultima_transmision.json')
    casos = []
    def caso(nombre, esperado, modificar):
        copia = deepcopy(datos)
        modificar(copia)
        casos.append((nombre, esperado, copia))
    caso('campo ausente', ['titulo', 'ausente'], lambda d: d.pop('titulo'))
    caso('inicio inexistente', ['inicio', 'E99'], lambda d: d.update(inicio='E99'))
    caso('escena duplicada', ['E1', 'repetido'], lambda d: d['escenas'].append(deepcopy(d['escenas'][0])))
    caso('opción duplicada', ['revisar', 'repetido'], lambda d: d['escenas'][0]['opciones'].append(deepcopy(d['escenas'][0]['opciones'][0])))
    caso('destino inexistente', ['destino', 'E99'], lambda d: d['escenas'][0]['opciones'][0].update(destino='E99'))
    caso('variable no declarada', ['otra', 'no declarada'], lambda d: d['escenas'][0]['opciones'][0]['efectos'].update(otra=True))
    caso('valor no booleano', ['conoce_origen', 'booleano'], lambda d: d['variables'].update(conoce_origen=1))
    caso('final incompatible', ['E1', 'cantidad'], lambda d: d['escenas'][0].update(final=True))
    mensajes = []
    try:
        cargar_historia(RAIZ / 'datos/no_existe.json')
    except ErrorHistoria as error:
        mensaje = str(error)
        mensajes.append(dict(caso='archivo ilegible', mensaje=mensaje,
                             cumple='archivo' in mensaje and 'no_existe.json' in mensaje))
    for nombre, esperado, copia in casos:
        try:
            validar_historia(copia)
            mensajes.append(dict(caso=nombre, mensaje='No rechazado', cumple=False))
        except ErrorHistoria as error:
            mensaje = str(error)
            mensajes.append(dict(caso=nombre, mensaje=mensaje,
                                 cumple=all(t in mensaje for t in esperado)))
    repeticiones = []
    for _ in range(3):
        suite = unittest.defaultTestLoader.discover(str(RAIZ / "tests"), pattern='test_motor.py')
        salida = io.StringIO()
        with redirect_stdout(salida):
            resultado = unittest.TextTestRunner(stream=salida).run(suite)
        repeticiones.append(dict(casos=resultado.testsRun, fallos=len(resultado.failures),
                                 errores=len(resultado.errors), cumple=resultado.wasSuccessful()))
    evidencia = dict(python=platform.python_version(),
        RNF01=dict(meta='Segunda historia finalizada con cero cambios de código',
                   cumple=modificabilidad, huellas_antes=antes, huellas_despues=huellas()),
        RNF02=dict(meta='9 de 9 categorías con causa y localización',
                   cumple=len(mensajes) == 9 and all(m['cumple'] for m in mensajes), casos=mensajes),
        RNF03=dict(meta='Tres ejecuciones consecutivas de 7 escenarios sin fallos',
                   cumple=all(r['cumple'] and r['casos'] == 7 for r in repeticiones), ejecuciones=repeticiones))
    (RAIZ / 'evidencias/evidencia_rnf.json').write_text(json.dumps(evidencia, ensure_ascii=False, indent=2), encoding='utf-8')
    for nombre in ['RNF01', 'RNF02', 'RNF03']:
        print(f"{nombre}: {'CUMPLE' if evidencia[nombre]['cumple'] else 'FALLA'}")
    return 0 if all(evidencia[n]['cumple'] for n in ['RNF01', 'RNF02', 'RNF03']) else 1


if __name__ == '__main__':
    raise SystemExit(main())
