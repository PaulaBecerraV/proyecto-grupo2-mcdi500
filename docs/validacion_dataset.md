# Validación del dataset — MCDI500

**Archivo:** `EGRE_DATOS_ABIERTOS_2022.csv` · 1597118 filas × 18 columnas

## Perfil de variables

| variable | dtype | rol | unicos | pct_nulos |
| --- | --- | --- | --- | --- |
| PERTENENCIA_ESTABLECIMIENTO_SALUD | str | texto libre | 3 | 0.0 |
| SEXO | str | nominal | 4 | 0.0 |
| GRUPO_EDAD | str | fecha | 12 | 0.0 |
| ETNIA | str | nominal | 3 | 0.0 |
| GLOSA_PAIS_ORIGEN | str | nominal | 3 | 0.0 |
| COMUNA_RESIDENCIA | int64 | discreta | 348 | 0.0 |
| GLOSA_COMUNA_RESIDENCIA | str | alta cardinalidad | 348 | 0.0 |
| REGION_RESIDENCIA | object | fecha | 31 | 0.0 |
| GLOSA_REGION_RESIDENCIA | str | alta cardinalidad | 17 | 0.0 |
| PREVISION | object | fecha | 15 | 0.0 |
| GLOSA_PREVISION | str | nominal | 8 | 0.0 |
| ANO_EGRESO | object | fecha | 3 | 0.0 |
| DIAG1 | str | alta cardinalidad | 7119 | 0.0 |
| DIAG2 | str | alta cardinalidad | 1735 | 90.6 |
| DIAS_ESTADA | int64 | discreta | 740 | 0.0 |
| CONDICION_EGRESO | int64 | binaria | 2 | 0.0 |
| GLOSA_INTERV_Q_PPAL | str | texto libre | 1032 | 53.1 |
| GLOSA_PROCED_PPAL | str | texto libre | 491 | 87.3 |

## Requisitos del curso

| estado | requisito | detalle |
| --- | --- | --- |
| OK | Al menos 2000 filas | 1597118 filas |
| OK | Al menos 12 columnas | 18 columnas |
| OK | Combina al menos 3 roles analíticos | nominal, fecha, alta cardinalidad, texto libre, discreta, binaria |
| OK | Al menos una variable numérica | 2 numéricas (continuas o discretas) |
| OK | Al menos una variable categórica | 5 categóricas (nominales, binarias u ordinales) |
| OK | Presencia de valores faltantes | máximo 90.6% en una variable |
| AVISO | Ninguna variable sobre 60% de faltantes | máximo 90.6% |
| OK | Incluye alguna variable de fecha | 4 detectadas |
| OK | Incluye texto o categórica de alta cardinalidad | 7 detectadas |
| AVISO | Archivo bajo 100 MB | 341.4 MB |
| AVISO | Sin filas duplicadas exactas | 359464 duplicadas |

## Resultado

El conjunto **cumple** los requisitos mínimos.