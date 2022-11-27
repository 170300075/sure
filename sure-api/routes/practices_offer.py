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

practices_offer = APIRouter(
    tags = ["Prácticas profesionales"]
)

@practices_offer.get("/professional_practices/{id_subject}/{period}")
async def read_practices_offer(id_subject : str, period : str):
    """
    Endpoint para obtener la oferta de prácticas profesionales. Los dos parametros necesarios para 
    este son

    \n- `id_subject` (clave de la asignatura de prácticas que depende de si es Prácticas I, II o alguna de preespecialidad y de la carrera).
    \n- `period` (periodo para el que se consulta).
    """
    data = db.practices_offer.find_one({"id_offer" : id_subject, "period" : period}, {"_id" : 0, "offer" : 1})["offer"]
    return data

# Endpoint para obtener la última fecha de actualización de las prácticas profesionales
@practices_offer.get("/professional_practices/{id_subject}/{period}/last_updated")
async def read_practices_offer_last_updated(id_subject : str, period : str):
    """
    Endpoint para obtener la última fecha de actualización de las prácticas profesionales.
    Dado que existen varias ofertas, los parámetros necesarios son

    \n- `id_subject` (clave de la asignatura de prácticas que depende de si es Prácticas I, II o alguna de preespecialidad y de la carrera).
    \n- `period` (periodo para el que se consulta).
    """
    # Obtenemos la fecha de ultima actualizacion
    data = db.practices_offer.find_one({"id_offer" : id_subject, "period" : period}, {"_id" : 0, "last_updated" : 1})["last_updated"]
    return(data)

# Endpoint para obtener la lista de los periodos de ofertas de prácticas disponibles
@practices_offer.get("/professional_practices/periods")
async def read_practices_offer_list():
    """
    Endpoint para obtener la lista de asignaturas de prácticas y sus respectivos 
    periodos disponibles para las prácticas profesionales
    """
    data = list(db.practices_offer.find({}, {"_id" : 0, "id_offer" : 1, "period" : 1}))
    return(data)