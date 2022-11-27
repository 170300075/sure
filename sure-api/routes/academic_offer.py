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

academic_offer = APIRouter(
    tags = ["Oferta académica"]
)

@academic_offer.get("/academic_offer/{study_plan}")
def read_academic_offer(study_plan : str):
    """
    Obtener la oferta academica de un plan de estudios
    que se pasa como parámetro. 
    """
    # Asignaturas adicionales
    additional = pd.DataFrame(fetch("academic_offer/" + study_plan + "/additional"))
    # Talleres
    workshops = pd.DataFrame(fetch("academic_offer/" + study_plan + "/workshops"))
    # Lengua extranjera
    foreign_language = pd.DataFrame(fetch("academic_offer/" + study_plan + "/foreign_language"))

    # Combinamos la información de los dataframes anteriores
    academic_offer = pd.concat([additional, workshops, foreign_language], ignore_index = True)
    # Rellenamos datos faltantes
    academic_offer = academic_offer.fillna("-")

    # Eliminar duplicados
    academic_offer.drop_duplicates(inplace = True)
    
    return(dataframe2Dict(academic_offer))

@academic_offer.get("/academic_offer/{study_plan}/period")
def read_period_from_academic_offer(study_plan : str):
    """
    Permite obtener el nombre completo de la oferta academica del periodo actual
    """
    data = db.academic_offer.find_one({"study_plan" : study_plan}, {"_id" : 0, "period_offer_title" : 1})["period_offer_title"]
    return(data)

@academic_offer.get("/academic_offer/{study_plan}/last_updated")
async def read_academic_offer_last_updated(study_plan : str):
    """
    Endpoint para obtener la última fecha de actualización de la oferta académica
    """
    data = db.academic_offer.find_one({"study_plan" : study_plan}, {"_id" : 0, "last_updated" : 1})["last_updated"]
    return(data)

@academic_offer.get("/academic_offer/{study_plan}/{type}")
async def read_academic_offer_type(study_plan : str, type : str):
    """
    Endpoint para obtener la oferta academica de acuerdo a un plan de estudios y el tipo de asignaturas ofertadas.
    Los tipos son:
    \n- `additional`: asignaturas adicionales
    \n- `workshops`: asignaturas de talleres
    \n- `foreign_language`: asignaturas de lengua extranjera
    """
    if type == "additional":
        data = db.academic_offer.find_one({"study_plan" : study_plan}, {"_id" : 0, "aditionals" : 1})
        return data["aditionals"]
        # return "aditionals"
    elif type == "workshops":
        data = db.academic_offer.find_one({"study_plan" : study_plan}, {"_id" : 0, "workshops" : 1})
        return data["workshops"]
    elif type == "foreign_language":
        data = db.academic_offer.find_one({"study_plan" : study_plan}, {"_id" : 0, "foreign_languages" : 1})
        return data["foreign_languages"]
    else:
        raise HTTPException(status_code = 404, detail = "Resource Not Found")

@academic_offer.get("/academic_offer_for_student/{id_user}/{option}")
def read_subjects_list(id_user : str, option : str):
    """
    Endpoint que permite filtrar la oferta académica de acuerdo a una opción de filtro. Las opciones son:
    \n- `exclusive`: devuelve las asignaturas de la oferta academica excluyendo aquellas que el estudiante ha acreditado.
    \n- `inclusive`: devuelve las asignaturas de la oferta academica incluyendo aquellas que el estudiante ha acreditado.
    \n- `mandatory`: devuelve las asignaturas de la oferta academica que son obligatorias porque fueron reprobadas por el estudiante 
    """
    programa = db.users.find_one({"id_user" : id_user}, {"_id" : 0, "career.study_plan" : 1})["career"]["study_plan"]
    print("programa: " + programa)
    if option == "exclusive":
        acreditadas = pd.DataFrame(fetch("control/" + id_user + "/acredited"))
        oferta_academica = pd.DataFrame(fetch("academic_offer/" + programa))
        filtro = set(set(oferta_academica["id_subject"])).difference(acreditadas["id_subject"])
        oferta = oferta_academica[oferta_academica["id_subject"].isin(list(filtro))]
        mapa_curricular = pd.DataFrame(fetch("curricular_map/" + programa))
        oferta_academica = oferta.merge(mapa_curricular.drop("subject", axis = 1), on = ["id_subject"], how = "left")
        
        # Añadir las tasas de reprobación
        ## Por asignaturas
        tasa_reprobacion_asig = pd.read_csv("tasa_reprobacion_asignaturas.csv")

        # oferta_academica = dataframe("academic_offer_for_student/" + id_user + "/exclusive")
        oferta_academica = oferta_academica.merge(tasa_reprobacion_asig, on = ["id_subject"], how = "left")
        oferta_academica = oferta_academica.fillna(0)

        ## Por docente
        tasa_reprobacion_docente = pd.read_csv("tasa_reprobacion_docentes.csv", encoding = "Latin1")
        oferta_academica = oferta_academica.merge(tasa_reprobacion_docente, on = ["teacher"], how = "left").fillna(0)

        ## Por docente y asignatura
        tasa_reprobacion_docente_asignatura = pd.read_csv("tasa_reprobacion_docente_asignatura.csv", encoding = "Latin1")
        oferta_academica = oferta_academica.merge(tasa_reprobacion_docente_asignatura, on = ["id_subject", "teacher"], how = "left").fillna(0)

        # Calcular cuartiles
        cuartiles = []
        for i in oferta_academica["fail_rate"]:
            if i == 0:
                cuartiles.append(1)
            elif(i > 0 and i < 6):
                cuartiles.append(2)
            elif(i > 6 and i < 12):
                cuartiles.append(3)
            elif(i > 12):
                cuartiles.append(4)
        oferta_academica["quartiles"] = cuartiles

        # Calcular quintiles
        quintiles = []
        for i in oferta_academica["fail_rate"]:
            if i == 0:
                quintiles.append(1)
            elif(i > 0 and i < 4):
                quintiles.append(2)
            elif(i > 4 and i < 9):
                quintiles.append(3)
            elif(i > 9 and i < 14):
                quintiles.append(4)
            elif(i > 14):
                quintiles.append(5)
                
        oferta_academica["quintiles"] = quintiles

        # ######################################### Filtrar las asignaturas pendientes
        
        # creditos = dataframe("credits/" + id_user)
        # obligatorias = dataframe("academic_offer_for_student/" + id_user + "/mandatory")
        # datos_estudiante = fetch("user/" + id_user)

        # # Filtramos los ciclos que tienen créditos faltantes
        # faltantes = creditos[creditos["req_credits"] > creditos["credits"]]
        # # Filtramos la oferta de acuerdo a los ciclos con créditos pendientes
        # pendientes = oferta_academica[oferta_academica["school_year"].isin(faltantes["school_year"])].sort_values(by = "school_year", ascending = True)
        # mascara = pendientes[["monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]].isin(["-"]).sum(axis = 1)
        # mascara = pendientes[mascara == 6]
        # eliminadas = set(mascara["id_subject"]).difference(set(pendientes[pendientes["subject"].str.startswith("Prácticas Profesionales")]["id_subject"]))
        # mascara = mascara[mascara["id_subject"].isin(list(eliminadas))]

        # # Eliminar las asignaturas están en la oferta 
        # # pero no se pueden cargar
        # pendientes = pendientes.drop(mascara.index)

        # # Eliminar el aula de los horarios y los indices
        # pendientes = eliminar_salon(pendientes).reset_index(drop = True)
        # obligatorias = eliminar_salon(obligatorias)
        # obligatorias = obligatorias.reset_index(drop = True)

        # # Eliminamos las asignaturas obligatorias de la tabla de asignaturas pendientes (hacemos lo mismo pero más eficiente)
        # pendientes = pendientes[~pendientes["id_subject"].isin(obligatorias["id_subject"].unique())]
        # pendientes = pendientes.reset_index(drop = True)

        # # Eliminamos preespecialidad
        # # pre_inteliencia = creditos[]
        # if(creditos["credits"][5]!=creditos["credits"][6]):
        #     if(creditos["credits"][5]>creditos["credits"][6]):
        #         pendientes = pendientes[pendientes["type"]!= "Innovación en TIC"]
        #         pendientes = pendientes [pendientes["subject"]!= "Prácticas Profesionales preespecialidad: Innovación en TIC"]
        #     else:
        #         pendientes = pendientes[pendientes["type"]!= "Inteligencia Organizacional y de Negocios"]
        #         pendientes = pendientes [pendientes["subject"]!= "Prácticas profesionales preespecialidad: Inteligencia organizacional y de negocios"]
                
        # ################################################ Terminar la segunda version 

        return(dataframe2Dict(oferta_academica))
        # return(dataframe2Dict(pendientes))

    elif option == "inclusive":
        return(fetch("academic_offer/" + programa))
    
    elif option == "mandatory":
        obligatorias = pd.DataFrame(fetch("subjects/" + id_user +  "/not_acredited_yet"))
        oferta_obligatoria = None
        if len(obligatorias) > 0:
            oferta_obligatoria = obligatorias["id_subject"]
            oferta = pd.DataFrame(fetch("academic_offer_for_student/" + id_user + "/exclusive"))
            oferta_obligatoria = oferta[oferta["id_subject"].isin(oferta_obligatoria)]

            if len(oferta_obligatoria) > 0:
                return(dataframe2Dict(oferta_obligatoria))
            else:
                return([{"message": "No se encontraron obligatorias ofertadas"}])
        else:
            return([{"message" : "El estudiante no tiene asignaturas obligatorias"}])
    else:
        return([{"message": "Opción no existe"}])