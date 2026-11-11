"""Funciones reutilizables de la transformación de colelitiasis (Fase 2 -> Fase 3).

Mismo criterio que F2_03_transformacion.ipynb, pero como funciones con parámetros
definidos, en lugar de celdas sueltas. Cada función recibe un DataFrame, no lo
modifica (trabaja sobre una copia) y devuelve un DataFrame nuevo, para que el
flujo de datos sea verificable paso a paso.

Este módulo es la base que se reutilizará en la Fase 3 (las clases del pipeline
encapsularán esta misma lógica).
"""

import pandas as pd

PROVINCIA_POR_CODIGO = {
    "091": "Cautín",
    "092": "Malleco",
}


def filtrar_colelitiasis(df):
    """Filtra los egresos cuyo diagnóstico principal es colelitiasis (K80.0-K80.8).

    Parámetros
    ----------
    df : pandas.DataFrame
        Debe tener la columna DIAG1.

    Devuelve
    --------
    pandas.DataFrame
        Copia de df solo con los egresos cuyo DIAG1 empieza con "K80".

    Excepciones
    -----------
    KeyError
        Si falta la columna DIAG1.
    """
    if "DIAG1" not in df.columns:
        raise KeyError("filtrar_colelitiasis: falta la columna DIAG1.")

    es_colelitiasis = df["DIAG1"].str.startswith("K80", na=False)
    return df[es_colelitiasis].copy()


def asignar_provincia(df):
    """Agrega la columna PROVINCIA_RESIDENCIA a partir del código de comuna.

    Comunas que empiezan con 091 quedan como "Cautín" y con 092 como "Malleco".
    Un código distinto (o un valor enmascarado "*") queda como nulo (NaN).

    Parámetros
    ----------
    df : pandas.DataFrame
        Debe tener la columna COMUNA_RESIDENCIA.

    Devuelve
    --------
    pandas.DataFrame
        Copia de df con la columna PROVINCIA_RESIDENCIA agregada.

    Excepciones
    -----------
    KeyError
        Si falta la columna COMUNA_RESIDENCIA.
    """
    if "COMUNA_RESIDENCIA" not in df.columns:
        raise KeyError("asignar_provincia: falta la columna COMUNA_RESIDENCIA.")

    resultado = df.copy()
    resultado["PROVINCIA_RESIDENCIA"] = (
        resultado["COMUNA_RESIDENCIA"].str[:3].map(PROVINCIA_POR_CODIGO)
    )
    return resultado


def marcar_grupos_riesgo(df):
    """Agrega las tres columnas booleanas de grupo de riesgo, cada una por separado.

    - GRUPO_RIESGO_MUJER: SEXO == "MUJER"
    - GRUPO_RIESGO_ETNIA: ETNIA == "Si se identifica con alguna etnia"
    - GRUPO_RIESGO_40_49: GRUPO_EDAD == "40 a 49"

    Parámetros
    ----------
    df : pandas.DataFrame
        Debe tener las columnas SEXO, ETNIA y GRUPO_EDAD.

    Devuelve
    --------
    pandas.DataFrame
        Copia de df con las tres columnas de grupo de riesgo agregadas.

    Excepciones
    -----------
    KeyError
        Si falta alguna de las columnas SEXO, ETNIA o GRUPO_EDAD.
    """
    requeridas = ["SEXO", "ETNIA", "GRUPO_EDAD"]
    faltantes = [c for c in requeridas if c not in df.columns]
    if faltantes:
        raise KeyError(f"marcar_grupos_riesgo: faltan columnas {faltantes}.")

    resultado = df.copy()
    resultado["GRUPO_RIESGO_MUJER"] = resultado["SEXO"] == "MUJER"
    resultado["GRUPO_RIESGO_ETNIA"] = (
        resultado["ETNIA"] == "Si se identifica con alguna etnia"
    )
    resultado["GRUPO_RIESGO_40_49"] = resultado["GRUPO_EDAD"] == "40 a 49"
    return resultado


def marcar_colecistectomia(df):
    """Agrega la columna booleana FLAG_COLECISTECTOMIA.

    Se considera que hubo colecistectomía cuando GLOSA_INTERV_Q_PPAL contiene
    "colecistectom" (sin distinguir mayúsculas ni tildes). Un campo vacío se
    interpreta como "sin colecistectomía registrada", no como dato perdido.

    Parámetros
    ----------
    df : pandas.DataFrame
        Debe tener la columna GLOSA_INTERV_Q_PPAL.

    Devuelve
    --------
    pandas.DataFrame
        Copia de df con la columna FLAG_COLECISTECTOMIA agregada.

    Excepciones
    -----------
    KeyError
        Si falta la columna GLOSA_INTERV_Q_PPAL.
    """
    if "GLOSA_INTERV_Q_PPAL" not in df.columns:
        raise KeyError("marcar_colecistectomia: falta la columna GLOSA_INTERV_Q_PPAL.")

    resultado = df.copy()
    resultado["FLAG_COLECISTECTOMIA"] = resultado["GLOSA_INTERV_Q_PPAL"].str.contains(
        "colecistectom", case=False, na=False
    )
    return resultado


def transformar(df):
    """Encadena las cuatro funciones anteriores: el mismo resultado que F2_03.

    Parámetros
    ----------
    df : pandas.DataFrame
        Subconjunto de egresos de La Araucanía (salida de F2_01), con las
        columnas DIAG1, COMUNA_RESIDENCIA, SEXO, ETNIA, GRUPO_EDAD y
        GLOSA_INTERV_Q_PPAL.

    Devuelve
    --------
    pandas.DataFrame
        Egresos por colelitiasis (K80.0-K80.8), con provincia, los tres grupos
        de riesgo y la marca de colecistectomía agregados.

    Excepciones
    -----------
    KeyError
        Si falta alguna columna requerida (ver cada función interna).
    """
    resultado = filtrar_colelitiasis(df)
    resultado = asignar_provincia(resultado)
    resultado = marcar_grupos_riesgo(resultado)
    resultado = marcar_colecistectomia(resultado)
    return resultado
