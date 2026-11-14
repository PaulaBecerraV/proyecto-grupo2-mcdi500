"""Clase de proporciones de la Fase 3 (núcleo algorítmico).

Calcula la proporción de egresos con colecistectomía por grupo de riesgo y
provincia, **sobre el CSV ya transformado en F2_03** (no vuelve a transformar).

Diseño (POO):
- ``CalculadorBase`` es una clase abstracta que fija el contrato (método
  ``calcular``) y el formato de salida (patrón *Template Method*).
- ``CalcBucle``, ``CalcPandas`` y ``CalcNumpy`` heredan de la base y solo
  especializan *cómo se cuentan* los egresos (patrón *Strategy*). El resto del
  sistema las usa de forma intercambiable (polimorfismo).
- El DataFrame se guarda en un atributo protegido y se valida al construir el
  objeto (encapsulamiento).
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class Columnas:
    """Nombres de las columnas del CSV transformado (ajustar si difieren)."""

    provincia: str = "PROVINCIA"
    flag: str = "FLAG_COLECISTECTOMIA"
    grupos: tuple = ("GR_MUJER", "GR_ETNIA", "GR_40_49")

    def requeridas(self):
        return (self.provincia, self.flag) + tuple(self.grupos)


class CalculadorBase(ABC):
    """Contrato común: cuenta egresos con colecistectomía por grupo y provincia."""

    nombre = "base"

    def __init__(self, df, columnas=None):
        self._cols = columnas or Columnas()
        faltan = [c for c in self._cols.requeridas() if c not in df.columns]
        if faltan:
            raise KeyError(f"{type(self).__name__}: faltan las columnas {faltan}.")
        if df[self._cols.provincia].isna().any():
            raise ValueError(f"{type(self).__name__}: hay egresos sin provincia asignada.")
        self._df = df[list(self._cols.requeridas())].copy()   # estado protegido
        self._preparar()

    @property
    def n_egresos(self):
        return len(self._df)

    def _preparar(self):
        """Gancho opcional: cada estrategia arma aquí su representación interna."""

    @abstractmethod
    def _contar(self):
        """Devuelve {(grupo, provincia, en_grupo): (egresos, con_colecistectomia)}."""

    def calcular(self):
        """Tabla estándar de proporciones (misma salida para todas las estrategias)."""
        filas = [
            {"grupo": g, "provincia": p, "en_grupo": en, "egresos": n,
             "con_colecistectomia": k, "proporcion": k / n if n else np.nan}
            for (g, p, en), (n, k) in self._contar().items()
        ]
        tabla = pd.DataFrame(filas, columns=["grupo", "provincia", "en_grupo", "egresos",
                                             "con_colecistectomia", "proporcion"])
        return (tabla.sort_values(["grupo", "provincia", "en_grupo"])
                .reset_index(drop=True))

    def proporcion_global(self):
        """Proporción de egresos con colecistectomía, sin separar por grupo."""
        if not self.n_egresos:
            return float("nan")
        return float(self._df[self._cols.flag].mean())


class CalcBucle(CalculadorBase):
    """Versión 1: Python puro, un bucle sobre las filas con contadores en un diccionario."""

    nombre = "Bucle Python"

    def _preparar(self):
        c = self._cols
        self._prov = self._df[c.provincia].tolist()
        self._flag = self._df[c.flag].tolist()
        self._grupos = [self._df[g].tolist() for g in c.grupos]

    def _contar(self):
        cuenta = {}
        nombres = self._cols.grupos
        for i, prov in enumerate(self._prov):
            flag = self._flag[i]
            for g, col in enumerate(self._grupos):
                par = cuenta.setdefault((nombres[g], prov, col[i]), [0, 0])
                par[0] += 1
                par[1] += flag
        return {k: tuple(v) for k, v in cuenta.items()}


class CalcPandas(CalculadorBase):
    """Versión 2: pandas vectorizado con ``groupby``."""

    nombre = "pandas groupby"

    def _contar(self):
        c = self._cols
        cuenta = {}
        for g in c.grupos:
            agg = self._df.groupby([c.provincia, g])[c.flag].agg(["size", "sum"])
            for (prov, en), fila in agg.iterrows():
                cuenta[(g, prov, bool(en))] = (int(fila["size"]), int(fila["sum"]))
        return cuenta


class CalcNumpy(CalculadorBase):
    """Versión 3: NumPy con máscaras booleanas sobre arreglos."""

    nombre = "NumPy máscaras"

    def _preparar(self):
        c = self._cols
        self._provs = sorted(self._df[c.provincia].unique())
        self._prov = self._df[c.provincia].to_numpy()
        self._flag = self._df[c.flag].to_numpy(dtype=np.int64)
        self._grupos = {g: self._df[g].to_numpy(dtype=bool) for g in c.grupos}

    def _contar(self):
        cuenta = {}
        for p in self._provs:
            en_prov = self._prov == p
            for g, arr in self._grupos.items():
                for en in (False, True):
                    mask = en_prov & (arr == en)
                    n = int(mask.sum())
                    if n:
                        cuenta[(g, p, en)] = (n, int(self._flag[mask].sum()))
        return cuenta


ESTRATEGIAS = (CalcBucle, CalcPandas, CalcNumpy)
