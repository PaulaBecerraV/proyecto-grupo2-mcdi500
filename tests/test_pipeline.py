"""Pruebas del contrato y del pipeline; ejecutar desde la raíz del repositorio.

Comando: python -m unittest discover -s tests -p test_pipeline.py -v
Las clases auxiliares de este archivo son ejemplos exclusivos de prueba.
"""

import unittest

import pandas as pd
from pandas.testing import assert_frame_equal

from src.base import EtapaBase
from src.pipeline import Pipeline
from src import transformacion as tr


class SumarUno(EtapaBase):
    def ejecutar(self, datos):
        return datos.assign(valor=datos["valor"] + 1)


class Duplicar(EtapaBase):
    def ejecutar(self, datos):
        return datos.assign(valor=datos["valor"] * 2)


class EtapaFuncionDePrueba(EtapaBase):
    """Adapta funciones existentes solo para comprobar la integración."""

    def __init__(self, funcion):
        self.funcion = funcion

    def ejecutar(self, datos):
        return self.funcion(datos)


class TestPipeline(unittest.TestCase):
    def test_ejecuta_en_orden_y_preserva_la_entrada(self):
        entrada = pd.DataFrame({"valor": [1, 3]})
        original = entrada.copy()
        resultado = Pipeline([SumarUno(), Duplicar()]).ejecutar(entrada)
        assert_frame_equal(resultado, pd.DataFrame({"valor": [4, 8]}))
        assert_frame_equal(entrada, original)

    def test_acepta_dataframe_sin_filas(self):
        entrada = pd.DataFrame({"valor": pd.Series(dtype="int64")})
        resultado = Pipeline([SumarUno(), Duplicar()]).ejecutar(entrada)
        assert_frame_equal(resultado, entrada)

    def test_exige_implementar_metodo_abstracto(self):
        with self.assertRaises(TypeError):
            EtapaBase()

    def test_rechaza_pipeline_sin_etapas(self):
        with self.assertRaisesRegex(ValueError, "al menos una etapa"):
            Pipeline([])

    def test_rechaza_objeto_que_no_es_etapa(self):
        with self.assertRaisesRegex(TypeError, "heredar de EtapaBase"):
            Pipeline([object()])

    def test_rechaza_entrada_incorrecta(self):
        with self.assertRaisesRegex(TypeError, "entrada debe ser un DataFrame"):
            Pipeline([SumarUno()]).ejecutar([1, 2])

    def test_rechaza_salida_incorrecta(self):
        etapa = EtapaFuncionDePrueba(lambda datos: None)
        with self.assertRaisesRegex(TypeError, "debe devolver un DataFrame"):
            Pipeline([etapa]).ejecutar(pd.DataFrame())

    def test_detiene_el_flujo_ante_una_excepcion(self):
        pasos_posteriores = []

        def fallar(datos):
            raise KeyError("Falta una columna requerida.")

        def posterior(datos):
            pasos_posteriores.append(True)
            return datos

        flujo = Pipeline([
            EtapaFuncionDePrueba(fallar),
            EtapaFuncionDePrueba(posterior),
        ])
        with self.assertRaisesRegex(KeyError, "columna requerida"):
            flujo.ejecutar(pd.DataFrame())
        self.assertEqual(pasos_posteriores, [])

    def test_conecta_las_funciones_existentes_de_f2(self):
        entrada = pd.DataFrame({
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
        original = entrada.copy()
        funciones = [
            tr.filtrar_colelitiasis,
            tr.asignar_provincia,
            tr.marcar_grupos_riesgo,
            tr.marcar_colecistectomia,
        ]
        flujo = Pipeline([EtapaFuncionDePrueba(f) for f in funciones])
        resultado = flujo.ejecutar(entrada)

        assert_frame_equal(resultado, tr.transformar(entrada))
        assert_frame_equal(entrada, original)
        self.assertEqual(len(resultado), 3)
        self.assertEqual(resultado["FLAG_COLECISTECTOMIA"].tolist(), [True, False, False])


if __name__ == "__main__":
    unittest.main()
