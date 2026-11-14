"""Utilidades para verificar el entorno de ejecución del proyecto."""
import sys
from importlib.metadata import version, PackageNotFoundError

LIBRERIAS_PROYECTO = ("pandas", "numpy", "matplotlib", "seaborn")


def verificar_entorno(librerias=LIBRERIAS_PROYECTO):
    """Muestra la versión de Python, si se usa el entorno virtual del
    proyecto y la versión instalada de cada librería de la lista.

    Devuelve un diccionario {librería: versión o None}, para poder
    usarla también en pruebas automatizadas.
    """
    print("Versión de Python:", sys.version.split()[0])
    print("Entorno virtual del proyecto (.venv):", ".venv" in sys.executable)
    versiones = {}
    for nombre in librerias:
        try:
            versiones[nombre] = version(nombre)
            print(f"{nombre}: {versiones[nombre]}")
        except PackageNotFoundError:
            versiones[nombre] = None
            print(f"{nombre}: NO instalada")
    return versiones
