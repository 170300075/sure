import pandas as pd
import requests
import json
from urllib import response

from config.database import base_url

def dataframe2Dict(dataframe):
    """
    Esta funcion permite convertir un dataframe a
    un diccionario (JSON like)
    """
    # Convertir una dataframe a un diccionario
    data_dict = dataframe.to_dict("records")
    # Retornamos el diccionario
    return(data_dict)

def fetch(endpoint = ""):
    # En caso de deploy, cambiar por ruta de producción
    root = base_url
    # root = "https://sure-api.herokuapp.com/"

    res = requests.get(root+endpoint)
    res = json.loads(res.text)
    return(res)


def fetch_post(endpoint = ""):
    root = base_url
    res = requests.post(root+endpoint)
    res = json.loads(res.text)
    return(res)

def post(endpoint, body):
    root = base_url
    res = requests.post(root+endpoint, data = json.dumps(body))
    res = json.loads(res.text)
    return(res)

def dataframe(endpoint):
    """
    Esta función permite obtener un dataframe 
    (si es posible) directamente de un endpoint.
    Toma como parámetro la ruta del endpoint.
    """
    dictionary = fetch(endpoint)
    return(pd.DataFrame(dictionary))