######################################
#           Bibliotecas              #
######################################
from fastapi import APIRouter, HTTPException
import pandas as pd

######################################
#           Dependencias             #
######################################
from config.database import db
from config.utilities import dataframe2Dict, dataframe, fetch, fetch_post, post
from config.generator_utilities import colision, colision_carga, eliminar_salon, serializar, recomendacion, oferta_pendientes

generators = APIRouter(
    tags = ["Recomendador automático"]
)

@generators.get("/generator/{id_user}")
def generate_recommendations(id_user : str):
    """
    Permite generar recomendaciones de asignaturas que no colisionen 
    en horario, que respecten las serializaciones, cierre de ciclos, recomendar las
    obligatorias reprobadas.
    """
    datos_estudiante = fetch("user/" + id_user)
    
    oferta = dataframe("academic_offer_for_student/" + id_user + "/exclusive")
    creditos = dataframe("credits/" + id_user)
    obligatorias = dataframe("academic_offer_for_student/" + id_user + "/mandatory")s
    
    pendientes = oferta_pendientes(oferta, creditos, obligatorias)

    acreditadas = dataframe("control/" + id_user + "/acredited")
    seriadas = pd.read_csv("config/seriadas.csv")
    
    print("situacion:", datos_estudiante["career"]["situation"])
    print("trabaja: ", datos_estudiante["job"]["working"])

    if datos_estudiante["career"]["situation"] == "Condicionado":
        condicionado = True
    else: 
        condicionado = False

    if datos_estudiante["job"]["working"] == "No trabajo":
        trabaja = False
    else:
        trabaja = True

    n_obligatorias = len(obligatorias["id_subject"].unique())

    # Si está condicionado o tiene más de 3 reprobadas para cargar
    # este semestre
    if condicionado == True or n_obligatorias >= 3:
        tam = 3
        
    # Si no esta condicionado
    else: 
        # Si el estudiante trabaja
        if(trabaja == True):
            tam = 5
        # Si el estudiante no trabaja
        else:
            tam = 8

    print("tam: ", tam)

    # Eliminar de las pendientes las asignaturas que no hayan acreditados las previas
    pendientes = serializar(pendientes, seriadas, acreditadas)

    
    # Generar las recomendaciones
    pendientes = obligatorias.append(pendientes)
    recomendaciones = recomendacion(pendientes, tam)
    
    pendientes["key"] = pendientes["id_subject"].astype(str).str.cat(pendientes["section"].astype(str),sep=" ")
    dfs = [ dataframe2Dict(pendientes[pendientes["key"].isin(i)]) for i in recomendaciones]
    return(dfs)

@generators.get("/generator/validation/{id_user}")
def generate_and_validate_recomendations(id_user : str):
    lista_recomendaciones = fetch("generator/" + id_user)
    # preliminar = {"id_user" : id_user, "recommendations" : lista_recomendaciones}
    validadas = {"id_user" : id_user}
    lista = []
    # for item in preliminar["recommendations"]:
    for item in lista_recomendaciones:
        df = pd.DataFrame(item)
        lista.append({ "valid" : post("model?id_user=" + id_user, dataframe2Dict(df[["section", "id_subject"]]) ), "draft" : dataframe2Dict(df)})

    validadas["recommendations"] = lista
    db.recommendations.replace_one({"id_user" : id_user}, validadas, upsert = True)

    return("Finalizado")
    
@generators.get("/generator/read/{id_user}/availability")
def read_auto_recommendations(id_user : str):
    recomendaciones = db.recommendations.find_one({"id_user" : id_user}, {"_id" : 0, "recommendations" : 1})["recommendations"]
    return(len(recomendaciones))


@generators.get("/generator/read/{id_user}/{index}")
def read_recommendation(id_user : str, index : int):
    recomendaciones = db.recommendations.find_one({"id_user" : id_user}, {"_id" : 0, "recommendations" : 1})["recommendations"]
    return(recomendaciones[index])