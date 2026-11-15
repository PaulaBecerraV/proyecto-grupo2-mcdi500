"""Pruebas de las clases de etapa en src/etapas.py; ejecutar desde la raíz del repositorio.

Comando: python -m unittest discover -s tests -p test_etapas.py -v
"""

import unittest

import pandas as pd
from pandas.testing import assert_frame_equal

from src.base import EtapaBase
from src.pipeline import Pipeline
from src.etapas import (
    FiltroColelitiasis,
    AsignadorProvincia,
    MarcadorGruposRiesgo,
    MarcadorColecistectomia,
)
from src import transformacion as tr


def egresos_de_prueba():
    return pd.DataFrame({
        "DIAG1": ["K802", "K800", "J189", "K808"],
        "COMUNA_RESIDENCIA": ["09101", "09201", "09101", "*"],
        "SEXO": ["MUJER", "HOMBRE", "MUJER", "*"],
        "ETNIA": [
            "Si se identifica con alguna etnia",
            "No se identifica con alguna etnia",
            "No se identifica con alguna etnia",
            "*",
        ],
        "GRUPO_EDAD": ["40 a 49", "50 a 59", "40 a 49", "*"],
        "GLOSA_INTERV_Q_PPAL": ["Colecistectomía", None, "", ""],
    })


class TestEtapas(unittest.TestCase):
    def test_cada_etapa_hereda_de_etapabase(self):
        for clase in (
            FiltroColelitiasis,
            AsignadorProvincia,
            MarcadorGruposRiesgo,
            MarcadorColecistectomia,
        ):
            self.assertTrue(issubclass(clase, EtapaBase))

    def test_filtro_colelitiasis_coincide_con_la_funcion(self):
        entrada = egresos_de_prueba()
        resultado = FiltroColelitiasis().ejecutar(entrada)
        assert_frame_equal(
            resultado.reset_index(drop=True),
            tr.filtrar_colelitiasis(entrada).reset_index(drop=True),
        )
        self.assertEqual(len(resultado), 3)

    def test_asignador_provincia_coincide_con_la_funcion(self):
        entrada = tr.filtrar_colelitiasis(egresos_de_prueba())
        resultado = AsignadorProvincia().ejecutar(entrada)
        assert_frame_equal(
            resultado.reset_index(drop=True),
            tr.asignar_provincia(entrada).reset_index(drop=True),
        )

    def test_marcador_grupos_riesgo_coincide_con_la_funcion(self):
        entrada = tr.filtrar_colelitiasis(egresos_de_prueba())
        resultado = MarcadorGruposRiesgo().ejecutar(entrada)
        assert_frame_equal(
            resultado.reset_index(drop=True),
            tr.marcar_grupos_riesgo(entrada).reset_index(drop=True),
        )

    def test_marcador_colecistectomia_coincide_con_la_funcion(self):
        entrada = tr.filtrar_colelitiasis(egresos_de_prueba())
        resultado = MarcadorColecistectomia().ejecutar(entrada)
        assert_frame_equal(
            resultado.reset_index(drop=True),
            tr.marcar_colecistectomia(entrada).reset_index(drop=True),
        )

    def test_caso_limite_comuna_fuera_de_rango_y_glosa_vacia(self):
        entrada = pd.DataFrame({
            "DIAG1": ["K801"],
            "COMUNA_RESIDENCIA": ["05101"],  # fuera de 091/092
            "SEXO": ["MUJER"],
            "ETNIA": ["No se identifica con alguna etnia"],
            "GRUPO_EDAD": ["40 a 49"],
            "GLOSA_INTERV_Q_PPAL": [None],
        })
        etapas = [
            FiltroColelitiasis(),
            AsignadorProvincia(),
            MarcadorGruposRiesgo(),
            MarcadorColecistectomia(),
        ]
        resultado = Pipeline(etapas).ejecutar(entrada)
        self.assertTrue(resultado["PROVINCIA_RESIDENCIA"].isna().all())
        self.assertFalse(resultado["FLAG_COLECISTECTOMIA"].any())

    def test_excepcion_por_columna_faltante(self):
        sin_glosa = tr.filtrar_colelitiasis(egresos_de_prueba()).drop(
            columns=["GLOSA_INTERV_Q_PPAL"]
        )
        with self.assertRaisesRegex(KeyError, "GLOSA_INTERV_Q_PPAL"):
            MarcadorColecistectomia().ejecutar(sin_glosa)

    def test_encadenadas_en_pipeline_dan_lo_mismo_que_transformar(self):
        entrada = egresos_de_prueba()
        etapas = [
            FiltroColelitiasis(),
            AsignadorProvincia(),
            MarcadorGruposRiesgo(),
            MarcadorColecistectomia(),
        ]
        resultado = Pipeline(etapas).ejecutar(entrada)
        assert_frame_equal(
            resultado.reset_index(drop=True),
            tr.transformar(entrada).reset_index(drop=True),
        )

class TestMarcadorAprende(unittest.TestCase):
    """El marcador aprende el vocabulario en ajustar() y lo aplica en ejecutar()."""

    def test_aprende_el_vocabulario_de_los_datos(self):
        datos = pd.DataFrame({"GLOSA_INTERV_Q_PPAL": [
            "Colecistectomía laparoscópica", "Apendicectomía", None,
            "Colecistectomía laparoscópica",
        ]})
        marcador = MarcadorColecistectomia().ajustar(datos)
        self.assertEqual(marcador.vocabulario,
                         frozenset({"Colecistectomía laparoscópica"}))

    def test_aplica_lo_aprendido_a_datos_nuevos(self):
        entrenamiento = pd.DataFrame({"GLOSA_INTERV_Q_PPAL": ["Colecistectomía abierta"]})
        nuevos = pd.DataFrame({"GLOSA_INTERV_Q_PPAL": [
            "Colecistectomía abierta", "Colecistectomía robótica",
        ]})
        marcador = MarcadorColecistectomia().ajustar(entrenamiento)
        marcas = marcador.ejecutar(nuevos)["FLAG_COLECISTECTOMIA"].tolist()
        self.assertEqual(marcas, [True, False])   # la glosa no vista no se marca

    def test_consultar_antes_de_ajustar_lanza_error(self):
        with self.assertRaises(RuntimeError):
            MarcadorColecistectomia().vocabulario


if __name__ == "__main__":
    unittest.main()
