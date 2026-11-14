"""Contrato común para las etapas del procesamiento de datos de F3."""

from abc import ABC, abstractmethod

import pandas as pd


class EtapaBase(ABC):
    """Una etapa recibe un DataFrame y devuelve el DataFrame resultante.

    Las subclases deben implementar ``ejecutar``. La lógica específica de
    cada transformación corresponde a esas subclases.
    """

    @abstractmethod
    def ejecutar(self, datos: pd.DataFrame) -> pd.DataFrame:
        """Procesa los datos sin modificar el DataFrame recibido.

        Una etapa debe informar con una excepción clara si faltan columnas
        necesarias. Puede devolver cero filas si el filtro no encuentra casos.
        """
        raise NotImplementedError
