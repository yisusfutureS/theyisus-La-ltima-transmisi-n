"""Carga y valida historias; no contiene reglas de una narración concreta."""
import json
from pathlib import Path
from copy import deepcopy


class ErrorHistoria(ValueError):
    pass


def validar_historia(datos):
    def exigir(condicion, campo, causa):
        if not condicion:
            raise ErrorHistoria(f"{campo}: {causa}")

    def campos(objeto, nombres, ruta):
        exigir(isinstance(objeto, dict), ruta, "debe ser un objeto")
        for nombre in nombres:
            exigir(nombre in objeto, f"{ruta}.{nombre}", "campo obligatorio ausente")

    def cadena(valor, ruta):
        exigir(isinstance(valor, str) and bool(valor.strip()), ruta,
               "debe ser texto no vacío")

    campos(datos, ['titulo', 'inicio', 'variables', 'escenas'], 'historia')
    cadena(datos['titulo'], 'titulo')
    cadena(datos['inicio'], 'inicio')
    variables = datos['variables']
    exigir(isinstance(variables, dict), 'variables', 'debe ser un objeto')
    for nombre, valor in variables.items():
        cadena(nombre, 'variables.nombre')
        exigir(type(valor) is bool, f'variables.{nombre}', 'debe ser booleano')
    escenas = datos['escenas']
    exigir(isinstance(escenas, list) and bool(escenas), 'escenas',
           'debe ser una lista no vacía')
    ids = set()
    for indice, escena in enumerate(escenas):
        ruta = f'escenas[{indice}]'
        campos(escena, ['id', 'texto', 'final', 'opciones'], ruta)
        cadena(escena['id'], f'{ruta}.id')
        ruta = f"escena {escena['id']}"
        exigir(escena['id'] not in ids, ruta, 'ID de escena repetido')
        ids.add(escena['id'])
        cadena(escena['texto'], f'{ruta}.texto')
        exigir(type(escena['final']) is bool, f'{ruta}.final', 'debe ser booleano')
        opciones = escena['opciones']
        exigir(isinstance(opciones, list), f'{ruta}.opciones', 'debe ser lista')
        exigir(len(opciones) == 0 if escena['final'] else len(opciones) >= 1,
               f'{ruta}.opciones', 'cantidad incompatible con final')
        ids_opciones = set()
        for numero, opcion in enumerate(opciones):
            ubicacion = f'{ruta}.opciones[{numero}]'
            campos(opcion, ['id', 'texto', 'destino', 'condiciones', 'efectos'], ubicacion)
            for campo in ['id', 'texto', 'destino']:
                cadena(opcion[campo], f'{ubicacion}.{campo}')
            ubicacion = f"{ruta}.opcion {opcion['id']}"
            exigir(opcion['id'] not in ids_opciones, ubicacion, 'ID de opción repetido')
            ids_opciones.add(opcion['id'])
            for campo in ['condiciones', 'efectos']:
                exigir(isinstance(opcion[campo], dict), f'{ubicacion}.{campo}',
                       'debe ser un objeto')
                for nombre, valor in opcion[campo].items():
                    exigir(nombre in variables, f'{ubicacion}.{campo}.{nombre}',
                           'variable no declarada')
                    exigir(type(valor) is bool, f'{ubicacion}.{campo}.{nombre}',
                           'debe ser booleano')
    exigir(datos['inicio'] in ids, 'inicio', f"escena inexistente: {datos['inicio']}")
    for escena in escenas:
        for opcion in escena['opciones']:
            exigir(opcion['destino'] in ids,
                   f"escena {escena['id']}.opcion {opcion['id']}.destino",
                   f"escena inexistente: {opcion['destino']}")
    return deepcopy(datos)


def cargar_historia(ruta):
    try:
        with Path(ruta).open(encoding='utf-8') as archivo:
            datos = json.load(archivo)
    except (OSError, UnicodeError, ValueError, RecursionError) as error:
        raise ErrorHistoria(f'archivo {ruta}: no se pudo leer JSON: {error}') from error
    return validar_historia(datos)
