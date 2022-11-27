######################################
#           Bibliotecas              #
######################################
from fastapi import APIRouter, HTTPException
import re

######################################
#           Dependencias             #
######################################
from config.database import db
from config.utilities import dataframe2Dict, dataframe, fetch


######################################
#           Modelos                  #
######################################

users = APIRouter(
    tags = ["Usuarios"]
)

@users.get("/users")
async def read_users():
    """
    Obtener las matriculas de todos los estudiantes
    registrados en la base de datos de SURE.
    """
    data = list(db.users.find({}, {"_id" : 0, "id_user" : 1}))
    return(data)

@users.get("/user/{id_user}")
async def read_user(id_user : str):
    """
    Obtener la información personal 
    de un estudiante a partir de su matrícula.
    """
    data = db.users.find_one({"id_user" : id_user}, {"_id" : 0})
    if data == None:
        raise HTTPException(status_code = 404, detail = "User Not Found")
    else:
        return data

@users.get("/user/{id_user}/study_plan")
def read_user_study_plan(id_user):
    """
    Obtener el plan de estudios de un estudiante.
    """
    data = db.users.find_one({"id_user" : id_user}, {"_id" : 0, "career.study_plan" : 1})["career"]["study_plan"]
    return(data)

@users.get("/user/{id_user}/last_updated")
async def read_user_last_updated(id_user : str):
    """
    Obtener la última fecha de actualización de los 
    datos del estudiante.
    """
    data = db.users.find_one({"id_user" : id_user}, {"_id": 0, "last_updated" : 1})["last_updated"]
    return(data)

@users.get("/user/{id_user}/dwell_time")
def get_student_dwell_time(id_user : str):
    """
    Obtener el tiempo de permanencia (en años) del estudiante.
    """
    año_ingreso = int(re.findall(r"^[0-9]{2}", str(id_user))[0])
    # año_ingreso

    año_actual = dataframe("grades/" + id_user + "/periods").loc[0,0]
    año_actual = int(re.findall(r"[0-9]{2}", str(año_actual))[1])
    # año_actual

    permanencia = año_actual - año_ingreso
    return(permanencia)