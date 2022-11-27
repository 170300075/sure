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

payments = APIRouter(
    tags = ["Pagos"]
)

@payments.get("/payments/{id_user}")
async def read_payments(id_user : str):
    """
    Endpoint para obtener el registro de pagos del estudiante,
    se toma como parametro su matricula.
    """
    data = db.payments.find_one({"id_user" : id_user}, {"_id" : 0, "payments" : 1})["payments"]
    # print(data)
    return data


@payments.get("/payments/{id_user}/last_updated")
async def read_payments_last_update(id_user : str):
    """
    Endpoint para obtener la última fecha de actualización de los registros de pagos del estudiante
    """
    data = db.payments.find_one({"id_user" : id_user}, {"_id" : 0, "last_updated" : 1})["last_updated"]

    return(data)