# Validación del dataset — MCDI500

**Archivo:** `egresos_araucania_k80_transformado.csv` · 3789 filas × 23 columnas

## Perfil de variables

| variable | dtype | rol | unicos | pct_nulos |
| --- | --- | --- | --- | --- |
| PERTENENCIA_ESTABLECIMIENTO_SALUD | str | binaria | 2 | 0.0 |
| SEXO | str | binaria | 2 | 0.0 |
| GRUPO_EDAD | str | fecha | 10 | 0.0 |
| ETNIA | str | binaria | 2 | 0.0 |
| GLOSA_PAIS_ORIGEN | str | binaria | 2 | 0.0 |
| COMUNA_RESIDENCIA | str | fecha | 32 | 0.0 |
| GLOSA_COMUNA_RESIDENCIA | str | alta cardinalidad | 32 | 0.0 |
| REGION_RESIDENCIA | str | fecha | 1 | 0.0 |
| GLOSA_REGION_RESIDENCIA | str | nominal | 1 | 0.0 |
| PREVISION | str | nominal | 6 | 0.0 |
| GLOSA_PREVISION | str | nominal | 6 | 0.0 |
| ANO_EGRESO | str | fecha | 1 | 0.0 |
| DIAG1 | str | nominal | 7 | 0.0 |
| DIAG2 | str | vacía | 0 | 100.0 |
| DIAS_ESTADA | int64 | discreta | 45 | 0.0 |
| CONDICION_EGRESO | int64 | binaria | 2 | 0.0 |
| GLOSA_INTERV_Q_PPAL | str | alta cardinalidad | 24 | 18.0 |
| GLOSA_PROCED_PPAL | str | texto libre | 10 | 95.0 |
| PROVINCIA_RESIDENCIA | str | binaria | 2 | 0.0 |
| GRUPO_RIESGO_MUJER | str | binaria | 2 | 0.0 |
| GRUPO_RIESGO_ETNIA | str | binaria | 2 | 0.0 |
| GRUPO_RIESGO_40_49 | str | binaria | 2 | 0.0 |
| FLAG_COLECISTECTOMIA | str | binaria | 2 | 0.0 |

## Requisitos del curso

| estado | requisito | detalle |
| --- | --- | --- |
| OK | Al menos 2000 filas | 3789 filas |
| OK | Al menos 12 columnas | 23 columnas |
| OK | Combina al menos 3 roles analíticos | binaria, fecha, nominal, alta cardinalidad, discreta, texto libre |
| OK | Al menos una variable numérica | 1 numéricas (continuas o discretas) |
| OK | Al menos una variable categórica | 14 categóricas (nominales, binarias u ordinales) |
| OK | Presencia de valores faltantes | máximo 100.0% en una variable |
| AVISO | Ninguna variable sobre 60% de faltantes | máximo 100.0% |
| OK | Incluye alguna variable de fecha | 4 detectadas |
| OK | Incluye texto o categórica de alta cardinalidad | 3 detectadas |
| OK | Archivo bajo 100 MB | 1.0 MB |
| AVISO | Sin filas duplicadas exactas | 1276 duplicadas |

## Resultado

El conjunto **cumple** los requisitos mínimos.