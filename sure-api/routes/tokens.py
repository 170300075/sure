######################################
#           Bibliotecas              #
######################################
from fastapi import APIRouter, HTTPException
import pandas as pd
from datetime import datetime, timedelta
import secrets

######################################
#           Dependencias             #
######################################
from config.database import db
from config.utilities import dataframe2Dict, dataframe, fetch

######################################
#           Modelos                  #
######################################

tokens = APIRouter(
    tags = ["Tokens"]
)

@tokens.post("/token")
def generate_token(id_user):
    """
    Permite generar un token para la sesión del estudiante
    """
    # Generar un token
    secret = secrets.token_urlsafe()
    
    # Guardar metadatos del token
    token = {
        "token" : secret,
        "id_user" : id_user,
        "creation_date" : datetime.utcnow(),
        "expiration_date" : datetime.utcnow() + timedelta(minutes = 30)
    }
    
    # Almacenamos el token en la base de datos
    db.tokens.replace_one({"id_user" : id_user}, token, upsert = True)

    return(token["token"])

@tokens.post("/token/validate")
def validate_token(token : str):
    """
    Permite validar un token. Regresa:
    * `message`: un mensaje de error  si el token no 
    fue encontrado en la base de datos, o si el token ha expirado.
    * `id_user`: devuelve la matrícula del estudiante al que pertenece el token en un string.
    """
    data = db.tokens.find_one({"token" : token}, {"_id" : 0, "id_user" : 1, "expiration_date" : 1})
    # Si encuentra un token
    if data is not None:
        # Revisar token no haya caducado
        if data["expiration_date"] > datetime.now():
            return(data["id_user"])
        else:
            return({"message" : "token expirado"})
    else:
        return({"message" : "token no encontrado"})