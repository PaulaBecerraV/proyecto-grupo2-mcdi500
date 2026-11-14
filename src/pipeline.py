"""Ejecución ordenada de las etapas del proyecto."""

from collections.abc import Iterable

import pandas as pd

from .base import EtapaBase


class Pipeline:
    """Conecta etapas: la salida de una es la entrada de la siguiente.

    Parámetros
    ----------
    etapas : iterable de EtapaBase
        Objetos ya creados, en el orden en que deben ejecutarse.
    """

    def __init__(self, etapas: Iterable[EtapaBase]):
        self._etapas = tuple(etapas)

        if not self._etapas:
            raise ValueError("Pipeline: se requiere al menos una etapa.")

        for posicion, etapa in enumerate(self._etapas, start=1):
            if not isinstance(etapa, EtapaBase):
                raise TypeError(
                    f"Pipeline: la etapa {posicion} debe heredar de EtapaBase."
                )

    @property
    def etapas(self) -> tuple[EtapaBase, ...]:
        """Permite consultar el orden de las etapas configuradas."""
        return self._etapas

    def ejecutar(self, datos: pd.DataFrame) -> pd.DataFrame:
        """Ejecuta todas las etapas y devuelve el resultado final.

        Se parte de una copia para proteger la entrada del usuario. Cada
        etapa debe devolver un DataFrame. Las excepciones de las etapas se
        propagan: el flujo se detiene, sin ocultar fallos ni exportar resultados.
        """
        if not isinstance(datos, pd.DataFrame):
            raise TypeError("Pipeline.ejecutar: la entrada debe ser un DataFrame.")

        resultado = datos.copy()

        for etapa in self._etapas:
            resultado = etapa.ejecutar(resultado)
            if not isinstance(resultado, pd.DataFrame):
                raise TypeError(
                    f"{type(etapa).__name__}.ejecutar debe devolver un DataFrame."
                )

        return resultado
