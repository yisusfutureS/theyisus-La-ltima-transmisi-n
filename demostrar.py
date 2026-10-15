"""Recorridos y salidas reales para la demostración."""
import sys, json
from pathlib import Path
RAIZ=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(RAIZ/'src'))
from cargador import cargar_historia, validar_historia, ErrorHistoria
from motor import Motor, ErrorEleccion

def estado(m):
    return {'escena':m.escena_actual['id'],'variables':m.variables,
            'final':m.escena_actual['final'],
            'opciones':[o['id'] for o in m.opciones_disponibles()]}

def main():
    bloques=[]
    for final,ruta in [('E4',['revisar','investigar','activar_codigo']),
                       ('E5',['revisar','continuar','activar_sin_verificar']),
                       ('E6',['revisar','investigar','cortar'])]:
        m=Motor(cargar_historia(RAIZ/'datos/la_ultima_transmision.json'))
        lineas=['Inicio: '+json.dumps(estado(m),ensure_ascii=False)]
        for opcion in ruta:
            m.elegir(opcion)
            lineas.append('Elegir '+opcion+': '+json.dumps(estado(m),ensure_ascii=False))
        assert m.escena_actual['id']==final
        bloques.append({'titulo':'Recorrido al final '+final,'salida':'\n'.join(lineas)})
    m=Motor(cargar_historia(RAIZ/'datos/segunda_historia.json'))
    lineas=['Segunda historia: El último algoritmo; mismo motor']
    for opcion in ['O1','O1']:
        m.elegir(opcion)
        lineas.append('Elegir '+opcion+': '+json.dumps(estado(m),ensure_ascii=False))
    assert m.escena_actual['id']=='S5'
    bloques.append({'titulo':'Segunda historia sin cambiar el motor','salida':'\n'.join(lineas)})
    datos=cargar_historia(RAIZ/'datos/la_ultima_transmision.json')
    datos['escenas'][0]['opciones'][0]['destino']='E99'
    try:
        validar_historia(datos)
        raise AssertionError('No rechazó E99')
    except ErrorHistoria as error:
        bloques.append({'titulo':'Error de contenido controlado','salida':str(error)})

    m=Motor(cargar_historia(RAIZ/'datos/la_ultima_transmision.json'))
    lineas=['Inicio: respaldo='+str(m.puede_deshacer)]
    m.elegir('revisar'); m.elegir('investigar')
    lineas.append('Investigar: '+json.dumps(estado(m),ensure_ascii=False))
    try:
        m.elegir('activar_sin_verificar')
    except ErrorEleccion as error:
        lineas.append(str(error)+'; respaldo='+str(m.puede_deshacer))
    assert m.deshacer()
    lineas.append('Deshacer: '+json.dumps(estado(m),ensure_ascii=False))
    lineas.append('Otro deshacer: '+str(m.deshacer()))
    m.elegir('continuar'); m.elegir('activar_sin_verificar')
    lineas.append('Llegada al final: '+json.dumps(estado(m),ensure_ascii=False))
    assert m.deshacer()
    lineas.append('Desde final: '+json.dumps(estado(m),ensure_ascii=False))
    m.reiniciar()
    lineas.append('Reinicio: '+json.dumps(estado(m),ensure_ascii=False)+'; respaldo='+str(m.puede_deshacer))
    bloques.append({'titulo':'Cambio: retroceso de un nivel','salida':'\n'.join(lineas)})

    for bloque in bloques:
        print(bloque['titulo']+'\n'+bloque['salida']+'\n')
    (RAIZ/'demo/recorridos.json').write_text(json.dumps(bloques,ensure_ascii=False,indent=2),encoding='utf-8')
if __name__=='__main__':
    main()
