######################################
#           Bibliotecas              #
######################################
from fastapi import FastAPI

######################################
#           Importamos los routers   #                
######################################
from routes.tokens import tokens
from routes.credentials import credentials
from routes.curricular_maps import curricular_maps
from routes.credits import credits
from routes.users import users
from routes.indicators import indicators
from routes.payments import payments
from routes.grades import grades
from routes.schedules import schedules
from routes.control import control
from routes.subjects import subjects
from routes.academic_offer import academic_offer
from routes.practices_offer import practices_offer
from routes.services_offer import services_offer
from routes.recommenders import recommenders
from routes.webscrapers import webscrapers
from routes.generator import generators

# Descripción de la API
description = """
SURE API ayuda a obtener información para la SURE APP. 
Todos los cálculos se han realizado desde los diferentes endpoints
por lo que en muchos casos, solo será necesario consultar esta información
directamente desde algún endpoint.

SURE API está desarrollado para hacer cosas maravillosas 🚀.
Hecho con ❤ por Kenneth a.k.a BlackMaster (170300075).
"""

# Definimos una instancia de fastapi
app = FastAPI(
    title = "SURE API",
    version = "1.0.0",
    description = description,
    contact = {
        "name" : "Kenneth Díaz González",
        "email" : "kennethdiazgonzalez@hotmail.com"
    }
)

# Añadimos los routers a la app
app.include_router(webscrapers)
app.include_router(generators)
app.include_router(tokens)
app.include_router(credentials)
app.include_router(recommenders)
app.include_router(curricular_maps)
app.include_router(credits)
app.include_router(users)
app.include_router(indicators)
app.include_router(payments)
app.include_router(grades)
app.include_router(schedules)
app.include_router(control)
app.include_router(subjects)
app.include_router(academic_offer)
app.include_router(practices_offer)
app.include_router(services_offer)