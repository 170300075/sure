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

control = APIRouter(
    tags = ["Historial académico"]
)

@control.get("/control/{id_user}")
def get_student_records(id_user : str):
    """
    Endpoint para obtener la información del historial academico.
    Esta contiene los registros de las asignaturas que han
    sido cursadas por el estudiante e información
    propia de la asignatura como créditos, área, ciclo y periodo. 
    """
    
    # Consultamos el documento en la base de datos donde la matricula coincida
    historial_academico = pd.DataFrame(fetch("grades/" + id_user))
    programa = db.users.find_one({"id_user" : id_user}, {"_id" : 0, "career.study_plan" : 1})["career"]["study_plan"]
    curricular_map = pd.DataFrame(fetch("curricular_map/" + programa))

    # Unimos los datos del historial y el mapa curricular tomando como match la columna id_subject
    control = historial_academico.merge(curricular_map.drop("subject", axis = 1), on = ["id_subject"], how = "left")
    ######### AVISO:
    # Quitar este fillna cuando se hayan agregado las asignaturas co-curriculares
    control = control.fillna("-")

    control = dataframe2Dict(control)
    return(control)

@control.get("/control/{id_user}/{status}")
def get_filtered_student_records(id_user : str, status : str):
    """
    Endpoint para obtener la información del historial académico
    filtrada bajo ciertos criterios:

    \n- acredited: asignaturas acreditadas.
    \n- not_acredited: asignaturas no acreditadas, incluyen las
    asignaturas cursandose y reprobadas.
    \n- failed: asignaturas reprobadas.
    \n- studying: asignaturas que se están cursando en este periodo.
    \n- repeated: asignaturas recursadas, incluyen tanto reprobatorias
    aprobatorias (si de esta ultima existe registro).
    \n- repeated_acredited: asignaturas recursadas que se aprobaron en segunda
    o tercera oportunidad.
    """
    # Consultar la API con el endpoint para la tabla control y convertir a dataframe
    control = pd.DataFrame(fetch("control/" + id_user))
    
    # Obtenemos el filtro para los registros de asignaturas aprobatorias
    aprobatorias = control["final_grade"].isin(["Aprobado", 7.0, 8.0, 9.0, 10.0])
    # Las asignaturas no aprobatorias son el complemento de las anteriores
    no_aprobatorias = ~aprobatorias
    
    if status == "acredited":
        # Filtramos las asignaturas aprobadas tomando en consideracion
        # las posibles calificaciones aprobatorias que son >= 7 y "Aprobado"
        aprobadas = control[aprobatorias].sort_values(by = ["school_year", "school_period", "subject_type", "id_subject"])

        # Retornamos los datos ordenados por ciclo, semestres, tipo de asignatura y clave de asignatura
        return(dataframe2Dict(aprobadas))
    
    elif status == "not_acredited": 
        # Filtramos los registros para las asignaturas no aprobadas
        no_aprobadas = control[no_aprobatorias]
        # Retornar los registros no acreditados
        return(dataframe2Dict(no_aprobadas))

    elif status == "failed":
        no_aprobadas = pd.DataFrame(fetch("control/" + id_user + "/not_acredited"))
        # Filtramos las asignaturas reprobadas
        reprobadas = no_aprobadas[no_aprobadas["final_grade"] != "-"]
        # Retornamos los datos
        return(dataframe2Dict(reprobadas))

    elif status == "studying":
        no_aprobadas = pd.DataFrame(fetch("control/" + id_user + "/not_acredited"))
        # Filtramos las asignaturas que se están cursando
        cursando = no_aprobadas[no_aprobadas["final_grade"] == "-"]
        # Retornamos los datos
        return(dataframe2Dict(cursando))

    elif status == "repeated":
        # Obtenemos las asignaturas que se han cursado más de una vez
        recursadas = control[control.duplicated(subset = ["id_subject"], keep = False)].sort_values(by = ["id_subject", "final_grade"], ascending = False)
        # Retornamos los datos
        return(dataframe2Dict(recursadas))

    elif status == "repeated_acredited":
        recursadas = pd.DataFrame(fetch("control/" + id_user + "/repeated"))
        # Flitrar asignaturas que fueron recursadas y acreditadas
        recursadas_aprobadas = recursadas[recursadas["final_grade"].isin(["Aprobado", 7.0, 8.0, 9.0, 10.0])]
        # Retornamos los datos
        return(dataframe2Dict(recursadas_aprobadas))

    else:
        return(id_user)
