# Fase 3 · Núcleo algorítmico y programación orientada a objetos

**Grupo 2 · MCDI500 · Programación para la Ciencia de Datos**

La Fase 3 reutiliza las transformaciones de los egresos hospitalarios de La Araucanía de 2022. El pipeline aplica etapas de filtrado y transformación en orden. El cálculo de proporciones compara tres implementaciones para estimar, por grupo de riesgo y provincia, la proporción de egresos por colelitiasis con colecistectomía registrada. La unidad de análisis es el egreso hospitalario.

## Archivos principales

| Archivo | Función |
| --- | --- |
| [`src/base.py`](../src/base.py) y [`src/pipeline.py`](../src/pipeline.py) | Definen el contrato de las etapas y su ejecución ordenada. |
| [`src/transformacion.py`](../src/transformacion.py) | Reúne las funciones reutilizadas de Fase 2. |
| [`src/etapas.py`](../src/etapas.py) | Implementa FiltroColelitiasis, AsignadorProvincia, MarcadorGruposRiesgo y MarcadorColecistectomia, reutilizando las funciones de transformación. |
| [`src/proporciones.py`](../src/proporciones.py) | Implementa las estrategias de cálculo con bucle de Python, agrupación con pandas y máscaras de NumPy. |
| [`tests/test_pipeline.py`](../tests/test_pipeline.py) | Verifica el contrato, el flujo, los casos límite y el manejo de errores. |
| [`docs/arquitectura_f3.md`](../docs/arquitectura_f3.md) | Presenta el diagrama de clases y explica herencia, polimorfismo, encapsulamiento y el patrón Pipeline. |
| [`F3_02_eficiencia.ipynb`](F3_02_eficiencia.ipynb) | Verifica la equivalencia de las estrategias y compara su tiempo y memoria. |

## Entorno

Ejecuta los comandos desde la raíz de una copia del repositorio. Usa Python 3.13 y el archivo [`requirements.txt`](../requirements.txt), que fija las versiones de pandas, NumPy, Matplotlib, Seaborn, JupyterLab e ipykernel.

**macOS o Linux**

```bash
python3.13 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m ipykernel install --user --name grupo2-mcdi500 --display-name "Python (grupo2-mcdi500)"
python -m jupyterlab
```

**Windows (PowerShell)**

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m ipykernel install --user --name grupo2-mcdi500 --display-name "Python (grupo2-mcdi500)"
.\.venv\Scripts\python.exe -m jupyterlab
```

Si el repositorio ya tiene un entorno `.venv`, empieza por la instalación de dependencias usando el Python de ese entorno. El comando de registro deja disponible el kernel del entorno con el nombre **Python (grupo2-mcdi500)**. En JupyterLab, selecciona **Python (grupo2-mcdi500)** y abre los notebooks mediante el explorador de archivos dentro de **`F3/`**. En particular, `F3_01` calcula las rutas a partir de ese directorio.

## Datos de entrada

- [`egresos_araucania_2022.csv`](../data/processed/egresos_araucania_2022.csv) es el subconjunto regional generado en [F2_01](../F2/F2_01_obtencion.ipynb).
- [`egresos_araucania_k80_transformado.csv`](../data/processed/egresos_araucania_k80_transformado.csv) contiene el subconjunto de egresos por colelitiasis generado en [F2_03](../F2/F2_03_transformacion.ipynb).

Los dos CSV están en `data/processed/`. Son suficientes para ejecutar los notebooks de Fase 3. Si necesitas reconstruirlos desde la fuente DEIS, sigue las instrucciones del [README principal](../README.md#obtención-de-los-datos).

## Ejecución de los notebooks

Abre cada notebook en JupyterLab, reinicia el kernel y ejecuta todas sus celdas desde el inicio.

| Notebook | Entrada | Resultado esperado |
| --- | --- | --- |
| `F3_01_nucleo_poo.ipynb` | CSV regional y CSV transformado de Fase 2. | Transforma el conjunto regional con las etapas del pipeline. Comprueba la igualdad frente a `transformar()` y frente a un recorrido recursivo. También contrasta las cinco columnas derivadas con el CSV de F2_03 y calcula las proporciones con NumPy. |
| [`F3_02_eficiencia.ipynb`](F3_02_eficiencia.ipynb) | CSV transformado de F2_03. Puede ejecutarse con ese archivo directamente. | Compara las tres estrategias de cálculo y comprueba que arrojen los mismos resultados. Verifica **3.789 egresos por colelitiasis** y **3.056 con colecistectomía registrada (80,7 %)**. Los tiempos pueden variar según el equipo. |

`F3_02` puede ejecutarse en `main`. `F3_01` y las cuatro etapas de `src/etapas.py` están disponibles en la rama [`feat/f3-01-integracion`](https://github.com/PaulaBecerraV/proyecto-grupo2-mcdi500/tree/feat/f3-01-integracion). El diagrama de clases se incorpora mediante el [PR #6](https://github.com/PaulaBecerraV/proyecto-grupo2-mcdi500/pull/6). Después de integrar la rama del notebook, el orden sugerido de lectura y ejecución es `F3_01` para el flujo general y `F3_02` para el detalle de la comparación de rendimiento.

## Pruebas del pipeline

Desde la raíz del repositorio y con el entorno del proyecto activo:

```bash
python -m unittest discover -s tests -p test_pipeline.py -v
```

En Windows, si el entorno no está activado, sustituye `python` por `.\.venv\Scripts\python.exe`. Se esperan nueve pruebas aprobadas con datos sintéticos. Para revisar el diseño inicial y su integración en F3, consulta [`README_esqueleto.md`](README_esqueleto.md) y el [PR #2](https://github.com/PaulaBecerraV/proyecto-grupo2-mcdi500/pull/2).
