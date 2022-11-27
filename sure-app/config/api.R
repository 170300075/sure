library(httr)
library(jsonlite)
library(dplyr)

# Ruta base
env_path <- paste0(getwd(), "/config/.env")
# Leer variables de ambiente
readRenviron(env_path)
# Obtener cadena de conexion a base de datos
api_url <- Sys.getenv("API_URL")


get <- function(endpoint = ""){
    # URI root de la API
    root <- api_url
    # Construimos la uri de consulta
    uri <- paste0(root, endpoint)
    # Obtenemos el resultado de la API
    res <- GET(uri)
    # Convertimos a lista
    result <- fromJSON(rawToChar(res$content))
    # Retornamos el resultado
    return(result)
}

post <- function(endpoint = ""){
    # URI root de la API
    root <- api_url
    # Construimos la uri de consulta
    uri <- paste0(root, endpoint)
    # Obtenemos el resultado de la API
    res <- POST(uri)
    # Convertimos a lista
    result <- fromJSON(rawToChar(res$content))
    # Retornamos el resultado
    return(result)
}

# Obtener el numero de recomendaciones automaticas autogeneradas
get_n_recommendations <- function(id_user) {
    res <- get(paste0("generator/read/", id_user, "/availability"))
    return(0:(res-1))
}

# Obtener recomendacion automatica por index
get_recommendation <- function(id_user, index) {
    res <- get(paste0("generator/read/", id_user, "/", index))
    return(res)
}

# Registrar un nuevo usuario en la base de datos
register_new_user <- function(id_user, password) {
    root <- api_url

    # Endpoint para la consulta
    endpoint <- paste0(root, "webscraper/register?id_user=", id_user, "&password=", password)
    
    # Realizar consulta al endpoint POST
    res <- POST(endpoint)
    # Extraer datos del JSON
    res <- fromJSON(rawToChar(res$content))
    return(res)
}

# Obtener la foto de perfil de instagram
get_profile_picture <- function(id_user) {
    data <- get(paste0("profile_picture/", id_user))
    return(data)
}

# Obtener el mapa curricular de un estudiante
get_curricular_map <- function(id_user) {
    data <- get(paste0("curricular_map_student/", id_user))
}

# Obtener los datos del estudiante
get_user_data <- function(id_user) {
    data <- get(paste0("user/", id_user))
    return(data)
}

get_user_last_updated <- function(id_user) {
    data <- get(paste0("user/", id_user, "/last_updated"))
    return(data)
}

validate_credentials <- function(id_user, password){
    data <- post(paste0("credentials?id_user=", id_user, "&password=", password))
    return(data)
}

generate_token <- function(id_user) {
    data <- post(paste0("token?id_user=", id_user)) 
    return(data)
}

validate_token <- function(token) {
    data <- post(paste0("token/validate?token=", token))
    return(data)
}


# Obtener los datos de pagos del estudiante
get_payments <- function(id_user) {
    data <- get(paste0("payments/", id_user))
    return(data)
}

# Obtener la última fecha de actualización de la tabla de pagos y adeudos
get_payments_last_updated <- function(id_user) {
    data <- get(paste0("payments/", id_user, "/last_updated"))
    return(data)
}


# Obtener los créditos por ciclo del estudiante
get_credits <- function(id_user) {
    data <- get(paste0("credits/", id_user))
    return(data)
}

# Obtener la lista de periodos disponibles del estudiante
get_periods <- function(id_user) {
    data <- get(paste0("grades/", id_user, "/periods"))
    return(data)
}

# Obtener la boleta de calificaciones dependiendo del periodo
get_grades_per_period <- function(id_user, period) {
    data <- get(paste0("grades/", id_user, "/", period))
    return(data)
}

# Obtener la ultima fecha de actualización de las boletas de calificaciones
get_grades_last_updated <- function(id_user) {
    data <- get(paste0("grades/", id_user, "/last_updated"))
    return(data)
}

# Obtener los promedios generales de cada periodo disponible para el estudiante
get_average_grades <- function(id_user) {
    data <- get(paste0("grades/", id_user, "/averages"))
    return(data)
}

## Obtener el horario academico de un estudiante
get_student_schedule <- function(id_user) {
    data <- get(paste0("student_schedule/", id_user))
    return(data)
}

# Obtener la oferta academica, ya sea inclusiva, exclusiva u obligatoria
get_academic_offer <- function(id_user, option) {
    data <- get(paste0("academic_offer_for_student/", id_user, "/", option))
    return(data)
}

# Obtener la última fecha de actualización de la oferta académica
get_academic_offer_last_updated <- function(study_plan) {
    data <- get(paste0("academic_offer/", study_plan, "/last_updated"))
    return(data)
}

# Obtener la oferta de prácticas profesionales por id_subject y period
get_practices_offer_per_period <- function(id_subject, period) {
    data <- get(paste0("professional_practices/", id_subject, "/", period))
    return(data)
}

# Obtener la última fecha de actualización de la oferta de prácticas
get_practices_last_updated <- function(id_subject, period) { 
    data <- get(paste0("professional_practices/", id_subject, "/", period, "/last_updated"))    
    return(data)
}

# Obtener periodos de ofertas disponibles para las práctica profesionales
get_practices_offer_periods <- function() {
    data <- get("professional_practices/periods")
    return(data)
}

# Obtener la oferta de servicio social
get_social_service_offer <- function() {
    data <- get("social_service/")
    return(data)
}

# obtener la última fecha de actualizacion de la oferta de servicio social
get_social_service_last_updated <- function() {
    data <- get(paste0("social_service/last_updated"))
    return(data)
}

## Obtener las fechas del calendario
get_calendar <- function(year) {
    data <- get(paste0("calendar/", year))
    return(data)
}

## Obtener los estados de las evaluaciones al desempeño docente
get_teachers_evaluation <- function(id_user) {
    data <- get(paste0("teachers_evaluation/", id_user))
    return(data)
}

## Obtener la última fecha de actualización de la evaluación al desempeño docente
get_teachers_evaluation_last_updated <- function(id_user) {
    data <- get(paste0("teachers_evaluation/", id_user, "/last_updated"))
    return(data)
}

## Obtener la tabla con promedio general y promedio del ultimo period
get_indicators <- function(id_user) {
    data <- get(paste0("indicators/", id_user, "/period_averages"))
    return(data)
}

## Obtener el tiempo de permanencia del estudiante
get_dwell_time <- function(id_user) {
    data <- get(paste0("user/", id_user, "/dwell_time"))
    return(data)
}

# Obtener la recomendacion de acuerdo a la seleccion academica
model <- function(id_user, bucket){
    root <- api_url
    res <- POST(
        url = paste0(root, paste0("model?id_user=", id_user)), 
        body = toJSON(bucket),
        encode = "json"
    )
    
    return(fromJSON(rawToChar(res$content)))
}