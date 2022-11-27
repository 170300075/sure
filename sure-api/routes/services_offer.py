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

services_offer = APIRouter(
    tags = ["Servicio social"]
)

@services_offer.get("/social_service/")
def read_social_service():
    """
    Endpoint para obtener la oferta del servicio social. Este endpoint no requiere parámetros adicionales
    """
    data = []
    data.extend(fetch("social_service/internal"))
    data.extend(fetch("social_service/external"))
    return data

@services_offer.get("/social_service/last_updated")
async def read_social_service_last_updated():
    """
    Endpoint para obtener la última fecha de actualización
    de la oferta de servicio social
    """

    data = db.service_offer.find_one({}, {"_id" : 0, "last_updated" : 1})["last_updated"]
    print(data)
    return(data)

@services_offer.get("/social_service/{project_type}")
async def read_social_service_offer(project_type : str):
    """
    Endpoint para obtener la oferta del servicio social de acuerdo al tipo de proyecto 
    que se pasa como parámetro; internal (para proyectos internos) o external (para proyectos externos).
    """
    if project_type == "internal":
        data = db.service_offer.find_one({}, {"_id" : 0, "internal_projects.aditional_information" : 0})["internal_projects"]
        return data
    elif project_type == "external":
        data = db.service_offer.find_one({}, {"_id" : 0, "external_projects.aditional_information" : 0})["external_projects"]
        return data
    else:
        raise HTTPException(status_code = 404, detail = "Resource Not Found")