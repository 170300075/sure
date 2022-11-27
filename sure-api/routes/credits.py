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

credits = APIRouter(
    tags = ["Créditos"]
)

@credits.get("/credits/{id_user}")
def read_user_credits(id_user : str):
    """
    Endpoint para obtener los créditos obtenidos por ciclo y preespecialidades 
    de un estudiante.
    """
    # Obtener las asignaturas acreditadas por el estudiante
    print("Obtener acreditadas")
    acreditadas = pd.DataFrame(fetch("control/" + id_user + "/acredited"))

    print("Calcular creditos por periodo")
    # Obtener la tabla de validación por ciclos     
    creditos_por_periodo = acreditadas[["school_year", "school_period", "subject_type", "credits"]].groupby(["school_year", "school_period", "subject_type"]).sum("credits").reset_index()

    print("Filtrar asignaturas creditos de primarias")
    # Filtrar las asignaturas Básicas y elección libre para contabilizar créditos por ciclo
    primarias = creditos_por_periodo[creditos_por_periodo["subject_type"].isin(["Básica", "Elección libre"])]
    # Calculamos créditos en asignaturas primarias
    creditos_primarias = primarias.groupby("school_year").sum("credits").reset_index()

    print("Filtrar creditos de secundarias")
    # Filtrar las asignaturas de Preespecialidad para contabilizar créditos por ciclo
    preespecialidad = creditos_por_periodo[creditos_por_periodo["subject_type"].str.startswith("Pre-especialidad")]
    # Obtenemos los nombres de las preespecialidades de la carrera
    nombres_preespecialidades = [j for i, j in preespecialidad["subject_type"].str.split("Pre-especialidad ")]
    # Asignamos los nombres de preespecialidades como valores de school_year
    preespecialidad["school_year"] = nombres_preespecialidades
    # Calculamos créditos en asignaturas de preespecialidad
    creditos_preespecialidades = preespecialidad.groupby(["school_year"]).sum("credits").reset_index()
    print("Juntar ambas tablas de creditos")
    creditos = pd.concat([creditos_primarias, creditos_preespecialidades])

    print("Obtener programa de estudiante")
    programa = db.users.find_one({"id_user" : id_user}, {"_id" : 0, "career.study_plan" : 1})["career"]["study_plan"]
    print("Obtener tabla de validacion")
    validacion = pd.DataFrame(fetch("validation/" + programa))

    print("Calcular creditos por ciclo escolar en primarias")
    validacion_primarias = validacion[["school_year", "max_credits", "req_credits"]][validacion["subject_type"].isin(["Básica", "Elección libre"])]
    validacion_primarias = validacion_primarias.groupby(["school_year"]).sum().reset_index()
    
    print("Calcular creditos por ciclo escolar en preespecialidad")
    validacion_preespecialidades = validacion[validacion["subject_type"].str.startswith("Pre-especialidad")]
    del validacion_preespecialidades["school_year"] 
    del validacion_preespecialidades["school_period"]
    validacion_preespecialidades = validacion_preespecialidades.rename({"subject_type" : "school_year"}, axis = "columns")
    nombres_preespecialidades = [j for i, j in validacion_preespecialidades["school_year"].str.split("Pre-especialidad ")]
    validacion_preespecialidades["school_year"] = nombres_preespecialidades

    print("Juntar info en una tabla")
    validacion_carrera = pd.concat([validacion_primarias, validacion_preespecialidades])
    print("creditos requeridos vs obtenidos por estudiante por ciclos")
    validacion_carrera = validacion_carrera.merge(creditos, on = ["school_year"], how = "left")
    print("Rellenar creditos de ciclos no iniciados con 0 creditos")
    validacion_carrera = validacion_carrera.fillna(0)
    return(dataframe2Dict(validacion_carrera))