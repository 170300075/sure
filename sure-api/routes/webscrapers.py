######################################
#           Bibliotecas              #
######################################
from fastapi import APIRouter, HTTPException
import pandas as pd
import datetime
# X Display
from pyvirtualdisplay import Display
display = Display(visible = 0, size = (1024, 768))
display.start()


######################################
#           Dependencias             #
######################################
from config.database import db
from config.utilities import dataframe2Dict, dataframe, fetch, fetch_post

from config.webscrapers import initializeWebDriver
from config.webscrapers import loginSIGMAA, logoutSIGMAA 
from config.webscrapers import getPersonalInfo, getAcademicOffer, getGrades, getPayments

# Inicializar el webdriver
# global driver

webscrapers = APIRouter(
    tags = ["Webscrapers"]
)

@webscrapers.post("/webscraper/login_sigmaa")
def login_sigmaa(id_user : str, password : str):
    
    # Iniciar sesión en SIGMAA con credenciales estudiante
    status = loginSIGMAA(driver, id_user, password)
    if status == True:
        return({"message" : "login into sigmaa"})
    else:
        return({"message" : "login error"})

@webscrapers.get("/webscraper/logout_sigmaa")
def logout_sigmaa():
    # Cerrar sesión en el sigmaa
    logoutSIGMAA(driver)
    return({"message" : "logout from sigmaa"})


@webscrapers.post("/webscraper/user")
def update_user_information(id_user : str, password : str):
    # Obtenemos la información personal del estudiante
    student_information = getPersonalInfo(driver, id_user, password)
    student_information["last_updated"] = datetime.datetime.utcnow()

    # Guardamos los datos del estudiante en la base de datos
    db.users.replace_one({"id_user" : id_user}, student_information, upsert = True)

    return({"message" : "Usuario registrado"})

@webscrapers.get("/webscraper/academic_offer/{id_user}")
def update_academic_offer(id_user : str):
    # Obtenemos la oferta académica del estudiante
    academic_offer = getAcademicOffer(driver, fetch("user/" + id_user + "/study_plan"))
    # Guardamos la ultima fecha de actualizacion en el diccionario de datos
    academic_offer["last_updated"] = datetime.datetime.utcnow()

    # Guardamos la oferta académica del estudiante
    db.academic_offer.replace_one({"study_plan" : fetch("user/" + id_user + "/study_plan")}, academic_offer, upsert = True)

    return({"message" : "Oferta actualizada"})


@webscrapers.get("/webscraper/grades/{id_user}")
def update_grades(id_user : str):
    # Obtenemos todas las calificaciones disponibles para el
    # estudiante
    student_grades = getGrades(driver, id_user)
    # Guardamos la fecha de actualizacion en diccionario de datos
    student_grades["last_updated"] = datetime.datetime.utcnow()

    # Guardamos en bases de datos las calificaciones del estudiante 
    db.grades.replace_one({"id_user" : id_user}, student_grades, upsert = True)

    return({"message":"Calificaciones actualizadas"})

@webscrapers.get("/webscraper/payments/{id_user}")
def update_payments(id_user : str):
    # Obtenemos los registros de pagos del estudiante
    payments = getPayments(driver, id_user)
    # Guardamos la fecha de actualizacion en diccionario de datos 
    payments["last_updated"] = datetime.datetime.utcnow()

    # Guardamos en bases de datos los registros de pagos del estudiante
    db.payments.replace_one({"id_user" : id_user}, payments, upsert = True)

    return({"message" : "Registros de pagos actualizados"})


@webscrapers.post("/webscraper/register")
def register_user(id_user : str, password : str):
    # Definimos la variable driver como global
    global driver
    # Creamos una instancia del webdriver para cada sesion
    driver = initializeWebDriver()
    
    status = fetch_post(f"webscraper/login_sigmaa?id_user={id_user}&password={password}")
    print("Estatus de login sigmaa: ", status)

    if status["message"] == "login into sigmaa":        
        fetch_post(f"webscraper/user?id_user={id_user}&password={password}")
        fetch(f"webscraper/academic_offer/{id_user}")
        fetch(f"webscraper/grades/{id_user}")
        fetch(f"webscraper/payments/{id_user}")
        fetch("webscraper/logout_sigmaa")
        # Cerramos la sesion del driver para eliminar caché
        driver.quit()
        return(True)
    
    else:
        # Cerramos la sesion del driver para eliminar caché
        driver.quit()
        return(False)