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

subjects = APIRouter(
    tags = ["Agregaciones con asignaturas"]
)

@subjects.get("/subjects/{id_user}/{option}")
def get_subject_options(id_user : str, option : str):
    """
    Endpoint para obtener información sobre asignaturas
    que han sido reprobadas por el estudiante: 

    \n- not_acredited_yet: obtener información de la(s) asignatura(s) reprobada(s) que el
    estudiante aun no ha acreditado y que por lo tanto, son obligatorias.
    \n- repetitions: obtener información de la cantidad de recursamientos 
    por asignatura reprobada.
    \n- subject_records_per_school_year: permite obtener un conteo de los registros de asignaturas 
    disponibles para cada ciclo escolar y preespecialidades de un estudiante.
    """
    if option == "not_acredited_yet":
        # Obtenemos las asignaturas reprobadas
        reprobadas = pd.DataFrame(fetch("control/" + id_user + "/failed"))
        # Obtenemos las asignaturas recursadas aprobadas del estudiante
        recursadas_aprobadas = pd.DataFrame(fetch("control/" + id_user + "/repeated_acredited"))
        # Obtenemos el programa al que pertenece la carrera del estudiante
        program = db.users.find_one({"id_user" : id_user}, {"_id" : 0, "career.study_plan" : 1})["career"]["study_plan"]
        # Obtenemos el mapa curricular para el programa al que pertenece el estudiante
        curricular_map = pd.DataFrame(fetch("curricular_map/" + program))
        # Obtenemos el conjunto de asignaturas reprobadas que no se han acreditado
        asignaturas_reprobadas = set(reprobadas["id_subject"]).difference(set(recursadas_aprobadas["id_subject"]))
        # Filtramos los datos de esas asignaturas en el mapa curricular
        asignaturas_reprobadas = curricular_map[curricular_map["id_subject"].isin(list(asignaturas_reprobadas))]
        # Retornamos el resultado
        return(dataframe2Dict(asignaturas_reprobadas))

    elif option == "repetitions":
        # Obtenemos las asignaturas recursadas por el estudiante
        recursadas = pd.DataFrame(fetch("control/" + id_user + "/repeated"))
        # Obtenemos el número de recursamientos de las asignaturas que ha reprobado el estudiante
        n_recursamientos = recursadas.groupby("id_subject").size().reset_index(name = "repetitions")
        # Obtenemos el programa al que pertenece la carrera del estudiante
        program = db.users.find_one({"id_user" : id_user}, {"_id" : 0, "career.study_plan" : 1})["career"]["study_plan"]
        # Obtenemos el mapa curricular para el programa al que pertenece el estudiante
        curricular_map = pd.DataFrame(fetch("curricular_map/" + program))
        # Obtenemos la información de la asignatura y unimos los datos de la cantidad de recursamientos
        n_recursamientos = curricular_map.merge(n_recursamientos, on = ["id_subject"], how = "right")
        # Retornamos los datos
        return(dataframe2Dict(n_recursamientos))

    elif option == "subject_records_per_school_year":
        # Obtenemos el historial academico de control
        control = pd.DataFrame(fetch("control/" + id_user))

        n_asignaturas_primarias = control[control["subject_type"].isin(["Básica", "Elección libre"])].groupby(["school_year"]).size().reset_index(name = "n_subjects")

        asignaturas_preespecialidad = control[control["subject_type"].str.startswith("Pre-especialidad")]
        # asignaturas_preespecialidad
        del asignaturas_preespecialidad["school_year"]
        # asignaturas_preespecialidad
        nombres_asignaturas_preespecialidad = [j for i, j in asignaturas_preespecialidad["subject_type"].str.split("Pre-especialidad")]
        nombres_asignaturas_preespecialidad
        asignaturas_preespecialidad = asignaturas_preespecialidad.rename({"subject_type" : "school_year"}, axis = "columns")
        asignaturas_preespecialidad["school_year"] = nombres_asignaturas_preespecialidad
        n_asignaturas_preespecialidad = asignaturas_preespecialidad.groupby(["school_year"]).size().reset_index(name = "n_subjects")
        
        n_asignaturas = pd.concat([n_asignaturas_primarias, n_asignaturas_preespecialidad])
        return(dataframe2Dict(n_asignaturas))
    else:
        return(id_user)