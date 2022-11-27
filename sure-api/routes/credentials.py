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

credentials = APIRouter(
    tags = ["Validación de credenciales"]
)

@credentials.post("/credentials")
def validate_credentials(id_user : str, password : str):
    """
    Permite validar las credenciales del estudiante a partir 
    de la matrícula y la contraseña. Regresa `true` si las credenciales
    son correctas, `false` si no son correctas, y un mensaje de error `message`
    explicando que el usuario no está registrado en las bases de datos.
    """
    credentials = db.users.find_one({"id_user" : id_user}, {"_id" : 0, "password" : 1})
    if credentials is not None:
        if password == credentials["password"]:
            return(True)
        else:
            return(False)
    else:
        return({"message" : "Usuario no registrado en la base de datos"})