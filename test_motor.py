import unittest
import tempfile
from pathlib import Path
from copy import deepcopy
import sys

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))

from cargador import cargar_historia, validar_historia, ErrorHistoria
from motor import Motor, ErrorEleccion

BASE = RAIZ / 'datos'


class Pruebas(unittest.TestCase):
    def setUp(self):
        self.datos = cargar_historia(BASE / 'la_ultima_transmision.json')
        self.motor = Motor(self.datos)

    def test_U1_carga_y_errores(self):
        self.assertEqual(self.datos['inicio'], 'E1')
        with tempfile.TemporaryDirectory(dir=BASE.parent) as carpeta:
            ruta = Path(carpeta) / 'mala.json'
            with self.assertRaisesRegex(ErrorHistoria, 'archivo'):
                cargar_historia(ruta)
            ruta.write_text('{', encoding='utf-8')
            with self.assertRaisesRegex(ErrorHistoria, 'JSON'):
                cargar_historia(ruta)
        variantes = []
        def caso(nombre, modificar):
            copia = deepcopy(self.datos)
            modificar(copia)
            variantes.append((nombre, copia))
        caso('titulo', lambda d: d.pop('titulo'))
        caso('inicio', lambda d: d.update(inicio='E99'))
        caso('repetido', lambda d: d['escenas'].append(deepcopy(d['escenas'][0])))
        caso('repetido', lambda d: d['escenas'][0]['opciones'].append(deepcopy(d['escenas'][0]['opciones'][0])))
        caso('E99', lambda d: d['escenas'][0]['opciones'][0].update(destino='E99'))
        for campo in ['condiciones', 'efectos']:
            caso('no declarada', lambda d, c=campo: d['escenas'][0]['opciones'][0][c].update(otra=True))
            caso('booleano', lambda d, c=campo: d['escenas'][0]['opciones'][0][c].update(conoce_origen=1))
        caso('booleano', lambda d: d['variables'].update(conoce_origen='false'))
        caso('cantidad', lambda d: d['escenas'][0].update(opciones=[]))
        caso('cantidad', lambda d: d['escenas'][0].update(final=True))
        variantes.append(('objeto', []))
        for mensaje, datos in variantes:
            with self.subTest(mensaje=mensaje, datos=datos):
                with self.assertRaisesRegex(ErrorHistoria, mensaje):
                    validar_historia(datos)

    def test_U2_condiciones_y_estado_CA01(self):
        self.motor.elegir('revisar')
        self.motor.elegir('investigar')
        self.assertEqual(self.motor.escena_actual['id'], 'E3')
        self.assertTrue(self.motor.variables['conoce_origen'])
        self.assertEqual({o['id'] for o in self.motor.opciones_disponibles()}, {'activar_codigo', 'cortar'})

    def test_U3_rechazo_directo_CA02(self):
        self.motor.elegir('revisar')
        self.motor.elegir('continuar')
        self.assertEqual({o['id'] for o in self.motor.opciones_disponibles()}, {'activar_sin_verificar', 'cortar'})
        with self.assertRaises(ErrorEleccion):
            self.motor.elegir('activar_codigo')
        self.assertEqual(self.motor.escena_actual['id'], 'E3')
        self.motor.elegir('activar_sin_verificar')
        self.assertEqual(self.motor.escena_actual['id'], 'E5')

    def test_U4_finales_y_bloqueo(self):
        self.datos['escenas'][0]['opciones'][0]['condiciones'] = {'conoce_origen': True}
        motor = Motor(self.datos)
        self.assertTrue(motor.bloqueada)
        with self.assertRaises(ErrorEleccion):
            motor.elegir('revisar')
        motor.reiniciar()
        self.assertEqual(motor.escena_actual['id'], 'E1')
        self.assertFalse(motor.puede_deshacer)

    def test_U5_reinicio(self):
        self.assertFalse(self.motor.puede_deshacer)
        self.motor.elegir('revisar')
        self.motor.elegir('investigar')
        self.motor.reiniciar()
        self.assertEqual(self.motor.escena_actual['id'], 'E1')
        self.assertEqual(self.motor.variables, self.datos['variables'])
        self.assertFalse(self.motor.puede_deshacer)

    def test_U6_deshacer(self):
        self.assertFalse(self.motor.deshacer())
        self.motor.elegir('revisar')
        previo = self.motor.variables
        self.motor.elegir('investigar')
        for invalida in ['inexistente', 'activar_sin_verificar']:
            with self.assertRaises(ErrorEleccion):
                self.motor.elegir(invalida)
            self.assertTrue(self.motor.puede_deshacer)
            self.assertTrue(self.motor.variables['conoce_origen'])
        self.assertTrue(self.motor.deshacer())
        self.assertEqual(self.motor.escena_actual['id'], 'E2')
        self.assertEqual(self.motor.variables, previo)
        self.assertFalse(self.motor.deshacer())
        self.assertEqual(self.motor.escena_actual['id'], 'E2')
        self.motor.elegir('continuar')
        self.assertTrue(self.motor.puede_deshacer)
        self.assertEqual({o['id'] for o in self.motor.opciones_disponibles()}, {'activar_sin_verificar', 'cortar'})

    def test_I1_archivo_tres_finales_deshacer_y_segunda_historia(self):
        for intermedia, ultima, final in [('investigar', 'activar_codigo', 'E4'),
                                          ('continuar', 'activar_sin_verificar', 'E5'),
                                          ('investigar', 'cortar', 'E6')]:
            with self.subTest(final=final):
                motor = Motor(cargar_historia(BASE / 'la_ultima_transmision.json'))
                motor.elegir('revisar')
                motor.elegir(intermedia)
                previo = motor.variables
                motor.elegir(ultima)
                self.assertEqual(motor.escena_actual['id'], final)
                self.assertEqual(motor.variables['confia_en_la_voz'], ultima != 'cortar')
                self.assertEqual(motor.variables['conoce_origen'], previo['conoce_origen'])
                self.assertTrue(motor.escena_actual['final'])
                self.assertEqual(motor.opciones_disponibles(), [])
                self.assertFalse(motor.bloqueada)
                self.assertTrue(motor.deshacer())
                self.assertEqual(motor.escena_actual['id'], 'E3')
                self.assertEqual(motor.variables, previo)
                self.assertFalse(motor.deshacer())
        motor = Motor(cargar_historia(BASE / 'segunda_historia.json'))
        motor.elegir('O1')
        motor.elegir('O1')
        self.assertTrue(motor.escena_actual['final'])
        self.assertEqual(motor.escena_actual['id'], 'S5')


    def test_I2_segunda_historia_condiciones_y_finales(self):
        for elecciones, final in [(['O2'], 'S3'), (['O1', 'O2'], 'S4'),
                                  (['O1', 'O1'], 'S5')]:
            with self.subTest(final=final):
                motor = Motor(cargar_historia(BASE / 'segunda_historia.json'))
                for eleccion in elecciones:
                    motor.elegir(eleccion)
                self.assertEqual(motor.escena_actual['id'], final)
                self.assertTrue(motor.escena_actual['final'])
                self.assertTrue(motor.deshacer())
                self.assertFalse(motor.puede_deshacer)
        motor = Motor(cargar_historia(BASE / 'segunda_historia.json'))
        motor.elegir('O3')
        self.assertEqual({o['id'] for o in motor.opciones_disponibles()}, {'O2', 'O3'})
        with self.assertRaises(ErrorEleccion):
            motor.elegir('O1')
        self.assertTrue(motor.deshacer())
        self.assertEqual(motor.escena_actual['id'], 'S1')
        self.assertEqual(motor.variables, {'ia_autonoma': False, 'codigo_guardado': False,
                                         'permitio_estudiar': False})


if __name__ == '__main__':
    unittest.main(verbosity=2)
