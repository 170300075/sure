from itertools import combinations, compress
import pandas as pd
import numpy as np
import json
import requests
from itertools import combinations, compress

# Funciones para generar las recomendaciones
def colision(materia1, materia2):
    """
    Detectar colisiones en un par de asignaturas
    que se pasan como parámetro y devuelve la 
    la suma de las colisiones encontradas.
    
    materia1 y materia2 son filas del dataframe
    de la oferta académica.
    """
    columnas = ['monday', 'tuesday', 'wednesday','thursday','friday','saturday']
    
    materia1 = materia1[columnas].replace({':00':''}, regex=True)
    materia2 = materia2[columnas].replace({':00':''}, regex=True)
    
    s = []

    for i in range(len(materia1)):
        if(materia1[i] != "-" and materia2[i] != "-"):
            
            materia1[i] = materia1[i].split("-", 1)
            temp = set(range(int(materia1[i][0]),int(materia1[i][1])))
            
            materia2[i] = materia2[i].split("-", 1)
            temp2 = set(range(int(materia2[i][0]),int(materia2[i][1])))
            
            if len(temp.intersection(temp2)) != 0:
                s.append(1)
                # Se decarta asignatura
            else:
                s.append(0)
                #a = a.union(b)
        else:
            s.append(0)
            
    
    return(sum(s))


def colision_carga(carga):
    """
    Devuelve una lista con la cantidad de colisiones
    por carga académica que se pasa como parámetro.
    carga es un dataframe.
    """
    h = []
    for i in range(len(carga)):
        a = carga.iloc[i]
        for j in range(i+1,len(carga)):
            b = carga.iloc[j]
            h.append(colision(a, b))
    
    return(sum(h))


def eliminar_salon(oferta):
    """
    Procesa de las materias introducidas 
    los salones en el horario asignado
    """
    columnas = ['monday', 'tuesday', 'wednesday','thursday','friday','saturday']
    oferta[columnas] = oferta[columnas].replace(regex=True, to_replace=r'A-'+'[0-9]'+'[0-9]', value=r'')
    oferta[columnas] = oferta[columnas].replace(regex=True, to_replace=r'B-'+'[0-9]'+'[0-9]', value=r'')
    oferta[columnas] = oferta[columnas].replace(regex=True, to_replace=r'C-'+'[0-9]'+'[0-9]', value=r'')
    oferta[columnas] = oferta[columnas].replace(regex=True, to_replace=r'D-'+'[0-9]'+'[0-9]', value=r'')
    oferta[columnas] = oferta[columnas].replace(regex=True, to_replace=r'E-'+'[0-9]'+'[0-9]', value=r'')
    oferta[columnas] = oferta[columnas].replace(regex=True, to_replace=r'F-'+'[0-9]'+'[0-9]', value=r'')
    oferta[columnas] = oferta[columnas].replace(regex=True, to_replace=r'G-'+'[0-9]'+'[0-9]', value=r'')
    oferta[columnas] = oferta[columnas].replace(regex=True, to_replace=r'[^0-9-:]', value=r'')
    
    return oferta

def serializar(pendientes, seriadas, acreditadas):
    
    # Obtenemos solo las columnas [id_subject] , [previous]
    s = seriadas
    # Left_join ubicamos las materias serializadas
    a = pendientes.merge(s, on='id_subject', how='left')
    # Obtenemos solo las columnas [id_subject] , [final_grade]
    p = acreditadas.drop(acreditadas.columns[[0,1,2,4,5,6,7,8,9,10,12,13,14,15,16,17,18]], axis='columns')
    # Renombramos la columna id_subjec para hacer el enlace
    # Hacemos left join con las columnas previous de ambos data frames
    p = p.rename(columns={'id_subject':'previous1'})
    a = a.merge(p, on='previous1', how='left')
    p = p.rename(columns={'previous1':'previous2','final_grade':'final_grade2' })
    a = a.merge(p, on='previous2', how='left')
    # Eliminamos las filas que no tengan final_grade (asignaturas no acreditadas)
    a = a.drop(a[(a['previous1'].isna() == False) & (a['final_grade'].isna() == True)].index)
    a = a.drop(a[(a['previous2'].isna() == False) & (a['final_grade2'].isna() == True)].index)
    #a['final_grade'] = a['final_grade'].astype("float64").astype('Int32')
    #a = a.drop(a[(a['previous'].isna() == False) & (a['final_grade'] <= 6)].index)
    
    # Eliminamos las filas que creamos con los joins
    a = a.drop(a.columns[[22,23,24,25]], axis='columns')
    # Retornamos la oferta academica sin las materias seriadas
    return a

def recomendacion(pendientes, tam):
    b = pendientes["id_subject"].unique()[0:tam]
    a = pendientes[pendientes.id_subject.isin(b)]
    a["key"] = a["id_subject"].astype(str).str.cat(a["section"].astype(str),sep=" ")
    b = set(a["key"])
    for j in range(tam):
        conjuntos = list(combinations(b , tam-j))
        c = []
        for i in conjuntos:
            if(colision_carga(a[a["key"].isin(i)]) >= 1):
                del i
            else:
                if(len(set(a[a["key"].isin(i)].id_subject)) == len(a[a["key"].isin(i)].id_subject)):
                    c.append(i)
        if(len(c) > 0):
            return c
            break

def oferta_pendientes(oferta, creditos, obligatorias):   
    faltantes = creditos[creditos["req_credits"] > creditos["credits"]]

    # Filtramos la oferta de acuerdo a los ciclos con créditos pendientes
    pendientes = oferta[oferta["school_year"].isin(faltantes["school_year"])]
    mascara = pendientes[["monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]].isin(["-"]).sum(axis = 1)
    mascara = pendientes[mascara == 6]
    eliminadas = set(mascara["id_subject"]).difference(set(pendientes[pendientes["subject"].str.startswith("Prácticas Profesionales")]["id_subject"]))
    mascara = mascara[mascara["id_subject"].isin(list(eliminadas))]

    # Eliminar las asignaturas están en la oferta 
    # pero no se pueden cargar
    pendientes = pendientes.drop(mascara.index)

    # Eliminar el aula de los horarios y los indices
    pendientes = eliminar_salon(pendientes).reset_index(drop = True)
    obligatorias = eliminar_salon(obligatorias)
    obligatorias = obligatorias.reset_index(drop = True)

    # Eliminamos las asignaturas obligatorias de la tabla de asignaturas pendientes (hacemos lo mismo pero más eficiente)
    pendientes = pendientes[~pendientes["id_subject"].isin(obligatorias["id_subject"].unique())]
    pendientes = pendientes.reset_index(drop = True)

    # Eliminamos preespecialidad
    # pre_inteliencia = creditos[]
    if(creditos["credits"][5]!=creditos["credits"][6]):
        if(creditos["credits"][5]>creditos["credits"][6]):
            pendientes = pendientes[pendientes["type"]!= "Innovación en TIC"]
            pendientes = pendientes[pendientes["subject"]!= "Prácticas Profesionales preespecialidad: Innovación en TIC"]
        else:
            pendientes = pendientes[pendientes["type"]!= "Inteligencia Organizacional y de Negocios"]
            pendientes = pendientes[pendientes["subject"]!= "Prácticas profesionales preespecialidad: Inteligencia organizacional y de negocios"]
    
    return(pendientes)