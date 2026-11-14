"""Etapas concretas del pipeline de F3.

Cada clase hereda de EtapaBase y envuelve una función de transformacion.py.
"""

from .base import EtapaBase
from . import transformacion as tr


class FiltroColelitiasis(EtapaBase):
    """Deja solo los egresos con diagnóstico principal K80 (colelitiasis)."""

    def ejecutar(self, datos):
        return tr.filtrar_colelitiasis(datos)


class AsignadorProvincia(EtapaBase):
    """Agrega la provincia de residencia (Cautín o Malleco) según el código de comuna."""
    
    def ejecutar(self, datos):
        return tr.asignar_provincia(datos)


class MarcadorGruposRiesgo(EtapaBase):
    """Agrega las tres columnas de grupo de riesgo: mujeres, etnia y 40 a 49 años."""

    def ejecutar(self, datos):
        return tr.marcar_grupos_riesgo(datos)


class MarcadorColecistectomia(EtapaBase):
    """Marca si el egreso tuvo colecistectomía según la glosa de la intervención principal."""

    def ejecutar(self, datos):
        return tr.marcar_colecistectomia(datos)
        