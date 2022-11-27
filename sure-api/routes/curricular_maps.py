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

curricular_maps = APIRouter(
    tags = ["Mapas curriculares"]
)

@curricular_maps.get("/curricular_map/{program}")
def get_curricular_map(program : str):
    """
    Endpoint para obtener el mapa curricular de una carrera, 
    requiere como parámetro la clave del programa del mapa curricular
    """

    if program == "2016ID":
        # Leemos la tabla del mapa curricular ideal
        curricular_map = pd.read_excel("Mapas curriculares.xlsx", sheet_name = "2016ID")
        # Mostramos las asignaturas del mapa curricular ideal
        return(dataframe2Dict(curricular_map))
    else:
        return("Program not found")

@curricular_maps.get("/validation/{program}")
def get_validation_table(program : str):
    """
    Endpoint para obtener la tabla de validación. Está permite visualizar los créditos máximos y 
    los necesarios por ciclo, periodo y tipo de asignatura.
    """
    if program == "2016ID":
        # Leemos la tabla de validación de asignaturas
        validation_table = pd.read_excel("Mapas curriculares.xlsx", sheet_name = "Créditos requeridos")
        return(dataframe2Dict(validation_table))
    else:
        return("Program not found")