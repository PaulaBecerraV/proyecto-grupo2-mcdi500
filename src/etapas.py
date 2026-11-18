"""Etapas concretas del pipeline de F3.

Cada clase hereda de EtapaBase. FiltroColelitiasis, AsignadorProvincia y
MarcadorGruposRiesgo aplican reglas fijas de la pregunta de investigación
(envuelven funciones de transformacion.py). MarcadorColecistectomia aprende de
los datos el vocabulario de glosas de colecistectomía y luego lo aplica.
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
    """Marca si el egreso tuvo colecistectomía.

    Es la única etapa que aprende de los datos: en ajustar() recorre las
    glosas de intervención y guarda el vocabulario de glosas que corresponden
    a colecistectomía; en ejecutar() marca los egresos cuya glosa pertenece a
    ese vocabulario aprendido.
    """

    COLUMNA = "GLOSA_INTERV_Q_PPAL"

    def __init__(self, patron="colecistectom"):
        self.patron = patron
        self._vocabulario = None          # se llena al ajustar (encapsulado)

    @property
    def vocabulario(self):
        """Glosas aprendidas como colecistectomía (solo lectura)."""
        if self._vocabulario is None:
            raise RuntimeError("El marcador aún no se ha ajustado.")
        return self._vocabulario

    def ajustar(self, datos):
        """Aprende de los datos qué glosas corresponden a colecistectomía."""
        if self.COLUMNA not in datos.columns:
            raise KeyError(f"MarcadorColecistectomia: falta la columna {self.COLUMNA}.")
        glosas = datos[self.COLUMNA].dropna().unique()
        self._vocabulario = frozenset(
            g for g in glosas if self.patron in str(g).lower()
        )
        return self

    def ejecutar(self, datos):
        """Aplica el vocabulario aprendido; si no se ha ajustado, aprende primero."""
        if self._vocabulario is None:
            self.ajustar(datos)
        if self.COLUMNA not in datos.columns:
            raise KeyError(f"MarcadorColecistectomia: falta la columna {self.COLUMNA}.")
        resultado = datos.copy()
        resultado["FLAG_COLECISTECTOMIA"] = resultado[self.COLUMNA].isin(self._vocabulario)
        return resultado