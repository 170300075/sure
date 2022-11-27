######################################
#           Bibliotecas              #
######################################
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import pandas as pd
import keras

# sudo apt install nvidia-cuda-toolkit


######################################
#           Dependencias             #
######################################
from config.database import db
from config.utilities import dataframe2Dict, dataframe, fetch

######################################
#           Modelos                  #
######################################
from models.recommenders import SelectedSubject, Predictors

recommenders = APIRouter(
    tags = ["Modelos de Machine/Deep Learning"]
)

@recommenders.post("/model", response_model = int)
def run_model(id_user : str, selecciones : list[SelectedSubject]):
    """
    Permite obtener si la carga será aprobadas
    """
    # Diccionario con las variables
    x = {}

    # Convertir diccionario a dataframe
    # selecciones = pd.DataFrame(selecciones)
    selecciones = pd.DataFrame([item.dict() for item in selecciones])
    # selecciones = dict((item[0], item[1]) for item in list(selecciones))
    print("selecciones: ", selecciones, end = "\n\n")
    # Obtener la oferta academica para el estudiante
    oferta_academica = dataframe("academic_offer_for_student/" + id_user + "/exclusive")
    
    ##### Recursada #####
    draft = selecciones.merge(oferta_academica, on = ["section", "id_subject"], how = "left")
    # Obtener las asignaturas obligatorias para el estudiante (Id_user)
    obligatorias = dataframe("academic_offer_for_student/" + id_user + "/mandatory")
    
    if obligatorias.columns.isin(["message"])[0] == False:
        x['recursada'] = 1 if True in draft["id_subject"].isin(obligatorias["id_subject"]) else 0
    else:
        x['recursada'] = 0

    ##### tasa_rep_carga ######
    x['tasa_rep_carga'] = draft["fail_rate"].mean()
    ##### ceneval_analitico #####
    x['ceneval_analitico'] = 1056.308896817509
    ##### ceneval_matematico #####
    x['ceneval_matematico'] = 1038.1467191957615
    ##### prom_per_prev ######
    x['prom_per_prev'] = fetch("indicators/" + id_user + "/period_averages")["prom_per_prev"]
    ##### asigMuchas #####
    x['asigMuchas'] = 1 if len(draft) > 6 else 0
    ##### complejidad_carga5 #####
    x['complejidad_carga5'] = draft["quintiles"].mean()
    ###### situacion_irregular #####
    x['situacion_irregular'] = 1 if fetch("user/" + id_user)["career"]["situation"] == "Irregular" else 0


    ## Version #1
    # Estandarización con las mismas constantes de entrenamiento
    x["recursada"] = (x["recursada"]-(0.134362934362934))/0.341173592111536
    x["tasa_rep_carga"] = (x["tasa_rep_carga"]-(20.128042593678))/7.33275018814469
    x["ceneval_analitico"] = (x["ceneval_analitico"]-(1104.96355208494))/96.7418660864241
    x["ceneval_matematico"] = (x["ceneval_matematico"]-(1099.94277839768))/107.330791356187
    x["prom_per_prev"] = (x["prom_per_prev"]-(7.85148801863088))/1.35222266632301
    x["asigMuchas"] = (x["asigMuchas"]-(0.476447876447876))/0.499637937095662
    x["complejidad_carga5"] = (x["complejidad_carga5"]-(3.20772200772201))/1.6700662139977
    x["situacion_irregular"] = (x["situacion_irregular"]-(0.343629343629344))/0.475102642521778

    x = pd.DataFrame([x])
    filename = "./predictors/Neural_Networks_v1.h5"
    modelo = keras.models.load_model(filename)

    ## Version #2
    # Normalización de las variables
    # x["recursada"] = (x["recursada"]-(0))/(1-(0))
    # x["tasa_rep_carga"] = (x["tasa_rep_carga"]-(0))/(41.83-(0))
    # x["ceneval_analitico"] = (x["ceneval_analitico"]-(820))/(1300-(820))
    # x["ceneval_matematico"] = (x["ceneval_matematico"]-(796))/(1300-(796))
    # x["prom_per_prev"] = (x["prom_per_prev"]-(0))/(10-(0))
    # x["asigMuchas"] = (x["asigMuchas"]-(0))/(1-(0))
    # x["complejidad_carga5"] = (x["complejidad_carga5"]-(1))/(5-(1))
    # x["situacion_irregular"] = (x["situacion_irregular"]-(0))/(1-(0))

    # x = pd.DataFrame([x])
    # filename = "./predictors/Neural_Networks_v2.h5"
    # modelo = keras.models.load_model(filename)

    y_pred = (modelo.predict(x) > 0.5).astype("int32")
    y_pred = y_pred[0][0]
    
    return(y_pred)