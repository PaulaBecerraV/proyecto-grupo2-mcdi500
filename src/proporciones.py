"""Clase de proporciones de la Fase 3 (núcleo algorítmico).

Calcula la proporción de egresos con colecistectomía por grupo de riesgo y
provincia, **sobre el CSV ya transformado en F2_03** (no vuelve a transformar).

Diseño (POO):
- ``CalculadorBase`` es una clase abstracta que fija el contrato (método
  ``calcular``) y el formato de salida (patrón *Template Method*).
- ``CalcBucle``, ``CalcPandas``, ``CalcNumpy`` y ``CalcRecursivo`` heredan de
  la base y solo especializan *cómo se cuentan* los egresos (patrón *Strategy*).
  El resto del sistema las usa de forma intercambiable (polimorfismo).
- ``CalcRecursivo`` aplica recursividad (divide y vencerás): parte las filas en
  mitades, cuenta cada mitad por recursión y suma los resultados.
- El DataFrame se guarda en un atributo protegido y se valida al construir el
  objeto (encapsulamiento).

Incluye además el intervalo de confianza de Wilson (95 %) para cada proporción.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import math

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class Columnas:
    """Nombres de las columnas del CSV transformado (valores por defecto reales de F2_03)."""

    provincia: str = "PROVINCIA_RESIDENCIA"
    flag: str = "FLAG_COLECISTECTOMIA"
    grupos: tuple = ("GRUPO_RIESGO_MUJER", "GRUPO_RIESGO_ETNIA", "GRUPO_RIESGO_40_49")

    def requeridas(self):
        return (self.provincia, self.flag) + tuple(self.grupos)


def wilson(k, n, z=1.96):
    """Intervalo de confianza de Wilson para una proporción (por defecto 95 %).

    Devuelve (límite_inferior, límite_superior). Para n = 0 devuelve (nan, nan).
    Es más adecuado que el intervalo normal cuando n es pequeño o la proporción
    se acerca a 0 o 1, como ocurre en los grupos de Malleco.
    """
    if n == 0:
        return (float("nan"), float("nan"))
    p = k / n
    denom = 1 + z**2 / n
    centro = (p + z**2 / (2 * n)) / denom
    margen = (z * math.sqrt(p * (1 - p) / n + z**2 / (4 * n**2))) / denom
    return (max(0.0, centro - margen), min(1.0, centro + margen))


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
        """Tabla estándar de proporciones con intervalo de Wilson al 95 %."""
        filas = []
        for (g, p, en), (n, k) in self._contar().items():
            li, ls = wilson(k, n)
            filas.append({"grupo": g, "provincia": p, "en_grupo": en, "egresos": n,
                          "con_colecistectomia": k,
                          "proporcion": k / n if n else np.nan,
                          "ic95_inf": li, "ic95_sup": ls})
        tabla = pd.DataFrame(filas, columns=["grupo", "provincia", "en_grupo", "egresos",
                                             "con_colecistectomia", "proporcion",
                                             "ic95_inf", "ic95_sup"])
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


class CalcRecursivo(CalculadorBase):
    """Versión 4: recursiva (divide y vencerás).

    Parte las filas en dos mitades, cuenta cada mitad por recursión y suma los
    resultados. El caso base es un bloque de UMBRAL filas o menos, que se cuenta
    directamente. Evidencia el uso de recursividad exigido por la Fase 3.
    """

    nombre = "Recursivo (divide y vencerás)"
    UMBRAL = 256   # tamaño del bloque base; evita una recursión demasiado profunda

    def _preparar(self):
        c = self._cols
        self._prov = self._df[c.provincia].tolist()
        self._flag = self._df[c.flag].tolist()
        self._grupos = [self._df[g].tolist() for g in c.grupos]
        self._nombres = c.grupos

    def _contar_bloque(self, ini, fin):
        """Cuenta las filas [ini, fin) directamente (caso base)."""
        cuenta = {}
        for i in range(ini, fin):
            flag = self._flag[i]
            prov = self._prov[i]
            for g, col in enumerate(self._grupos):
                par = cuenta.setdefault((self._nombres[g], prov, col[i]), [0, 0])
                par[0] += 1
                par[1] += flag
        return cuenta

    def _combinar(self, a, b):
        """Suma dos diccionarios de conteo."""
        for clave, (n, k) in b.items():
            par = a.setdefault(clave, [0, 0])
            par[0] += n
            par[1] += k
        return a

    def _contar_recursivo(self, ini, fin):
        if fin - ini <= self.UMBRAL:            # caso base
            return self._contar_bloque(ini, fin)
        medio = (ini + fin) // 2                # dividir
        izq = self._contar_recursivo(ini, medio)
        der = self._contar_recursivo(medio, fin)
        return self._combinar(izq, der)         # vencer: combinar mitades

    def _contar(self):
        bruto = self._contar_recursivo(0, len(self._prov))
        return {k: tuple(v) for k, v in bruto.items()}


ESTRATEGIAS = (CalcBucle, CalcPandas, CalcNumpy, CalcRecursivo)
