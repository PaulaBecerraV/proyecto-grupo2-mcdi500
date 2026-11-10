# Proyecto Grupo 2 · MCDI500

**Colecistectomía en grupos de riesgo de cáncer de vesícula, La Araucanía 2022**

Proyecto del curso "Programación para la Ciencia de Datos" del programa de Magister en Inteligencia Artificial y Ciencia de Datos de la Universidad Andrés Bello, Santiago, Chile. 
Este repositorio usa los egresos hospitalarios abiertos del Departamento de Estadísticas e Información de Salud (DEIS - MINSAL) para preparar el análisis de la proporción de egresos por colelitiasis con colecistectomía registrada en las provincias de Cautín y Malleco durante el año 2022.

## Estructura del repositorio

| Ruta | Contenido |
| --- | --- |
| [`F1/`](F1/) | Definición del problema, pregunta, objetivos y verificación del entorno. |
| [`F2/`](F2/) | Obtención, exploración, transformación y validación de los datos. |
| `F3/` y `F4/` | Carpetas para las siguientes fases del proyecto. |
| `src/` | Carpeta reservada para funciones reutilizables del proyecto. |
| `data/raw/` | Ubicación local del CSV nacional del DEIS. |
| [`data/processed/`](data/processed/) | CSV regional y CSV transformado de egresos por colelitiasis. |
| [`docs/`](docs/) | [Diccionario de variables](docs/diccionario_variables.md), [validación de la base nacional](docs/validacion_dataset.md) y [validación del subconjunto final](docs/validacion_colelitiasis.md). |
| [`validar_dataset.py`](validar_dataset.py) | Script del curso que genera el perfil de variables y comprueba los requisitos del conjunto de datos. |
| [`requirements.txt`](requirements.txt) | Versiones de las dependencias del entorno. |

## Entorno y dependencias

El proyecto se desarrolló con **Python 3.13** y **JupyterLab**. Las bibliotecas principales son pandas, NumPy, Matplotlib y Seaborn. Los comandos siguientes se ejecutan desde la raíz de una copia local del repositorio, donde están este README y `requirements.txt`. Puedes obtenerla con `git clone https://github.com/PaulaBecerraV/proyecto-grupo2-mcdi500.git` y entrar a la carpeta con `cd proyecto-grupo2-mcdi500`.

**Windows (PowerShell)**

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\jupyter-lab.exe
```

**macOS o Linux (Terminal)**

```bash
python3.13 -m venv .venv
source .venv/bin/activate
awk '!/^pywinpty==/' requirements.txt > .venv/requirements-posix.txt
python -m pip install -r .venv/requirements-posix.txt
jupyter lab
```

El listado de dependencias se generó en Windows. El paso con `awk` crea una copia local que omite `pywinpty`, una dependencia específica de Windows. Para ejecutar los notebooks, selecciona el kernel de Python del entorno `.venv` y ejecuta todas las celdas en el orden indicado abajo.

## Obtención de los datos

1. Descargar el [ZIP oficial de egresos hospitalarios 2022 del DEIS](https://repositoriodeis.minsal.cl/DatosAbiertos/EGRESOS/EGRESOS_2022.zip).
2. Extraer `EGRE_DATOS_ABIERTOS_2022.csv` y guardar como `data/raw/EGRE_DATOS_ABIERTOS_2022.csv`.
3. Ejecutar F2_01 para generar el subconjunto regional.

El CSV nacional y su ZIP se excluyen del control de versiones mediante `.gitignore`. Los dos CSV de `data/processed/` están disponibles en el repositorio. Si se usa esas copias, se puede ejecutar F2_02, F2_03 o F2_04 directamente con el archivo de entrada que indica la tabla.

## Orden de ejecución

| Paso | Notebook | Entrada | Resultado |
| --- | --- | --- | --- |
| 1 | [`F1_01_definicion.ipynb`](F1/F1_01_definicion.ipynb) | Entorno de Python | Pregunta y objetivos del proyecto, junto con las versiones del entorno. |
| 2 | [`F2_01_obtencion.ipynb`](F2/F2_01_obtencion.ipynb) | `data/raw/EGRE_DATOS_ABIERTOS_2022.csv` | `data/processed/egresos_araucania_2022.csv` con **84.618 egresos y 18 variables**. |
| 3 | [`F2_02_exploracion.ipynb`](F2/F2_02_exploracion.ipynb) | `data/processed/egresos_araucania_2022.csv` | Tablas y gráficos de exploración en el notebook. |
| 4 | [`F2_03_transformacion.ipynb`](F2/F2_03_transformacion.ipynb) | `data/processed/egresos_araucania_2022.csv` | `data/processed/egresos_araucania_k80_transformado.csv` con **3.789 egresos y 23 variables**. Incluye provincia, grupos de riesgo e indicador de colecistectomía registrada. |
| 5 | [`F2_04_validacion.ipynb`](F2/F2_04_validacion.ipynb) | `data/processed/egresos_araucania_k80_transformado.csv` | Comprobaciones del subconjunto final e informe `docs/validacion_colelitiasis.md`. |

**Ruta de F2_02.** La variable `RUTA` de la primera celda apunta al CSV desde la raíz del repositorio. Si el directorio de trabajo del kernel es `F2/`, usar `RUTA = "../data/processed/egresos_araucania_2022.csv"` en copia local antes de ejecutar el notebook.

## Fuente y limitaciones

Para consultar y descargar las bases de datos de egresos hospitalarios correspondientes a otros años, visitar el [portal de Datos Abiertos del DEIS](https://deis.minsal.cl/#datosabiertos).

**Limitaciones relacionadas con la completitud de los datos:** Las bases de datos del DEIS pueden presentar campos sin información en variables relevantes, como la región de residencia. Esta situación debe considerarse al realizar análisis desagregados territorialmente, ya que puede ocasionar una subestimación de los egresos atribuidos a cada región.
