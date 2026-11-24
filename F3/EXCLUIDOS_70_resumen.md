# Verificación de los 70 egresos excluidos por región enmascarada (*)

**Fase 2 · Filtro por región · La Araucanía 2022 (DEIS)**

El filtro por región de la Fase 2 excluyó **70 egresos** por colelitiasis (K80.0–K80.8)
cuya **comuna** corresponde a La Araucanía pero cuya **región viene enmascarada (`*`)**
en la base nacional. Este archivo resume su composición para poder verificar la
decisión **sin necesidad de descargar la base nacional** (que no se versiona en el repo).

## Total

| Concepto | Valor |
|---|---|
| Egresos excluidos por región `*` con comuna de La Araucanía | **70** |

## Por provincia

| Provincia | Excluidos |
|---|---|
| Cautín | 64 |
| Malleco | 6 |

## Por grupo de riesgo

| Grupo de riesgo | Excluidos que pertenecen |
|---|---|
| Mujer | 0 |
| Se identifica con etnia | 0 |
| 40 a 49 años | 0 |

## Conclusión

Los 70 excluidos tienen **sexo, etnia y grupo de edad enmascarados (`*`)**, por lo que
ninguno puede clasificarse dentro de los grupos de riesgo del estudio (de ahí los tres 0).
Excluirlos **no afecta** el análisis por grupos de riesgo, porque no aportaban casos a
ninguno de ellos. La verificación es reproducible desde la sección 9 del notebook
`F3/F3_02_eficiencia.ipynb`.
