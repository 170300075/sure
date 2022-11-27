# Selenium webdriver
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
# Waited conditionals for Selenium
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# Dropdown selection support for selenium
from selenium.webdriver.support.select import Select
# Data Manipulations libraries
import pandas as pd
# Regular expressions library
import re
# Datetime functionalities
import time
# String manipulation
import string
# Mathematical operations
import numpy as np
# Biblioteca para leer archivos
import os
# Biblioteca para leer .env
from dotenv import load_dotenv
# Importamos la biblioteca para MongoDB
import pymongo
from pymongo import MongoClient
# Leer el arbol de html
from lxml import etree
# datetime library
import datetime
# download file with wget
import wget
# convert a webpage to pdf
# it requires a compiler
import pdfkit

def initializeWebDriver(grid = False, browser = "Chrome"):
    """
    This function enable to use the user browser to run automatizated 
    scripts to interact with it 
    """
    if browser == "Edge":
        browser_options = webdriver.EdgeOptions()
    if browser == "Firefox":
        browser_options = webdriver.FirefoxOptions()
    if browser == "Chrome":
        browser_options = webdriver.ChromeOptions()

    if grid == True:
        driver = webdriver.Remote(
            command_executor='http://localhost:4444',
            options = browser_options
        )
        # Maximizar la ventana
        driver.maximize_window()

    else:
        # Open the web browser
        if browser == "Edge":
            driver = webdriver.Edge()
        if browser == "Firefox":
            driver = webdriver.Firefox()
        if browser == "Chrome":
            # chrome_options = webdriver.ChromeOptions()
            # chrome_options.add_argument("--headless")
            # driver = webdriver.Chrome(chrome_options = chrome_options)
            driver = webdriver.Chrome()
        # Maximizar la ventana
        driver.maximize_window()
    
    return(driver)

def loginSIGMAA(driver, id_user, password):
    """
    Allows to login using user credentials into
    the SIGMAA
    """
    # Acceder al SIGMAA
    url = 'https://uclb.ucaribe.edu.mx/sigmaav2/'
    driver.get(url)

    # Buscar el campo de usuario y escribir el username
    userinput = driver.find_element(By.XPATH, '/html/body/div[2]/form/div/span[2]/input')
    userinput.send_keys(id_user)
    # Buscar el campo de contraseña y escribir el password
    passinput = driver.find_element(By.XPATH, '/html/body/div[2]/form/div/input')
    passinput.send_keys(password)
    # Buscar el botón de submit y dar clic para iniciar sesión
    submitinput = driver.find_element(By.XPATH, '/html/body/div[2]/form/button')
    submitinput.click()

    # Si se intenta loguear pero se queda en la misma página de logueo
    if driver.title == "Ingresar · SIGMAA - Unicaribe":
        # Inicio de sesion erroneo
        return(False)
    else:
        # Inicio de sesion exitoso
        return(True)

def loginSIPP(driver, id_user, password):
    """
    Allows to login using user credentials into 
    the SIPP
    """

    # Acceder al SIPP
    url = 'https://uclb.ucaribe.edu.mx/practicas/'
    driver.get(url)

    # Buscar el campo de usuario y escribir el username
    userinput = driver.find_element(By.XPATH, '/html/body/table/tbody/tr/td/form/table/tbody/tr[1]/td[2]/table/tbody/tr[1]/td/table/tbody/tr[1]/td[2]/input')
    userinput.send_keys(id_user)

    # Buscar el campo de contraseña y escribir el password
    passinput = driver.find_element(By.XPATH, '/html/body/table/tbody/tr/td/form/table/tbody/tr[1]/td[2]/table/tbody/tr[1]/td/table/tbody/tr[2]/td[2]/input')
    passinput.send_keys(password)
    # Buscar el botón de submit y dar clic para iniciar sesión
    submitinput = driver.find_element(By.XPATH, '/html/body/table/tbody/tr/td/form/table/tbody/tr[1]/td[2]/table/tbody/tr[1]/td/input')
    submitinput.click()

def loginSASS(driver, id_user, password):
    """ 
    Allows to login using user credentials into
    the SASS
    """

    # Acceder al SASS
    url = "https://uclb.ucaribe.edu.mx/sass/"
    driver.get(url)

    # Buscar el campo de usuario y escribir el username
    userinput = driver.find_element(By.XPATH, '/html/body/table/tbody/tr[2]/td/form/table/tbody/tr[1]/td/table/tbody/tr[1]/td/table/tbody/tr[1]/td[2]/input')
    userinput.send_keys(id_user)

    # Buscar el campo de contraseña y escribir el password
    passinput = driver.find_element(By.XPATH, '/html/body/table/tbody/tr[2]/td/form/table/tbody/tr[1]/td/table/tbody/tr[1]/td/table/tbody/tr[2]/td[2]/input')
    passinput.send_keys(password)
    # Buscar el botón de submit y dar clic para iniciar sesión
    submitinput = driver.find_element(By.XPATH, '/html/body/table/tbody/tr[2]/td/form/table/tbody/tr[1]/td/table/tbody/tr[1]/td/div/input')
    submitinput.click()

def getData(df, row, col):
    """
    This function allow us to fetch data depending on 
    a col and row number from a python dataframe
    """
    return(df.iloc[row, col])

def replaceNull(dictionary):
    """
    This function allows to replace nan values
    to False values in a recursive way
    """
    for k, v in dictionary.items():
        if type(v) == dict:
            replaceNull(v)

        else:
            if pd.isnull(v):
                dictionary[k] = ""

    return(dictionary)

def getPersonalInfo(driver, id_user, password):
    """
    This function allow us to fetch all student 
    data from the personal information section on SIGMAA
    """
    personal_information_section = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div/div/ul[2]/li[6]/a')
    personal_information_section.click()

    # Extraer la tabla usando webscrapping
    dfs = pd.read_html(driver.page_source)
    df = dfs[1]
    
    # Obtener el nombre
    username = getData(df, 0, 5)
    username = string.capwords(username)
    
    # Obtener el primer apellido
    first_lastname = getData(df, 0, 1)
    first_lastname = string.capwords(first_lastname)

    # Obtener el segundo apellido
    second_lastname = getData(df, 0, 3)
    second_lastname = string.capwords(second_lastname)

    # Obtener la CURP
    curp = getData(df, 1, 3)

    # Obtener el RFC
    rfc = getData(df, 1, 1)

    # Obtener la nacionalidad
    nationality = getData(df, 2, 3)

    # Obtener numero de seguridad social
    nss = getData(df, 3, 1)

    # Obtener correo personal
    personal_email = getData(df, 3, 3)

    # Obtener la fecha de nacimiento
    birthday = getData(df, 2, 5)

    # Obtener el sexo
    sex = getData(df, 1, 5)

    # Obtener el telefono personal
    personal_phone = getData(df, 5, 3)

    # Obtener el telefono de casa
    home_phone = getData(df, 5, 1)

    # Obtener el estado civil
    dropdown = driver.find_element(By.XPATH, "/html/body/center/table/tbody/tr[4]/td[1]/select")
    dropdown = Select(dropdown)
    marital_status = dropdown.first_selected_option.text

    # Obtener el domicilio personal
    personal_address = getData(df, 4, 1)

    # Obtener el pais de nacimiento
    dropdown = driver.find_element(By.XPATH, "/html/body/center/table/tbody/tr[12]/td/select")
    dropdown = Select(dropdown)
    birthplace_country = dropdown.first_selected_option.text

    # Obtener el codigo de pais de nacimiento
    birthplace_country_code = driver.find_element(By.XPATH, "/html/body/center/table/tbody/tr[12]/td/select")
    birthplace_country_code = birthplace_country_code.get_attribute("value")

    # Obtener la entidad federativa de nacimiento
    dropdown = driver.find_element(By.XPATH, "/html/body/center/table/tbody/tr[13]/td/span/select")
    dropdown = Select(dropdown)
    birthplace_state = dropdown.first_selected_option.text

    # Obtener la ciudad de nacimiento
    dropdown = driver.find_element(By.XPATH, "/html/body/center/table/tbody/tr[14]/td/span/select")
    dropdown = Select(dropdown)
    birthplace_city = dropdown.first_selected_option.text

    # Obtener el nombre completo del padre
    father_fullname = getData(df, 8, 1)

    # Obtener el nombre completo de la madre
    mother_fullname = getData(df, 8, 3)

    # Obtener el estado civil de los padres
    dropdown = driver.find_element(By.XPATH, "/html/body/center/table/tbody/tr[10]/th[4]/select")
    dropdown = Select(dropdown)
    parents_marital_status = dropdown.first_selected_option.text

    # Obtener el pais del bachillerato de procedencia
    dropdown = driver.find_element(By.XPATH, "/html/body/center/table/tbody/tr[16]/td/select")
    dropdown = Select(dropdown)
    highschool_country = dropdown.first_selected_option.text

    # Obtener la entidad federativa del bachillerato de procedencia
    dropdown = driver.find_element(By.XPATH, "/html/body/center/table/tbody/tr[17]/td/span/select")
    dropdown = Select(dropdown)
    highschool_state = dropdown.first_selected_option.text

    # Obtener el municipio/condado del bachillerato de procedencia
    highschool_municipality_county = getData(df, 16, 1)

    # Obtener la ciudad del bachillerato de procedencia
    highschool_city = getData(df, 16, 4)

    # Obtener el nombre del bachillerato de procedencia
    highschool_school = getData(df, 17, 1)

    # Obtener el campus del bachillerato de procedencia
    highschool_campus = getData(df, 18, 1)

    # Obtener el sistema escolar del bachillerato de procedencia (publico o privado)
    school_system = getData(df, 18, 3)

    # Averiguar si el estudiante trabaja
    working = getData(df, 6, 1)
    if working == "NO":
        working = "No trabajo"
    else:
        working = "Actualmente trabajo"

    # Obtener el nombre de la empresa donde se labora
    company_name = getData(df, 6, 3)

    # Obtener la direccion de la empresa donde se labora
    company_address = getData(df, 6, 5)

    # Obtener el numero de telefono de la empresa donde se labora
    work_phone = getData(df, 5, 5)


    # Ir a la seccion de la boleta escolar en SIGMAA
    grades_section =  driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div/div/ul[2]/li[4]/a')
    grades_section.click()

    # Extraer la tabla usando webscrapping
    dfs = pd.read_html(driver.page_source)

    # Nos quedamos con la tabla de los datos generales de estudiante
    df = dfs[0]

    # Obtenemos el nombre de la carrera
    career_name = getData(df, 1, 1).split(" / ")[1]

    # Obtenemos la situacion del estudiante
    situation = getData(df, 2, 1)

    # Obtener el estatus del estudiante
    status = getData(df, 3, 1)

    # Averiguar si el estudiante ha liberado el servicio social o no
    social_service = getData(df, 5, 1)
    # Si el estudiante no ha linerado el servicio aparecen --- en el campo
    if social_service == "---":
        # Fijar el servicio social en false
        social_service = "No liberado"
    # Si aparece otra cosa
    else:
        # El estudiante ha finalizado el servicio social
        social_service = "Liberado"

    # Obtenemos el plan de estudios al que pertenece el estudiante
    study_plan = getData(df, 1, 1).split(" / ")[0]

    # (Pendiente) Datos que faltan obtener - Default por el momento
    department = "Ciencias Básicas e Ingenierías"
    profile_picture = "profiles/default_avatar.jpg"
    current_practices = ""

    # Creamos un diccionario para almancenar los datos
    # que hemos obtenido usando webscrapping
    personal_information = {
        "id_user" : id_user,
        "password" : password,
        "username" : username,
        "first_lastname" : first_lastname,
        "second_lastname" : second_lastname,
        "profile_picture" : profile_picture,
        "curp" : curp,
        "rfc" : rfc,
        "nationality" : nationality,
        "nss" : nss,
        "personal_email" : personal_email,
        "birthday" : birthday,
        "sex" : sex,
        "personal_phone" : personal_phone,
        "home_phone" : home_phone,
        "marital_status" : marital_status,
        "personal_address" : personal_address,
        "birthplace" : {
            "country" : birthplace_country,
            "country_code" : birthplace_country_code,
            "state": birthplace_state,
            "city" : birthplace_city
        },
        "parents" : {
            "father_fullname" : father_fullname,
            "mother_fullname" : mother_fullname,
            "parents_marital_status" : parents_marital_status 
        },
        "highschool" : {
            "country" : highschool_country,
            "state" : highschool_state,
            "municipality" : highschool_municipality_county,
            "city" : highschool_city,
            "school" : highschool_school,
            "campus" : highschool_campus,
            "school_system" : school_system
        },
        "career" : {
            "name" : career_name, 
            "situation" : situation, 
            "status" : status, 
            "social_service" : social_service,
            "current_practices"  : current_practices,
            "study_plan" : study_plan, 
            "department" : department
        },
        "job" : {
            "working": working, 
            "name" : company_name, 
            "address" : company_address, 
            "phone" : work_phone
        }
    }

    # Aplicamos una funcion que permite eliminar valores nulos
    # en el diccionario y reemplazarlos por un valor False
    # La funcion recorre el diccionario usando recursividad
    personal_information = replaceNull(personal_information)

    # Retornamos el diccionario con la informacion personal
    return(personal_information)

def logoutSIGMAA(driver):
    """
    Allows to logout from SIGMAA
    """
    # Encontrar el botón de cierre de sesión
    logout = driver.find_element(By.XPATH, '/html/body/div[2]/div/form/a')
    # Clic para cerrar sesión
    logout.click()

def logoutSIPP(driver):
    """
    Allows to logout from SIPP
    """
    # Encontrar el botón de cierre de sesión
    logout = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[1]/ul/li[3]/a')
    # Clic para cerrar sesión
    logout.click()
    
def logoutSASS(driver):
    """ 
    Allows to logout from SASS
    """

    # Encontrar el botón de cierre de sesión
    logout = driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div[1]/ul/li[3]/a")
    # Clic para cerrar sesión
    logout.click()

def openMySQL(uri):
    """
    Creates a connection to database
    """
    # Creamos un engine usando la cadena de conexion y habilitando la conexion
    # segura a traves de Secure Socket Layer (SSL)
    engine = create_engine(uri + "?ssl=true")
    # Retornamos objeto engine
    return(engine)

def closeMySQL(engine):
    """
    Closes a MySQL connection
    """
    # Cerramos la sesión del engine
    engine.dispose()

def openMongoDB(uri):
    """
    Allows to open a mongoDB connection
    """
    # Creamon una conexion como cliente  
    # donde se recibe la cadena de conexión
    client = MongoClient(uri)
    # Retornamos el objeto cliente
    return(client)

def closeMongoDB(client):
    """
    Allows to close a mongoDB connection
    """
    # Cerramos el cliente
    client.close()

def loadEnvs(path):
    """
    This function returns all the environmental variables
    used to stablish database connections in both MySQL and MongoDB
    """
    load_dotenv(path)

    # Obtenemos las cadenas de conexion para MySQL y MongoDB
    MONGODB_URI = os.getenv('MONGODB_URI_2')
    
    return({
        "id_user" : "",
        "password" : "",
        "MONGODB_URI" : MONGODB_URI
    })

def getAcademicOffer(driver, study_plan):

    # Ir a la sección de las tablas de la oferta académica
    academic_offer_section = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div/div/ul[2]/li[1]/a')
    academic_offer_section.click()

    # xpath de pestañas
    tabs = [
        # Secciones
        '/html/body/center/ul/li[1]/a',
        # Talleres
        '/html/body/center/ul/li[2]/a',
        # Lengua Extranjera
        '/html/body/center/ul/li[3]/a'
    ]

    period_offer_title = driver.find_element(By.XPATH, "/html/body/center/div")
    academic_offer = {
        "study_plan": study_plan, 
        "period_offer_title" : period_offer_title.text
    }

    # Recorremos las pestañas y las enumeramos
    for index, t in enumerate(tabs):

        # Nombre de la tabla
        table_name = ""

        # Nombramos las tablas de acuerdo a su indice en las pestañas
        if index == 0:
            table_name = "aditionals"
        elif index == 1:
            table_name = "workshops"
        else:
            table_name = "foreign_languages"
        # print(table_name, end = "\n\n")

        # Cambiamos a cada pestaña
        tab = driver.find_element(By.XPATH, t)
        tab.click() 

        # Extraer las tablas de la pestaña actual
        dfs = pd.read_html(driver.page_source)

        td = 0

        # Si el indice de la pestaña es 0
        if index == 0:
            # La columna de las asignaturas está en la columna 4 para adicionales
            td = 4
            # Nombres para las columnas
            columns = ['type', 'id_subject', 'section', 'subject', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'U1', 'U2', 'U3', 'U4']
            # Columnas que se desean conservar
            desired_columns = ['type', 'id_subject', 'section', 'subject', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
        else:
            # La columna de las asignaturas está en la columna 3 para ingles y talleres
            td = 3
            # Nombres para las columnas
            columns = ['id_subject', 'section', 'subject', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'U1', 'U2', 'U3', 'U4', 'U5']
            # Columnas que se desean conservar
            desired_columns = ['id_subject', 'section', 'subject', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']

        # Recorre cada tabla en la pestaña actual
        for i in range(1, len(dfs)):
            # Renombra las columnas
            dfs[i] = dfs[i].set_axis(columns, axis=1)
            # Mantiene las columnas deseadas
            dfs[i] = dfs[i].loc[:, dfs[i].columns.isin(desired_columns)]

            if i == 1:
                academic_offer[table_name] = dfs[i]
            else:
                academic_offer[table_name] = pd.concat([academic_offer[table_name], dfs[i]], ignore_index = True)

        # print("Todas las asignaturas de la pestaña: ", end = "\n\n")
        # print(academic_offer[table_name])

        html = etree.HTML(driver.page_source)

        # Buscamos las asignaturas, profesores y modalidades usando XPath
        subjects = html.xpath("//table[contains(@class, 'datos')]/tbody/tr/td[" + str(td) + "]/b/text()")
        subjects = [subject.split("\n")[0] for subject in subjects]
        # print(subjects, end = "\n\n")

        tr_nodes = html.xpath("//table[contains(@class, 'datos')]/tbody/tr/td[" + str(td) + "]/text()[2]")
        teachers = [tr.split("\n                        ")[0] for tr in tr_nodes]
        # print(teachers, end = "\n\n")

        modalities = html.xpath("//table[contains(@class, 'datos')]/tbody/tr/td[" + str(td) + "]/span[contains(@style, 'color:#08c;')]/text()")
        # print(modalities)

        # Sobreescribimos la columna de asignaturas
        academic_offer[table_name]["subject"] = subjects

        # Insertamos a los profesores al dataframe
        academic_offer[table_name].insert(3, "teacher", teachers)
        # Insertamos las modalidades al dataframe
        academic_offer[table_name].insert(4, "modality", modalities)
    
        # Convertimos el dataframe de la seccion en un diccionario
        academic_offer[table_name] = dataframe2Dict(academic_offer[table_name])
    return(academic_offer)

def getGrades(driver, id_user):
    """
    This function allows to obtain the average grades tables from SIGMAA
    and returns a dictionary where the key is the period and the value is
    the dataframe with the data
    """
    # Ir a la sección de la boleta escolar
    school_grades_section = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div/div/ul[2]/li[4]/a')
    school_grades_section.click()


    # Selecionar el munu desplehable del periodo de escolar
    select = driver.find_element(By.XPATH, "/html/body/center/form/select")
    select = Select(select)

    # Obtener todos los posibles valores de menu desplegable
    periods = [[option.get_attribute("value"), option.text] for option in select.options]

    grades = dict()

    for period, text in periods:
        if period != "":
            # print("=======================================")
            # print("Periodo escolar: ", text, end = "\n\n")
            # Selecionar el munu desplehable del periodo de escolar
            dropdown = driver.find_element(By.XPATH, "/html/body/center/form/select")
            dropdown.send_keys(text)

            # Consultar ese periodo
            button = driver.find_element(By.XPATH, '/html/body/center/form/input[4]')
            button.click()

            # Obtener la tabla de calificaciones
            dfs = pd.read_html(driver.page_source)
            school_grades = dfs[1]

            # Cambiar nombre de columnas
            columns = ['number', 'type', 'section', 'subject', 'first_partial', 'second_partial', 'third_partial', 'average', 'final_grade', 'U1', 'U2']

            # Limpieza del dataframe de boleta
            # Cambiar nombre de columnas
            school_grades = school_grades.set_axis(columns, axis = 1)
            # Eliminar columnas no deseadas
            school_grades = school_grades.drop(['U1', 'U2'], axis = 1)
            # Eliminar filas con valores nulos
            school_grades.dropna(how = 'all', inplace = True)

            # print("Nombre de columnas")
            # print(list(school_grades.columns), end = "\n\n")

            # print("Dataframe de boleta")
            # print(school_grades, end = "\n\n")

            # Obtener los datos de la columna "Asignatura" por separado
            # Obtenemos el HTML de la vista actual
            html = etree.HTML(driver.page_source)

            # Obtenemos la lista de claves de asignatura
            id_subjects = html.xpath("//table[2]/tbody/tr/td[contains(@align, 'left')]/text()[1]")

            # Obtenemos los nombres de las asignaturas
            subjects = html.xpath("//table[2]/tbody/tr/td[contains(@align, 'left')]/b/text()[1]")

            # Obtenemos los profesores de cada asignatura
            tr_nodes = html.xpath("//table[2]/tbody/tr/td[contains(@align, 'left')]/text()[3]")
            teachers = [node.split("\n")[2].split("            ")[1] for node in tr_nodes]

            # Obtenemos las modalidades
            modalities = html.xpath("//table[2]/tbody/tr/td[contains(@align, 'left')]/span[contains(@style, 'color:#08c;')]/text()")

            # print("subjects: ", subjects)
            # print("id_subjects: ", id_subjects)
            # print("teachers: ", teachers)
            # print("modalities: ", modalities, end = "\n\n")

            # Sobreescribimos la columna de asignaturas
            school_grades["subject"] = subjects
            school_grades.insert(3, "id_subject", id_subjects)
            school_grades.insert(4, "teacher", teachers)
            school_grades.insert(5, "modality", modalities)

            # print("Nuevas columnas")
            # print(school_grades.columns)

            # print("Dataframe de boleta actualizado")
            # print(school_grades)
            
            # Guardamos la tabla de calificaciones actual en un diccionario
            # donde la llave es el periodo y el valor es el dataframe
            school_grades = school_grades.fillna("-")
            grades[period] = school_grades
    
    student_grades = {
        "id_user" : id_user,
        "grades" : {}
    }

    grades_list = []
    for period, dataframe in grades.items():
        
        grades_period = {
            "period" : period,
            "average_grades" : getAverageGrade(dataframe),
            "total_credits" : 0,
            "subject_grades" : dataframe2Dict(dataframe)
        }
        
        grades_list.append(grades_period)
    
    student_grades["grades"] = grades_list
    
    # Retornamos el diccionario con las calificaciones de todos
    # los periodos
    return(student_grades)

def getAverageGrade(grades_table):
    """
    This function allows to obtain the final average grade where the value is quantifiable 
    (subjects that are not english and sport/cultural workshops) and 
    where values are not nulls (it occurs when there is no a grade available in the table)
    """
    # Obtener las calificaciones finales
    # de las asignaturas cuantificables
    grades_list = [float(g) for g in grades_table["final_grade"] if g not in ["Aprobado", "Reprobado", "-"]]

    # Lista final de calificaciones sin valores nullos
    final_grades = []
    # Para cada calificacion cuantificable
    for gl in grades_list:
        # si no es un valor nulo, se adjunta a la lista
        if not np.isnan(gl):
            final_grades.append(gl)

    # print(final_grades)
    
    # Si la cantidad de las calificaciones es mayor a 0
    if len(final_grades) > 0:
        # Se calcula el promedio
        average_grades = np.mean(final_grades)
    # Si no hay calificaciones disponibles
    else:
        # El promedio por defecto es 0
        average_grades = 0

    # Retornamos el promedio de las calificaciones finales
    # del periodo escolar
    return(average_grades)

def getPracticesOffer(driver, student_information):
    """ 
    This function allow us to get the the whole list of practice offers for all
    the available periods in SIPP. The scrapper will get the aditional info
    for all the available offers and will return a list of diccionaries (one for
    each period)
    """
    # Dar clic en el dropdown del menu
    dropdown = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[1]/ul/li[2]/a')
    dropdown.click()

    # Ir a la oferta de proyectos
    projects_section = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[1]/ul/li[2]/ul/li[2]/a')
    projects_section.click()

    # Obtener el selector
    select = driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div[2]/div/div/div/div/div/table/tbody/tr/td[1]/table[1]/tbody/tr/td/form/fieldset/div/select")
    # Crear un objecto Select para interactuar con el
    select = Select(select)

    # Creamos una variable que almacene la lista de opciones
    # del dropdown
    options = []

    # Obtenemos una lista de las opciones disponibles en el dropdown
    for item in select.options:
        options.append(item.get_attribute("innerHTML"))

    # Print available dropdown options
    print("Opciones: ", options)

    # Lista de perioos de practicas disponibles
    available_offers = []
    # Para cada opcion en el dropdown
    for option in options:
        # Encontramos el dropdown de nuevo
        dropdown = driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div[2]/div/div/div/div/div/table/tbody/tr/td[1]/table[1]/tbody/tr/td/form/fieldset/div/select")
        # Enviamos la opcion actual
        dropdown.send_keys(option)
        
        # Encontramos el boton de la consulta
        search = driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div[2]/div/div/div/div/div/table/tbody/tr/td[1]/table[1]/tbody/tr/td/form/fieldset/input")
        # Damos clic en el boton
        search.click()
        
        # Creamos un diccionario donde meteremos los datos
        practices_offer = {
            "id_offer" : "",
            "career" : student_information["career"]["name"],
            "period" : option.split()[0],
            "offer" : {}
        }

        # practices_offer
        # Encontramos todos los enlaces para consultar más info de la practica
        botones = driver.find_elements(By.XPATH, "//table[contains(@class, 'tbuscar')]/tbody/tr/td[7]/a")

        # Creamos una lista para almacenar los url
        urls = []
        # para cada boton extraemos su link
        for b in botones:
            # Guardamos cada link en la lista anterior
            urls.append(str(b.get_attribute("href")))

        # Imprimimos los links encontrados y la cantidad
        # print("Links: " + str(len(urls)))
        # print(urls)

        def getCompanyInfo(driver):
            """
            This function allows us to extract the data 
            inside each form when a 'more info' button is
            pressed in the list of companies offered 
            in the SIPP
            """
            # Encontramos las etiquetas html donde se encuentra la info
            # que nos interesa
            form_data = driver.find_elements(By.XPATH, "//valor")
            # Extraemos el texto de cada etiqueta en una lista
            data = [datum.text for datum in form_data]
            # Extraemos la direccion email del campo con la info
            email = re.search(r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", data[8]) # Get the email

            # Si el email no se encuentra
            if email == None:
                # Se fija este campo en cadena vacia
                email = ""
            # Si el email se encuentra usando regex
            else:
                # Se obtiene el texto del email encontrado
                email = email.group(0)

            # Imprimimos la lista de datos encontrados en formulario  
            # print(data)

            # Creamos un diccionario con los datos encontrados
            # y les datos nombres
            information = {
                "id_practice" : data[1].split(" / ")[0],
                "practice_name" : data[1].split(" / ")[1],
                "company_name" : data[0],
                "required_practitioners" : data[2],
                "available_spaces" : data[3],
                "type" : data[4],
                "endeavor" : data[5],
                "activities" : data[6],
                "required_english" : data[7] + "%",
                "contact_info" : data[8],
                "email" : email,
                "teacher" : data[9], 
                "comments" : data[10] 
            }

            # Returnamos el diccionario creado
            return(information)

        # Lista donde se guardarán los diccionarios 
        # con la información adicional consultada de 
        # cada empresa en la oferta (en el periodo previamente
        # seleccionado)
        info = []
        # Para cada url en la lista de urls
        for url in urls:
            # Vamos ese link
            driver.get(url)
            # Guardamos la informaciön extraida del formulario en la lista de 
            # información de las ofertas (aqui se guardan los diccionarios)
            info.append(getCompanyInfo(driver))
            # Regresar a la pagina anterior para repetir el proceso iterativamente
            driver.back()

        # En un diccionario final de practicas, guardamos la lista de diccionarios
        # en el campo "offer"
        practices_offer["offer"] = info
        practices_offer["id_offer"] = info[0]["id_practice"]
        # Guardamos este diccionario en una lista que contiene la info de todos los periodos
        # disponibles en el SIPP (Ej. 202202 Verano, 202203 Otoño...)
        available_offers.append(practices_offer)

    # Retornamos la lista con los diccionarios de las ofertas
    # que contienen la información de las ofertas de practicas
    return(available_offers)

def dataframe2Dict(dataframe):
    """
    This function allows to convert a dataframe to a
    dictionary (JSON like) object
    """
    # Convertir una dataframe a un diccionario
    data_dict = dataframe.to_dict("records")
    # Retornamos el diccionario
    return(data_dict)

def getSocialServiceOffer(driver):
    """ 
    This function allows to get the offer of the social service.
    It returns a diccionary with two list, one for internal projects and 
    another for the external projects. 
    """

    # Nos dirigimos a la seccion de la oferta de servicio social
    driver.get("https://uclb.ucaribe.edu.mx/sass/ofertaAction.do?accion=oferta")
    # Obtenemos los botones de "ver mas" informacion
    buttons = driver.find_elements(By.XPATH, "//table[contains(@class, 'tencabezado')]/tbody/tr/td/form/input[contains(@name, 'uiCveProyecto')]")
    # Una lista para almacenar el atributo value que se extraen del boton (es un input que se envia a un formulario usando POST)
    values = []
    # Para cada boton encontrado obtenemos el atributo value
    for button in buttons:
        # Guardamos el atributo encontrado
        values.append(button.get_attribute("value"))

    def getSocialServiceInfo(driver, id):
        """ 
        This is an internal function that allows to get the informacion
        of the company where you can do your social service
        """

        # Obtenemos los datos generales del proyecto como: tipo, titulo, organizacion, asesor, descripcion y espacios
        type = driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div[2]/div/div/div/div/div/table/tbody/tr/td/table/tbody/tr/td[1]/table[2]/tbody/tr[1]/th").text
        title = driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div[2]/div/div/div/div/div/table/tbody/tr/td/table/tbody/tr/td[1]/table[2]/tbody/tr[2]/td/span[1]").text
        organization = driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div[2]/div/div/div/div/div/table/tbody/tr/td/table/tbody/tr/td[1]/table[2]/tbody/tr[2]/td/span[2]").text
        assessor = driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div[2]/div/div/div/div/div/table/tbody/tr/td/table/tbody/tr/td[1]/table[2]/tbody/tr[2]/td/span[3]").text
        description = driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div[2]/div/div/div/div/div/table/tbody/tr/td/table/tbody/tr/td[1]/table[2]/tbody/tr[3]/td/span[1]").text
        spaces = driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div[2]/div/div/div/div/div/table/tbody/tr/td/table/tbody/tr/td[1]/table[2]/tbody/tr[3]/td/span[2]").text

        # Obtenemos los datos de la tabla con informacion especifica del proyecto, como: estado, municipio, colonia, codigo postal, ubicacion, telefono
        # fax, campo, sector, si ofrece apoyo economico, diracion del proyecto, idiomas requeridos, sexo requerido, carrera, departamento, horas por semana y clasificacion
        state = driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div[2]/div/div/div/div/div/table/tbody/tr/td/table/tbody/tr/td[1]/table[4]/tbody/tr[1]/td").text
        municipality = driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div[2]/div/div/div/div/div/table/tbody/tr/td/table/tbody/tr/td[1]/table[4]/tbody/tr[2]/td").text
        city = driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div[2]/div/div/div/div/div/table/tbody/tr/td/table/tbody/tr/td[1]/table[4]/tbody/tr[3]/td").text
        cologne = driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div[2]/div/div/div/div/div/table/tbody/tr/td/table/tbody/tr/td[1]/table[4]/tbody/tr[4]/td").text
        zip_code = driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div[2]/div/div/div/div/div/table/tbody/tr/td/table/tbody/tr/td[1]/table[4]/tbody/tr[5]/td").text
        location = driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div[2]/div/div/div/div/div/table/tbody/tr/td/table/tbody/tr/td[1]/table[4]/tbody/tr[6]/td").text
        phone = driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div[2]/div/div/div/div/div/table/tbody/tr/td/table/tbody/tr/td[1]/table[4]/tbody/tr[7]/td").text
        fax = driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div[2]/div/div/div/div/div/table/tbody/tr/td/table/tbody/tr/td[1]/table[4]/tbody/tr[8]/td").text
        field = driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div[2]/div/div/div/div/div/table/tbody/tr/td/table/tbody/tr/td[1]/table[4]/tbody/tr[9]/td").text
        sector = driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div[2]/div/div/div/div/div/table/tbody/tr/td/table/tbody/tr/td[1]/table[4]/tbody/tr[10]/td").text
        economical_support = driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div[2]/div/div/div/div/div/table/tbody/tr/td/table/tbody/tr/td[1]/table[4]/tbody/tr[11]/td").text
        duration = driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div[2]/div/div/div/div/div/table/tbody/tr/td/table/tbody/tr/td[1]/table[4]/tbody/tr[12]/td").text
        required_language = driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div[2]/div/div/div/div/div/table/tbody/tr/td/table/tbody/tr/td[1]/table[4]/tbody/tr[13]/td").text
        required_sex = driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div[2]/div/div/div/div/div/table/tbody/tr/td/table/tbody/tr/td[1]/table[4]/tbody/tr[14]/td").text
        career = driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div[2]/div/div/div/div/div/table/tbody/tr/td/table/tbody/tr/td[1]/table[4]/tbody/tr[15]/td").text
        department = driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div[2]/div/div/div/div/div/table/tbody/tr/td/table/tbody/tr/td[1]/table[4]/tbody/tr[16]/td").text
        hours_per_week = driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div[2]/div/div/div/div/div/table/tbody/tr/td/table/tbody/tr/td[1]/table[4]/tbody/tr[17]/td").text
        classification = driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div[2]/div/div/div/div/div/table/tbody/tr/td/table/tbody/tr/td[1]/table[4]/tbody/tr[18]/td").text

        # Concentramos toda la informacion del proyecto
        #  en un diccionario
        project = {
            "id" : id,
            "type" : type,
            "title" : title,
            "organization" : organization,
            "assessor" : assessor.split("Asesor: ")[1],
            "description" : description,
            "spaces" : spaces.split()[1],
            "aditional_information" : {
                "state" : state,
                "municipality" : municipality,
                "city" : city,
                "cologne" : cologne,
                "zip_code" : zip_code,
                "location" : location,
                "phone" : phone,
                "fax" : fax,
                "field" : field,
                "sector" : sector,
                "economical_support" : economical_support,
                "duration" : duration,
                "required_language" : required_language,
                "required_sex" : required_sex,
                "career" : career,
                "department" : department,
                "hours_per_week" : hours_per_week,
                "classification" : classification
            } 
        }

        # Regresamos el diccionario con la info
        return(project)

    # Una lista para almacenar los diccionarios con la informacion de cada oferta de servicio social
    projects = []
    # Para cada atributo "valor" 
    for value in values:
        # Enviamos los datos del formulario usando POST con el valor del atributo "value"
        # Con esto carga la informacion de la oferta para cada empresa
        driver.get("https://uclb.ucaribe.edu.mx/sass/ofertaAction.do?accion=ver&uiCveProyecto=" + str(value))
        # Guardamos en la lista el diccionario con la info de la oferta de la empresa
        projects.append(getSocialServiceInfo(driver, str(value)))
        # Regresamos a la pagina anterior y repetimos el proceso hasta que se acaben 
        # los value
        driver.back()
        
    # Separamos los proyectos internos de los proyectos externos en dos listas diferentes 
    # para cada oferta en la lista de diccionarios principal
    external_projects = [p for p in projects if p["type"] == "Proyecto Externo"]
    internal_projects = [p for p in projects if p["type"] == "Proyecto Interno"]

    # Creamos un diccionario final con los datos organizados
    social_service_offer = {
        "title" : "social_service_offer",
        "internal_projects" : internal_projects,
        "external_projects" : external_projects
    }

    # Retornamos el diccionario con la oferta de servicio social
    return(social_service_offer)

def getPayments(driver, id_user):
    # Ir a la seccion de pagos
    payments_section = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div/div/ul[2]/li[7]/a')
    payments_section.click()
    # Extraer las tablas con la información
    dfs = pd.read_html(driver.page_source)
    # Extraer la tabla con la informacion de los pagos
    payments = dfs[0].drop(['Opciones', 'Opciones.1'], axis = 1)
    # Nombres de las columnas para la tabla de pagos
    columns = ["number", "id", "period", "date", "description", "amount", "expiration", "status"]
    # Renombramos las columnas de la tabla de pagos
    payments = payments.set_axis(columns, axis = 1)
    # Convertimos la tabla a una lista de diccionarios
    payments = dataframe2Dict(payments)
    # Extraemos el documento del pago por realizar
    button = driver.find_elements(By.XPATH, "//table[contains(@class, 'datos')]/tbody/tr/td[9]/a")
    
    # Si se encontro un enlace de pago
    if len(button) > 0:
        # Obtenemos la url de la pagina con los datos de pago
        url = button[0].get_attribute("href")
        # Guardamos esa pagina como un PDF
        pdfkit.from_url(url, "payment_" + id_user + ".pdf")
    
    # Concentramos la informacion de los pagos en un diccionario
    # con la informacion del estudiante y la lista de diccionarios con pagos
    payments_info = {
        "id_user" : id_user,
        "payments" : payments
    }
    
    # Retornamos el diccionario con datos de los pagos
    return(payments_info)

