# F3 · Primera entrega de Michael: clase base y pipeline

Estado: esqueleto funcional revisado el 12 de noviembre de 2026 contra el
enunciado de F3 y la «Rúbrica sumativa 3 fase 3» (69 puntos). Es una entrega
parcial para coordinar el trabajo: falta acordar los nombres con el equipo e
integrar las clases concretas, los cálculos y el notebook final.

## Archivos entregados

| Archivo | Función |
| --- | --- |
| `src/base.py` | Define `EtapaBase`, la clase abstracta común. |
| `src/pipeline.py` | Define `Pipeline`, que conecta objetos de las etapas en orden. |
| `tests/test_pipeline.py` | Comprueba el flujo, casos límite, errores y conexión con las funciones de F2. |
| `F3/README_esqueleto.md` | Explica el acuerdo de integración propuesto y cómo comprobarlo. |

Se agregan estos archivos al repositorio existente. Se conserva
`src/transformacion.py`, del que dependen las pruebas de integración.
Este archivo es una guía del esqueleto; el README final de F3 debe actualizarse
cuando existan las clases específicas, los cálculos y el notebook integrado.

## Acuerdo propuesto para Sebastián y Coni

1. Cada etapa hereda de `EtapaBase`: `from src.base import EtapaBase`.
2. Implementa `ejecutar(self, datos)`: recibe un DataFrame y devuelve otro.
3. Trabaja sobre una copia, sin modificar la entrada recibida.
4. Informa con una excepción clara si faltan columnas necesarias.
5. El pipeline recibe objetos de las etapas ya creados, en el orden deseado.

Las cuatro clases de transformación de Sebastián pueden reutilizar las funciones
de `src/transformacion.py`. No hace falta duplicar sus reglas en el notebook.
La clase de cálculo de Coni puede devolver un DataFrame de resultados y situarse
al final del flujo. El esquema de esa tabla debe acordarse antes de la integración.

## Relación con el enunciado y la rúbrica

| Requisito | Evidencia en esta entrega | Pendiente para el trabajo completo |
| --- | --- | --- |
| Codificación y flujo de datos | `Pipeline.ejecutar` conecta las salidas con las entradas y valida el tipo de resultado. | Ejecutar y exportar el resultado de las etapas definitivas con los datos reales. |
| Diseño estructurado | La clase base establece el contrato; el pipeline coordina y las subclases realizan cada tarea. | Integrar el cálculo elegido y documentar sus decisiones. |
| Herencia | `EtapaBase` permite definir subclases con un método común obligatorio. | Las cuatro clases concretas de transformación y la clase de cálculo. |
| Polimorfismo | El pipeline llama a `etapa.ejecutar(datos)` para distintas clases, demostrado con las etapas de prueba. | Demostrar el mismo uso con las etapas reales en el notebook F3. |
| Encapsulamiento | El orden se almacena en `_etapas` como tupla y se consulta mediante la propiedad `etapas`, sin setter. | Mantener las reglas y parámetros de cada transformación en su clase. |
| Validación | Nueve pruebas del mecanismo, con casos normales, límite y excepciones. | Pruebas de las clases definitivas y comparación con F2_03 sobre los datos reales. |
| Documentación | Contrato, ejemplo de integración, métodos documentados y fuentes técnicas. | Diagrama de clases, evidencias del notebook, informe y README final. |

Esta correspondencia describe la contribución del esqueleto; no acredita por sí
sola el cumplimiento completo de cada criterio ni anticipa su puntaje.

### Decisiones de diseño

- Se usa `ABC` y `abstractmethod` para exigir que las subclases implementen
  `ejecutar`. La rúbrica exige herencia, pero no impone una clase abstracta: esta
  es una elección del diseño propuesto (Python Software Foundation, s. f.-a).
- Se utiliza composición: el pipeline contiene objetos de las etapas. Su
  responsabilidad es coordinarlas; las reglas de colelitiasis, provincia y
  cirugía permanecen en las transformaciones.
- El atributo `_etapas` es interno por convención de Python. La tupla impide
  agregar o quitar elementos de esa secuencia mediante la propiedad, pero no
  convierte en inmutables los objetos de las etapas (Python Software Foundation,
  s. f.-b).
- El pipeline utiliza un bucle porque conecta una secuencia de pasos. La rúbrica
  de diseño admite «recursividad o división funcional», pero el enunciado también
  pide evidenciar programación recursiva en el notebook: debe coordinarse esa
  evidencia en el trabajo algorítmico del equipo, sin forzar recursividad en este
  coordinador. Una opción a evaluar es incluir una versión recursiva entre las
  implementaciones comparadas por Coni.
- Las pruebas utilizan `unittest`, que permite ejecutar los casos en conjunto
  mediante un comando (Python Software Foundation, s. f.-c).

### Pendientes del equipo que afectan la integración

- Comparar implementaciones con mediciones reproducibles de tiempo y análisis
  de memoria, y justificar la elección final. Esta entrega no mide eficiencia.
- Mantener los criterios de F2 para faltantes, desconocidos y egresos repetidos.
  Los indicadores booleanos de riesgo no sustituyen las variables originales:
  antes de comparar grupos se deben excluir los desconocidos en la variable
  correspondiente, según la definición operacional del proyecto.
- Hacer que el notebook guarde la tabla devuelta por el pipeline, evitando una
  segunda transformación independiente en sus celdas.
- Actualizar las dependencias y registrar una ejecución completa en el entorno
  del proyecto antes de la entrega final.

## Ejemplo mínimo para construir una etapa

Este ejemplo ilustra el contrato; no sustituye las cuatro clases que implementará
Sebastián. Ejecutar desde la raíz del repositorio o en un notebook con esa raíz
añadida al entorno de importación.

```python
import pandas as pd
from src.base import EtapaBase
from src.pipeline import Pipeline
from src.transformacion import filtrar_colelitiasis


class FiltroDeEjemplo(EtapaBase):
    def ejecutar(self, datos):
        return filtrar_colelitiasis(datos)


datos = pd.DataFrame({"DIAG1": ["K802", "J189", "K808"]})
flujo = Pipeline([FiltroDeEjemplo()])
resultado = flujo.ejecutar(datos)
print(resultado)
```

Resultado esperado: dos filas, con los diagnósticos `K802` y `K808`.

## Uso desde un notebook situado en F3

Reutilizar la lógica de rutas del proyecto antes de importar los módulos:

```python
import sys
from pathlib import Path

RAIZ = Path.cwd()
if RAIZ.name == "F3":
    RAIZ = RAIZ.parent
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))
```

## Pruebas

Con el entorno del proyecto activo y desde la raíz del repositorio:

```bash
python -m unittest discover -s tests -p test_pipeline.py -v
```

Las pruebas usan `unittest` de la biblioteca estándar y pandas, ya utilizado por
el proyecto; no requieren instalar pytest. Cubren nueve escenarios: orden de
ejecución y conservación de la entrada, tabla sin filas, clase abstracta,
pipeline sin etapas, objeto inválido, entrada inválida, salida inválida,
interrupción ante un error y conexión con las funciones de F2 usando datos
sintéticos. La comparación con todos los registros reales y las pruebas de las
clases definitivas corresponden a la siguiente integración.

## Límites de esta primera entrega

- No incluye las cuatro clases finales de Sebastián ni la clase de cálculo de Coni.
- No modifica F1/F2 ni sus resultados; conserva sus criterios de transformación.
- No corrige el archivo de dependencias ni acredita instalación en otros sistemas.
- El flujo devuelve la tabla: el notebook integrado deberá exportar ese resultado.
- La revisión de la rúbrica no sustituye la revisión del código y la integración
  por parte de los integrantes del equipo.

## Subida sugerida por GitHub

Crear una rama `feat/base-pipeline-f3`, agregar los archivos conservando sus
carpetas, usar un mensaje como `feat: agrega clase base y pipeline de F3` y abrir
un pull request hacia `main` para que Paula revise la integración. Compartir el
enlace a la rama o al PR con Sebastián permite que empiece antes de la integración.

Para explicar tu aporte: la clase base establece un método común; el pipeline
coordina los objetos sin necesitar conocer las reglas internas de cada etapa.

## Verificación de esta entrega

Las nueve pruebas pasaron en Python 3.12.14 y pandas 2.2.3, en Linux. Se usaron datos sintéticos y el módulo existente de F2. No se ejecutó el dataset completo ni se comprobó la instalación en macOS o Windows.

## Referencias técnicas de este esqueleto

Estas referencias deben integrarse con las fuentes docentes y académicas del
informe. Por sí solas no cubren la combinación exigida de al menos dos fuentes
docentes, dos técnicas oficiales y una académica complementaria.

Python Software Foundation. (s. f.-a). *abc — Abstract base classes*. Python documentation. https://docs.python.org/3/library/abc.html

Python Software Foundation. (s. f.-b). *Classes*. Python documentation. https://docs.python.org/3/tutorial/classes.html

Python Software Foundation. (s. f.-c). *unittest — Unit testing framework*. Python documentation. https://docs.python.org/3/library/unittest.html
