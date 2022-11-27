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
from models.grades import SubjectGrade

grades = APIRouter(
    tags = ["Calificaciones"]
)

@grades.get("/grades/{id_user}", response_model = list[SubjectGrade])
async def read_grades(id_user : str):
    """
    Obtener las boletas de calificaciones del estudiante 
    a partir de su matrícula.
    """
    # Datos del historial academico en la base de datos
    historial_academico = db.grades.find_one({"id_user" : id_user}, {"_id" : 0})
    # Lista con las calificaciones procesadas
    lista_calificaciones = []
    # Iteramos sobre cada elemento de la lista de calificaciones
    for item in historial_academico["grades"]:
        # En cada lista de diccionario de calificaciones del periodo
        for d in item["subject_grades"]:
            # Añadimos a cada diccionario el periodo como nueva variable
            d["period"] = item["period"]
            d["id_user"] = historial_academico["id_user"]
        
        lista_calificaciones.extend(item["subject_grades"])

    # Convertimos la lista de diccionarios de las calificaciones en un dataframe
    # para generar el historial academico del estudiante
    historial_academico = pd.DataFrame(lista_calificaciones)
    # Imputar valores faltantes con -
    historial_academico = historial_academico.fillna("-")
    return(dataframe2Dict(historial_academico))

@grades.get("/grades/{id_user}/last_updated")
async def read_grades_last_update(id_user : str):
    """
    Obtener la fecha de actualización de las boletas de 
    calificaciones un estudiante a partir de su matrícula.
    """
    last_updated = db.grades.find_one({"id_user" : id_user}, {"_id" : 0, "last_updated" : 1})["last_updated"]
    return(last_updated)

@grades.get("/grades/{id_user}/periods")
async def get_grades_periods(id_user: str):
    """
    Obtener una lista de los periodos de los que se 
    disponen calificaciones para un estudiante a partir de su matrícula.
    """
    # Obtenemos las calificaciones con los periodos
    calificaciones_periodos = db.grades.find_one({"id_user" : id_user}, {"_id" : 0, "grades.period" : 1})
    # Creamos una lista que contendrá los periodos
    periodos = []
    # Para cada diccionario en las calificaciones
    for d in calificaciones_periodos["grades"]:
        # Guardamos todos esos valores en una lista
        periodos.append(d["period"])
    return(periodos)

@grades.get("/grades/{id_user}/averages")
async def get_grades_averages(id_user : str):
    """
    Obtener los promedios finales para cada periodo disponible.
    """
    data = db.grades.find_one({"id_user" : id_user}, {"_id" : 0, "grades.period": 1, "grades.average_grades" : 1})["grades"]
    return(data)

@grades.get("/grades/{id_user}/{period}")
async def get_grades_period(id_user : str, period : str):
    """
    Obtener las boleta de calificaciones de un periodo. Toma como parámetro la 
    matrícula y el periodo del que se quiere consultar.
    """
    for d in db.grades.find_one({"id_user" : id_user}, {"_id" : 0})["grades"]:
        if d["period"] == period:
            return(d["subject_grades"])