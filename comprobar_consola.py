"""Pruebas adicionales de la interfaz ejecutada como un proceso real."""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]


def ejecutar(ruta, entradas=''):
    return subprocess.run([sys.executable, str(RAIZ / 'src/main.py'), str(ruta)],
                          input=entradas, text=True, capture_output=True, encoding='utf-8',
                          env=__import__('os').environ | {'PYTHONIOENCODING': 'utf-8'},
                          cwd=RAIZ)


def main():
    resultado = ejecutar(RAIZ / 'datos/la_ultima_transmision.json',
        'revisar\ncontinuar\nactivar_codigo\nactivar_sin_verificar\n:reiniciar\n:salir\n')
    assert resultado.returncode == 0, resultado.stderr
    assert 'Opción inexistente o no habilitada' in resultado.stdout
    assert '[E5]' in resultado.stdout
    assert resultado.stdout.count('[E1]') == 2
    resultados = ['Consola: elección inválida, final y reinicio: OK']
    with tempfile.TemporaryDirectory(dir=RAIZ) as carpeta:
        datos = json.loads((RAIZ / 'datos/la_ultima_transmision.json').read_text(encoding='utf-8'))
        ruta = Path(carpeta) / 'invalida.json'
        datos['escenas'][0]['opciones'][0]['destino'] = 'E99'
        ruta.write_text(json.dumps(datos), encoding='utf-8')
        resultado = ejecutar(ruta)
        assert resultado.returncode == 1
        assert 'E99' in resultado.stdout and 'destino' in resultado.stdout
        assert 'Traceback' not in resultado.stderr and '[E1]' not in resultado.stdout
        resultados.append('Consola: destino E99 rechazado antes de jugar: OK')
        datos['escenas'][0]['opciones'][0]['destino'] = 'E2'
        datos['escenas'][0]['opciones'][0]['condiciones'] = {'conoce_origen': True}
        ruta.write_text(json.dumps(datos), encoding='utf-8')
        resultado = ejecutar(ruta, ':reiniciar\n:salir\n')
        assert resultado.returncode == 0
        assert resultado.stdout.count('Bloqueo:') == 2
        resultados.append('Consola: bloqueo controlado y reinicio: OK')
    (RAIZ / 'evidencias/evidencia_consola.txt').write_text('\n'.join(resultados) + '\n', encoding='utf-8')
    print('\n'.join(resultados))


if __name__ == '__main__':
    main()
