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

schedules = APIRouter(
    tags = ["Horarios escolares"]
)

@schedules.get("/student_schedule/{id_user}")
def get_student_schedule(id_user : str):
    """
    Permite obtener el horario escolar del estudiante para el periodo
    más reciente.
    """
    programa = db.users.find_one({"id_user" : id_user}, {"_id" : 0, "career.study_plan" : 1})["career"]["study_plan"]
    oferta_academica = pd.DataFrame(fetch("academic_offer/" + programa))
    period = fetch("grades/" + id_user + "/periods")[0]
    asignaturas_actuales = pd.DataFrame(fetch("grades/" + id_user + "/" + period))
    horario_escolar = asignaturas_actuales.merge(oferta_academica.drop(["type", "teacher", "modality", "subject"], axis = 1), on = ["id_subject", "section"], how = "left")
    horario_escolar = horario_escolar[["id_subject", "subject", "teacher", "modality", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]]
    return(dataframe2Dict(horario_escolar))