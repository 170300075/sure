######################################
#           Bibliotecas              #
######################################
from fastapi import APIRouter, HTTPException
import pandas as pd

######################################
#           Dependencias             #
######################################
from config.database import db
from config.utilities import dataframe2Dict, dataframe, fetch

######################################
#           Modelos                  #
######################################

indicators = APIRouter(
    tags = ["Indicadores de rendimiento escolar"]
)

@indicators.get("/indicators/{id_user}/period_averages")
def get_indicators(id_user):
    """
    Permite obtener los principales indicadores de promedio del estudiante:
    * `prom_general`: es el promedio general del estudiante obtenido a partir de todas
    las asignaturas cuantitativas en cada periodo.
    * `prom_per_prev`: es el promedio que el estudiante obtuvo en el penultimo periodo.
    """

    promedios = dataframe("grades/" + id_user + "/averages")
    prom_per_prev = promedios.loc[1, "average_grades"]
    prom_general = promedios.loc[1::, "average_grades"]
    prom_general = prom_general.mean()
    return({"prom_general" : prom_general, "prom_per_prev" : prom_per_prev})