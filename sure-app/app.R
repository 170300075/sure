#################################
#           Libraries           #
#################################

library(bslib)          # Agregar bootstrap 5
library(bs4Dash)        # Agregar bs4Dash
library(shinytoastr)    # Agregar toastr
library(waiter)         # Agregar pantalla de carga
library(toastui)        # Agregar toast ui
library(ggplot2)        # Agregar datasets de ggplot2
library(dplyr)          # Agregar manipulacion de datos dplyr
library(DiagrammeR)     # Agregar soporte de diagramas mermaid
library(shinyWidgets)   # Agregar widget a shiny
library(httr)           # Agregar funcionaldad para fetch API
library(jsonlite)
library(mapboxer)       # Agregar mapas de mapbox
library(stringr)        # Argegar manejo de cadenas
library(highcharter)    # Agregar gráficas de highchart
library(tidyr)

# Instalación -> devtools::install_github("colearendt/shinycookie")
library(shinycookie)    # Agregar cookies


#################################
#           Components          #
#################################

# Importar widgets personalizados
source("matriculaInput.R")
source("contraseñaInput.R")

# Importar componentes de aplicacion
components_path <- paste0(getwd(), "/components/")
source(paste0(components_path, "login.R"))
source(paste0(components_path, "register.R"))
source(paste0(components_path, "dashboard.R"))

# Importar archivos de configuración
config_path <- paste0(getwd(), "/config/")
source(paste0(config_path, "api.R"))

# La pagina principal
ui <- div(
  tags$head(
    tags$link(rel = "icon", type = "image/png", href = "logo.png"),
    tags$script(src = "bootstrap.bundle.min.js"),
    tags$link(rel = "stylesheet", type="text/css", href="bootstrap.min.css")
  ),
  
  div(
    id = "container",

    # Inicializar bibliotecas
    initShinyCookie("sure"), # Crear un token sure
    useToastr(), # Inicializar toastui
    useWaiter(), # Inicializar waiter
  )
)

server <- function(input, output, session){

  ####################################
  #    Definir variables reactivas   #
  ####################################
  data <- reactiveValues()

  observe({

    # Si el token de acceso existe
    if(!is.null(input$sure$token)) {
      # Si el token está para registro
      if(input$sure$token == "register") {
        # Remover el login/dashboard
        removeUI(selector = "#login")
        removeUI(selector = "#dashboard")

        # Insertar el formulario de registro
        insertUI(selector = "#container", where = "afterBegin", register)
      }

      # Si el token está para iniciar sesión
      else if(input$sure$token == "login") {
        # Remover el registro/dashboard
        removeUI(selector = "#register")
        removeUI(selector = "#dashboard")

        # Insertar el formulario de inicio de sesión
        insertUI(selector = "#container", where = "afterBegin", login)
      }

      # Si el token no está para ninguno de los anteriores
      else {
        # Comprobamos que el token actual pertenezca a un usuario y no haya expirado
        data$id_user <- validate_token(input$sure$token)

        # Si el token contiene un string con el id_user
        if(class(data$id_user) == "character") {
          # El token es válido, se obtienen datos de usuario y monta el dashboard
          
          # Remover el login/register
          removeUI(selector = "#login")
          removeUI(selector = "#register")
          
          # Mostrar barra de carga
          waiter_show(html = spin_fading_circles())

          # Obtener datos del estudiante
          data$user_data <- get_user_data(data$id_user)
          data$credits <- get_credits(data$id_user)
          data$periods <- get_periods(data$id_user)

          # Insertar el dashboard
          insertUI(selector = "#container", where = "afterBegin", dashboard)

          # Ocultar barra de carga
          waiter_hide()
        }

        # En otro caso, será una lista con un mensaje de error
        else {
          # El token es inválido y se actualiza la cookie al login
          updateCookie(session, "token" = "login")
        }
      }
    }

    # Si el token de acceso no existe
    else {
      # Se inicializa por default al login
      updateCookie(session, "token" = "login")
    }

  })

  observe({
    print(input$id_user)
    print(input$password)
    print(input$password_match)
  })

  # Si se presiona el botón de login
  observeEvent(input$login, {
    # Comprobar que los campos de las credenciales no estén vacíos
    if( !is.null(input$id_user) & !is.null(input$password) & input$id_user != "" & input$password != "" ) {

      # Obtener el resultado de validación consultando a la API
      data$validate_credentials <- validate_credentials(input$id_user, input$password)
      # print(data$validate_credentials)

      if(class(data$validate_credentials) != "list") {
        # Si las credenciales son correctas
        if(data$validate_credentials == TRUE) {
          # Generar un token nuevo para la sesión del usuario y guardarlo en cookies
          updateCookie(session, "token" = generate_token(input$id_user))
        }

        # Si las credenciales son incorrectas
        else {
          print("Credenciales incorrectas")
        }
      }

      # Si no es ninguna de las anteriores
      else{
        # El usuario no existe
        print("Usuario no está registrado")
      }
    }

    # Si algún campo está vacio
    else {
      # Se muestra un mensaje con el error
      print("Credenciales incompletas")
    }
  })


  # Si se presiona el botón de registro
  observeEvent(input$register, {
    # Mostrar barra de carga
    waiter_show(html = spin_fading_circles())

    # Si el password no coincide con el match
    if(input$password == input$password_match) {
      # Si se pudo registrar el usuario
      if(register_new_user(input$id_user, input$password) == TRUE) {
        print("Usuario registrado!")

        # Generar un token nuevo para la sesión del usuario y guardarlo en cookies
        updateCookie(session, "token" = generate_token(input$id_user))
      }

      else {
        print("El usuario no se pudo registrar")
      }
    }

    # Si no coinciden
    else {
      # Se envia mensaje de erro
      print("Las contraseñas no coinciden")
    }

    # Ocultar barra de carga
    waiter_hide()
  })

  # Si se cierra sesion
  observeEvent(input$logout, {
    print("Cerrando sesion")
    # Fijar token para login
    updateCookie(session, "token" = "login")
    session$reload()
  })

  ##########################################
  #       Renderizar widgets de header     #
  ##########################################

  # Renderizar logout de usuario
  output$user <- renderUser({
    # Rellenar widget con informacion de estudiante
    dashboardUser(
      name = data$user_data$username,
      image = data$user_data$profile_picture,
      title = data$user_data$career$name,
      subtitle = data$user_data$career$department,
      # Definir color del widget
      status = "white",
      # Definir elementos del footer
      footer = fluidRow(
        dashboardUserItem(
          width = 12,
          actionButton(
            inputId = "logout",
            label = "Cerrar sesión",
            icon = icon("right-from-bracket"),
            width = "80%",
            status = "primary",
            outline = TRUE,
            size = "sm"
          )
        )
      )
    )
  })
    
  ##########################################
  #       Renderizar widgets de sidebar    #
  ##########################################

  ##########################################
  #       Renderizar widgets de body       #
  ##########################################

  # Renderizar el mapa curricular de la carrera
  output$curricular_map <- renderUI({
    img(src = "./images/curricular_maps/2016ID.jpg", width = "100%")
  })

  # Renderizar cajas de información de ciclos del estudiante
  output$first_cycle <- renderInfoBox({
    # Obtener los créditos del ciclo
    data$first_cycle_credits <- data$credits[1, "credits"]
    data$first_cycle_req_credits <- data$credits[1, "req_credits"]
    print(data$first_cycle)
    print(data$first_cycle)

    # Asignar un color
    if(data$first_cycle_credits < data$first_cycle_req_credits) {
      data$first_cycle_subtitle <- em("Cursando")
      data$first_cycle_icon <- icon("circle-notch", class="fa-spin fa-sping-reverse")
      data$first_cycle_color <- "info"
    } else {
      data$first_cycle_subtitle <- em("Concluido")
      data$first_cycle_icon <- icon("check-circle")
      data$first_cycle_color <- "lime"
    }

    infoBox(
      title = "1er ciclo",
      value = paste0("Créditos: ", data$first_cycle_credits, "/", data$first_cycle_req_credits),
      subtitle = data$first_cycle_subtitle,
      icon = data$first_cycle_icon,
      color = data$first_cycle_color,
      elevation = 2,
      iconElevation = 0,
      gradient = TRUE,
      fill = TRUE
    )
  })

  output$second_cycle <- renderInfoBox({
    # Obtener los créditos del ciclo
    data$second_cycle_credits <- data$credits[2, "credits"]
    data$second_cycle_req_credits <- data$credits[2, "req_credits"]
    print(data$second_cycle)
    print(data$second_cycle)

    # Asignar un color
    if(data$second_cycle_credits < data$second_cycle_req_credits) {
      data$second_cycle_subtitle <- em("Cursando")
      data$second_cycle_icon <- icon("circle-notch", class="fa-spin fa-sping-reverse")
      data$second_cycle_color <- "info"
    } else {
      data$second_cycle_subtitle <- em("Concluido")
      data$second_cycle_icon <- icon("check-circle")
      data$second_cycle_color <- "lime"
    }

    infoBox(
      title = "2do ciclo",
      value = paste0("Créditos: ", data$second_cycle_credits, "/", data$second_cycle_req_credits),
      subtitle = data$second_cycle_subtitle,
      icon = data$second_cycle_icon,
      color = data$second_cycle_color,
      elevation = 2,
      iconElevation = 0,
      gradient = TRUE,
      fill = TRUE
    )
  })

  output$third_cycle <- renderInfoBox({
    # Obtener los créditos del ciclo
    data$third_cycle_credits <- data$credits[3, "credits"]
    data$third_cycle_req_credits <- data$credits[3, "req_credits"]
    print(data$third_cycle)
    print(data$third_cycle)

    # Asignar un color
    if(data$third_cycle_credits < data$third_cycle_req_credits) {
      data$third_cycle_subtitle <- em("Cursando")
      data$third_cycle_icon <- icon("circle-notch", class="fa-spin fa-sping-reverse")
      data$third_cycle_color <- "info"
    } else {
      data$third_cycle_subtitle <- em("Concluido")
      data$third_cycle_icon <- icon("check-circle")
      data$third_cycle_color <- "lime"
    }

    infoBox(
      title = "3er ciclo (Básicas)",
      value = paste0("Créditos: ", data$third_cycle_credits, "/", data$third_cycle_req_credits),
      subtitle = data$third_cycle_subtitle, # em("Reprobaciones: 1", class = "text-warning"),
      icon = data$third_cycle_icon, # icon("exclamation-circle", class = "fa-beat-fade"),
      color = data$third_cycle_color, # "danger",
      elevation = 2,
      iconElevation = 0,
      gradient = TRUE,
      fill = TRUE
    )
  })

  output$fourth_cycle <- renderInfoBox({
    # Obtener los créditos del ciclo
    data$fourth_cycle_credits <- data$credits[4, "credits"]
    data$fourth_cycle_req_credits <- data$credits[4, "req_credits"]
    print(data$fourth_cycle)
    print(data$fourth_cycle)

    # Asignar un color
    if(data$fourth_cycle_credits < data$fourth_cycle_req_credits) {
      data$fourth_cycle_subtitle <- em("Cursando")
      data$fourth_cycle_icon <- icon("circle-notch", class="fa-spin fa-sping-reverse")
      data$fourth_cycle_color <- "info"
    } else {
      data$fourth_cycle_subtitle <- em("Concluido")
      data$fourth_cycle_icon <- icon("check-circle")
      data$fourth_cycle_color <- "lime"
    }

    infoBox(
      title = "4to ciclo (Básicas)",
      value = paste0("Créditos: ", data$fourth_cycle_credits, "/", data$fourth_cycle_req_credits),
      subtitle = data$fourth_cycle_subtitle, # em("Sin comenzar") # , class = "text-muted"),
      icon = data$fourth_cycle_icon, # icon("pause-circle", class = "fa-fade"),
      color = data$fourth_cycle_color, # "gray-dark",
      elevation = 2,
      iconElevation = 0,
      gradient = TRUE,
      fill = TRUE
    )
  })

  output$other_subjects <- renderInfoBox({
    # Obtener los créditos del ciclo
    data$other_subjects_credits <- data$credits[5, "credits"]
    data$other_subjects_req_credits <- data$credits[5, "req_credits"]
    print(data$other_subjects)
    print(data$other_subjects)

    # Asignar un color
    if(data$other_subjects_credits < data$other_subjects_req_credits) {
      data$other_subjects_subtitle <- em("Cursando")
      data$other_subjects_icon <- icon("circle-notch", class="fa-spin fa-sping-reverse")
      data$other_subjects_color <- "info"
    } else {
      data$other_subjects_subtitle <- em("Concluido")
      data$other_subjects_icon <- icon("check-circle")
      data$other_subjects_color <- "lime"
    }

    infoBox(
      title = "3er/4to ciclo (ELIB)",
      value = paste0("Créditos: ", data$other_subjects_credits, "/", data$other_subjects_req_credits),
      subtitle = data$other_subjects_subtitle,
      icon = data$other_subjects_icon,
      color = data$other_subjects_color,
      elevation = 2,
      iconElevation = 0,
      gradient = TRUE,
      fill = TRUE
    )
  })

  output$prespeciality <- renderInfoBox({

    #########
    # Si la preespecialidad está definida
    if(data$credits[6, "credits"] + data$credits[7, "credits"] > 0) {
      # Averiguar cual preespecialidad está definida
      data$n <- ifelse(data$credits[6, "credits"] > data$credits[7, "credits"], 6, 7)
      
      data$pre_especialidad_credits <- data$credits[data$n, "credits"]
      data$pre_especialidad_req_credits <- data$credits[data$n, "req_credits"]
      data$pre_especialidad <- data$credits[data$n, "school_year"]
      
      if(data$pre_especialidad_credits < data$pre_especialidad_req_credits) {
        data$pre_especialidad_subtitle <- em("Cursando")
        data$pre_especialidad_icon <- icon("circle-notch", class = "fa-spin fa-sping-reverse")
        data$pre_especialidad_color <- "info"
      }

      else {
        data$pre_especialidad_subtitle <- em("Concluido")
        data$pre_especialidad_icon <- icon("check-circle")
        data$pre_especialidad_color <- "lime"
      }

      data$pre_especialidad_value <- paste0("Créditos: ", data$pre_especialidad_credits, "/", data$pre_especialidad_req_credits)
    }

    # Si no la preespecialidad está definida
    else{
      data$pre_especialidad <- "Preespecialidad indefinida"
      data$pre_especialidad_credits <- "No disponible"
      data$pre_especialidad_req_credits <- 0
      data$pre_especialidad_subtitle <- em("Sin comenzar")
      data$pre_especialidad_icon <- icon("pause-circle", class = "fa-fade")
      data$pre_especialidad_color <- "gray-dark"
      data$pre_especialidad_value <- br()
    }

    infoBox(
      title = data$pre_especialidad,
      value = data$pre_especialidad_value,
      subtitle = data$pre_especialidad_subtitle,
      icon = data$pre_especialidad_icon,
      color = data$pre_especialidad_color,
      elevation = 2,
      iconElevation = 0,
      gradient = TRUE,
      fill = TRUE
    )
  })

  # Renderlizar los indicadores de rendimiento escolar
  output$indicators <- renderInfoBox({
    data$indicadores <- get_indicators(data$id_user)
    infoBox(
      title = NULL,
      value = fluidRow(
        column(
          width = 6, 
          descriptionBlock(
            number = "18%",
            numberColor = "success",
            numberIcon = icon("caret-up"),
            header = formatC(data$indicadores$prom_general, digits = 2, format = "f"),
            text = "Promedio general",
            rightBorder = TRUE,
            marginBottom = FALSE
          ),
        ),

        column(
          width = 6, 
          descriptionBlock(
            number = "18%",
            numberColor = "danger",
            numberIcon = icon("caret-down"),
            header = formatC(data$indicadores$prom_per_prev, digits = 2, format = "f"),
            text = "Periodo previo",
            rightBorder = FALSE,
            marginBottom = FALSE
          )
        )
      ),

      subtitle = NULL,
      icon = icon("chart-line"),
      color = "warning",
      elevation = 2,
      iconElevation = 0,
      gradient = FALSE,
      fill = FALSE
    )
  })

  # Renderizar grafica de promedio escolar por periodos
  output$average_grades <- renderUI({
    data$promedios <- get_average_grades(data$id_user) %>% arrange(period)
    # hchart(promedios, "column", hcaes(x = period, y = average_grades))
    hchart(data$promedios, "areaspline", hcaes(x = period, y = average_grades)) %>% 
    hc_xAxis(title = list(text = "Periodo escolar")) %>% 
    hc_yAxis(title = list(text = "Promedio general"))
  })

  # Renderizar el velocímetro del tiempo de permanencia escolar
  output$dwell_time <- renderUI({
    data$permanencia <- get_dwell_time(data$id_user)
    col_stops <- data.frame(
      q = c(0.15, 0.4, .8),
      c = c('#55BF3B', '#DDDF0D', '#DF5353'),
      stringsAsFactors = FALSE
    )

    highchart() %>%
      hc_chart(type = "solidgauge") %>%
      hc_pane(
        startAngle = -90,
        endAngle = 90,
        background = list(
          outerRadius = '100%',
          innerRadius = '60%',
          shape = "arc"
        )
      ) %>%
      hc_tooltip(enabled = FALSE) %>% 
      hc_yAxis(
        stops = list_parse2(col_stops),
        lineWidth = 0,
        minorTickWidth = 0,
        tickAmount = 2,
        min = 0,
        max = 8,
        labels = list(y = 26, style = list(fontSize = "22px"))
      ) %>%
      hc_add_series(
        data = data$permanencia,
        dataLabels = list(
          y = -50,
          borderWidth = 0,
          useHTML = TRUE,
          style = list(fontSize = "40px")
        )
      ) %>% 
      hc_size(height = 300)
  })

  # Renderizar grafica de pagos acumulados
  output$payments_chart <- renderUI({
    # Obtener los datos de los pagos
    data$pagos <- get_payments(data$id_user)
    pagos <- data$pagos[, c("expiration", "amount")] %>% arrange(expiration)
    # hchart(pagos, "areaspline", hcaes(x = expiration, y = amount))

    pagos["cumulative"] <- cumsum(pagos[,"amount"])
    hchart(pagos, "column", hcaes(x = expiration, y = cumulative))
  })
  
  # Renderizar tabla de historico de pagos
  output$payments_table <- renderDatagrid({
    datos <- data$pagos %>% select(period, date, expiration, description, amount, status) %>% rename("Periodo" = period, "Fecha" = date, "Expiración" = expiration, "Concepto" = description, "Saldo" = amount, "Estado" = status)
    datagrid(datos,  colwidths = "guess", sortable = FALSE, theme = "striped")
  })

  # Renderizar la fecha de actualización de los pagos
  output$payments_chart_last_updated <- renderUI({
    p(paste0("Última actualización: ", get_payments_last_updated(data$id_user)), class="text-muted my-0")
  })

  output$payments_table_last_updated <- renderUI({
    p(paste0("Última actualización: ", get_payments_last_updated(data$id_user)), class="text-muted my-0")
  })

  # Renderizar menu desplegable para seleccionar boleta calificaciones
  output$grades_dropdown <- renderUI({
    dropdown(
      # h3("Seleccionar boleta"),

      selectInput(
        inputId = "school_period",
        label = "Periodo escolar",
        choices = data$periods
      ),
      
      style = "simple",
      label = "Buscar",
      icon = icon("magnifying-glass"),
      status = "primary",
      width = "300px",
      animate = animateOptions(
        enter = animations$fading_entrances$fadeIn,
        exit = animations$fading_exits$fadeOut
      )
    )
  })

  output$grades_table <- renderUI({
    # Obtenemos el resultado de la consulta a la API
    data$calificaciones <- get_grades_per_period(data$id_user, input$school_period)

    table_data <- data$calificaciones %>%
    select(!c("number", "type", "section", "modality")) %>%
    rename("Clave" = id_subject, 
    "Profesor" = teacher, 
    "Asignatura" = subject, 
    "1er. parcial" = first_partial, 
    "2do. parcial" = second_partial, 
    "3er. parcial" = third_partial, 
    "Promedio" = average, 
    "Final" = final_grade)

    bs4Table(
      cardWrap = FALSE,
      bordered = FALSE,
      striped = TRUE,
      table_data
    )
  })

  output$grades_last_updated <- renderUI({
    p(paste0("Última actualización: ", get_grades_last_updated(data$id_user)), class = "text-muted my-0")
  })

  # Renderizar el horario escolar del último semestre
  output$school_schedule <- renderUI({
    horario_escolar <- get_student_schedule(data$id_user) 
    horario_escolar <- horario_escolar %>% rename("Clave" = id_subject, "Asignatura" = subject, "Docente" = teacher, "Modalidad" = modality, "Lunes" = monday, "Martes" = tuesday, "Miercoles" = wednesday, "Jueves" = thursday, "Viernes" = friday, "Sabado" = saturday)
    bs4Table(
      cardWrap = FALSE,
      bordered = FALSE,
      striped = TRUE,
      horario_escolar
    )
  })

  # Renderizar la tabla de la oferta academica
  output$tabla <- renderDatagrid({
    data$oferta <- get_academic_offer(data$id_user, "exclusive")
    oferta <- data$oferta %>% select(id_subject, section, modality, subject, teacher, modality, fail_rate, teacher_fail_rate, teacher_subject_fail_rate, monday, tuesday, wednesday, thursday, friday, saturday)

    oferta["fail_rate"] <- formatC(oferta[, "fail_rate"], digits = 2, format = "f")
    oferta["teacher_fail_rate"] <- formatC(oferta[, "teacher_fail_rate"], digits = 2, format = "f")
    oferta["teacher_subject_fail_rate"] <- formatC(oferta[, "teacher_subject_fail_rate"], digits = 2, format = "f")
    oferta <- oferta %>% rename("Clave" = id_subject, "Sección" = section, "Asignatura" = subject, "Docente" = teacher, "Modalidad" = modality, "Por asignatura" = fail_rate, "Por docente" = teacher_fail_rate, "Por docente en asignatura" = teacher_subject_fail_rate, "Lun" = monday, "Mar" = tuesday, "Mié" = wednesday, "Jue" = thursday, "Vie" = friday, "Sáb" = saturday)
    # oferta["Añadir"] <- 1:nrow(oferta)

    datagrid(oferta, colwidths = "guess", sortable = FALSE, pagination = 10, theme = "striped") %>% 
    # grid_row_merge(columns = "Asignatura") %>% 
    grid_columns(columns = c("Asignatura", "Por asignatura", "Por docente", "Por docente en asignatura"), sortable = TRUE) %>%
    grid_selection_row(inputId = "selecciones", type = "checkbox", return = "data") %>% 
    grid_complex_header("Tasa de reprobación" = c("Por asignatura", "Por docente", "Por docente en asignatura")) %>% 
    grid_colorbar(column = "Por asignatura", color = "#000000", from = c(0, 100), suffix = "%", bar_bg = "#9BCCFF", height = "20px") %>% 
    grid_colorbar(column = "Por docente", color = "#000000", from = c(0, 100), suffix = "%", bar_bg = "#9CFFAE", height = "20px") %>% 
    grid_colorbar(column = "Por docente en asignatura", color = "#000000", from = c(0, 100), suffix = "%", bar_bg = "#FF9C9C", height = "20px")
    # grid_col_button(column = "Añadir", inputId  = "index", label = "Agregar", icon("check"), status = "success")

  })

  # Cuando el dataframe de selecciones se envía a validación
  observeEvent(input$launch, {
    # Almacenamos la tabla con las selecciones en una nueva variable
    selecciones <- input$selecciones
    # Cambiamos los nombres de las columnas de interés
    names(selecciones) <- c("id_subject", "section", "Asignatura", "Docente", "Modalidad", "Por asignatura", "Por docente", "Por docente y asignatura", "Lun", "Mar", "Mié", "Jue", "Vie", "Sáb")
    print(selecciones[, c("section", "id_subject")])
    # Se envía la sección y clave de la asignatura al endpoint del modelo
    data$prediccion <- model(data$id_user, selecciones[, c("section", "id_subject")])    
    # Mostramos los resultados de la predicción en la consola
    cat("Prediccion del modelo: ")
    print(data$prediccion)
  })


  observeEvent(data$prediccion, {
    if(!is.null(data$prediccion)) { 
      if(data$prediccion == 1) {
        data$prediccion_mensaje <- "selección recomendada"
        data$prediccion_estatus <- "lime"
      } else {
        data$prediccion_mensaje <- "selección no recomendada"
        data$prediccion_estatus <- "danger"
      }
    } else {
      data$prediccion_estatus <- "primary"
    }
  })

  # Renderizar la sección de alertas
  output$alertas <- renderUI({
    # Si las selecciones contienen información
    if(!is.null(input$selecciones)) {
      # Se define funcion para los infobox de alerta
      alerta <- function(title = NULL, value = NULL, elevation = 2, width = 3, subtitle = NULL, icon = NULL, color = "primary", fill = FALSE) {
        infoBox(title = title, value = value, elevation = elevation, width = width, subtitle = subtitle, icon = icon, color = color, fill = fill)
      }

      # Se define funcion para los callout de alerta
      aviso <- function(title = "", status = "info", width = 6, elevation = NULL, content = "") {
        callout(title = title, status = status, width = width, elevation = elevation, content)
      }

      fluidRow(
        # Renderizar aviso de las instrucciones
        aviso(title = p("Instrucciones", class = "lead fw-bold"), status = "danger", width = 4, elevation = 2, 
        HTML("Visualiza tu selección académica preliminar y las tasas de reprobación. Se recomienda validar para determinar 
        si la carga podría aprobarse o reprobarse.")),

        # Renderizar el infobox para validar la carga curricular
        alerta(
          title = p("Valida tu selección curricular", class="mb-0 lead text-center"),
          icon = icon("microchip"),
          width = 4,
          color = ifelse(is.null(data$prediccion_estatus), "primary", data$prediccion_estatus),
          subtitle = div(
          
          p(paste0("Predicción: ", data$prediccion_mensaje)),

          bs4Dash::actionButton(
            inputId = "launch", 
            label = "EJECUTAR", 
            outline = TRUE, 
            status = "info", 
            size = "sm", 
            width = "200px", 
            flat = TRUE
          ),
          
          class = "mt-0 mx-auto")
        ),
        
        alerta(title = p("Recomendaciones", class = "lead text-center"), color = "warning", subtitle = NULL, width = 4, icon = icon("exclamation-triangle"))
      )
    }
  })

  # Renderizar la tabla con las asignaturas seleccionadas en la oferta académica
  output$selecciones <- renderUI({
    # Si las selecciones no son nulas
    if(!is.null(input$selecciones)){
      selecciones <- input$selecciones
      # Mostrar la tabla de selecciones
      # Del dataframe de las selecciones de asignatura separamos las variables de interés
      selecciones <- selecciones %>% select(Asignatura, Docente, Lun, Mar, Mié, Jue, Vie, Sáb)
      # Mostramos la tabla en un datagrid
      datagrid(selecciones, colwidths = "guess", sortable = FALSE, width = "100%", height = "500px", theme = "striped")
    } else {
      # Si las selecciones de asignaturas son nulas, mostramos mensaje al usuario
      p("Opps... Parece que no has elegido asignaturas en la oferta", class = "lead mx-auto")
    }
  })

  # Renderizar las gráficas con las tasas de reprobación
  output$tasa_reprobacion <- renderUI({
    if(!is.null(input$selecciones)){
      selecciones <- input$selecciones
      cat("selecciones grafica")
      print(colnames(selecciones))

      names(selecciones) <- c("Clave", "Sección", "Modalidad", "Asignatura", "Docente", "Por asignatura", "Por docente", "Por docente y asignatura", "Lun", "Mar", "Mié", "Jue", "Vie", "Sáb")
      selecciones["Por asignatura"] <- as.numeric(selecciones[, "Por asignatura"])
      selecciones["Por docente"] <- as.numeric(selecciones[,  "Por docente"])
      selecciones["Por docente y asignatura"] <- as.numeric(selecciones[, "Por docente y asignatura"])

      pivote <- selecciones[, c("Asignatura", "Por asignatura", "Por docente", "Por docente y asignatura")] %>% pivot_longer(!Asignatura, names_to = "grupo", values_to = "Tasa de reprobación")

      hchart(pivote, "column", hcaes(x = `Asignatura`, y = `Tasa de reprobación`, group = `grupo`))
    } else {
      p("Tasas de reprobación no disponibles", class = "lead mx-auto")
    }
  })

  output$oferta_automatizada <- renderUI({
    r <- get_recommendation(data$id_user, 0)$draft
    r <- r %>% select(id_subject, section, teacher, subject, monday, tuesday, wednesday, thursday, friday, saturday)
    colnames(r) <- c("Clave", "Sección", "Docente", "Asignatura", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado")
    datagrid(r, colwidths = "guess", theme = "striped", width = "100%", height = "500px")
  })


  observeEvent(input$index, {
    print(input$index)

    data$selecciones <- c(data$selecciones, as.numeric(input$index))
    cat("Selecciones: ")
    print(data$selecciones)

    # Guardamos el nombre de la asignatura
    data$deleted_subject <- data$oferta[as.numeric(input$index), "Asignatura"]
    
    # Eliminamos la seleccion por numero de fila
    grid_proxy_delete_row("tabla", input$index)

    print(data$oferta)

    same_subjects <- data$oferta %>% filter("Asignatura"  == data$deleted_subject)
    counts <- nrow(same_subjects)
    cat("counts: ")
    print(counts)
  })

  # Renderizar el dropdown de las prácticas profesionales
  output$practices_dropdown <- renderUI({
    data$practices_periods <- get_practices_offer_periods()
    div(
      dropdown(
        # h3("Seleccionar boleta"),

        selectInput(
          inputId = "practice_period",
          label = "Periodo de prácticas",
          choices = data$practices_periods["period"]
        ),
        
        style = "simple",
        label = "Buscar",
        icon = icon("magnifying-glass"),
        status = "primary",
        width = "300px",
        animate = animateOptions(
          enter = animations$fading_entrances$fadeIn,
          exit = animations$fading_exits$fadeOut
        )
      ), 

      dropdown(
        # h3("Seleccionar boleta"),

        selectInput(
          inputId = "practice_subject",
          label = "Asignatura de prácticas",
          choices = data$practices_periods[data$practices_periods["id_offer"] == input$practice_period]
        ),
        
        style = "simple",
        label = "Buscar",
        icon = icon("magnifying-glass"),
        status = "primary",
        width = "300px",
        animate = animateOptions(
          enter = animations$fading_entrances$fadeIn,
          exit = animations$fading_exits$fadeOut
        )
      )
    )
  })

  # Renderizar la oferta de prácticas profesionales
  output$professional_practices <- renderDatagrid({
    data$professional_practices <- get_practices_offer_per_period(input$practice_period)
    datagrid()
  })

  # Renderizar la oferta de servicio social
  output$social_service <- renderDatagrid({
    data$social_service <- get_social_service_offer()

    social_service <- data$social_service %>% rename("Proyecto" = title, "Organización" = organization, "Asesor" = assessor, "Descripción" = description, "Espacios" = spaces)

    datagrid(social_service[, c("Proyecto", "Organización", "Asesor", "Descripción", "Espacios")], colwidths = "fit", sortable = FALSE, theme = "striped", pagination = 5)
  })

  # Renderizar la última actualización de la oferta académica
  output$academic_offer_last_updated <- renderUI({
    p(paste0("Última actualización: ", get_academic_offer_last_updated(data$user_data$career$study_plan)), class = "text-muted my-0")
  })

  # Renderizar calendario escolar
  output$school_calendar <- renderCalendar({
    data_calendar <- read.csv("calendario.csv")

    calendar(data_calendar, navigation = TRUE, width = "80%",height = "50%") %>%
      cal_props(
        list(
          id = 1,
          color = "white",
          bgColor = "#45AEFE",
          borderColor = "#45AEFE"
        ),
        list(
          id = 2,
          color = "white",
          bgColor = "#CD37B5",
          borderColor = "#CD37B5"
        ),
        list(
          id = 3,
          color = "white",
          bgColor = "#D51872",
          borderColor = "#D51872"
        ),
        list(
          id = 4,
          color = "white",
          bgColor = "#37578F",
          borderColor = "#37578F"
        ),
        list(
          id = 5,
          color = "white",
          bgColor = "#0ECD62",
          borderColor = "#0ECD62"
        ),
        list(
          id = 6,
          color = "white",
          bgColor = "#ABD228",
          borderColor = "#ABD228"
        ),
        list(
          id = 7,
          color = "white",
          bgColor = "#2C5904",
          borderColor = "#2C5904"
        ),
        list(
          id = 8,
          color = "white",
          bgColor = "#6C549B",
          borderColor = "#6C549B"
        ),
        list(
          id = 9,
          color = "white",
          bgColor = "#E11260",
          borderColor = "#E11260"
        ),
        list(
          id = 10,
          color = "white",
          bgColor = "#AA0069",
          borderColor = "#AA0069"
        )
      )
  })

  # Renderizar la información del usuario
  output$user_information <- renderUI({

    fluidRow(
      column(
        width = 8,
        class = "mx-auto mt-3",

        userBox(
          title = userDescription(
            title = paste(data$user_data$username, data$user_data$first_lastname, data$user_data$second_lastname),
            subtitle = data$user_data$career$name,
            image = data$user_data$profile_picture,
            backgroundImage = "https://cdn.statically.io/img/wallpaperaccess.com/full/1119564.jpg"
          ),
          
          width = 12,
          status = "olive",
          collapsible = FALSE,
          closable = FALSE,
          maximizable = FALSE,
          
          div(
            class = "pt-5 px-2 pb-0 mx-auto",
            tabBox(
              id = "tabcard",
              title = NULL,
              width = 12,
              collapsible = FALSE,
              closable = FALSE,
              maximizable = FALSE,
              # icon = icon("list-alt"),
              elevation = 0,
              side = "left",
              footer = NULL,
              tabPanel(
                title = "Mis datos", 
                htmlTemplate(
                  "mis_datos.html",
                  username = str_c("'", data$user_data$username, " ", data$user_data$first_lastname, " ", data$user_data$second_lastname, "'"),
                  id_user = str_c("'", data$user_data$id_user, "'"),
                  curp = str_c("'", data$user_data$curp, "'"),
                  rfc = str_c("'", data$user_data$rfc, "'"),
                  nationality = str_c("'", data$user_data$nationality, "'"),
                  nss = str_c("'", data$user_data$nss, "'"),
                  personal_email = str_c("'", data$user_data$personal_email, "'"),
                  personal_phone = str_c("'", data$user_data$personal_phone, "'"),
                  home_phone = str_c("'", data$user_data$home_phone, "'"),
                  marital_status = str_c("'", data$user_data$marital_status, "'"),
                  personal_address = str_c("'", data$user_data$personal_address, "'"),
                  birthplace = str_c("'", data$user_data$birthplace$city, ", ", data$user_data$birthplace$state, ", ", data$user_data$birthplace$country, "'")
                )
              ),

              tabPanel(
                title = "Perfil", 
                htmlTemplate("perfil.html")
              ),

              tabPanel(
                title = "Familiares", 
                htmlTemplate(
                  "familiares.html",
                  parent_1 = str_c("'", data$user_data$parents$father_fullname, "'"),
                  parent_2 = str_c("'", data$user_data$parents$mother_fullname, "'"),
                  parents_marital_status = str_c("'", data$user_data$parents$parents_marital_status, "'")
                )
              ),

              tabPanel(
                title = "Trabajo", 
                htmlTemplate(
                  "trabajo.html",
                  company = str_c("'", data$user_data$job$name, "'"),
                  working_hours = str_c("'", "", "'"),
                  working_schedule = str_c("'", "", "'"),
                  work_address = str_c("'", data$user_data$job$address, "'"),
                  work_phone = str_c("'", data$user_data$job$phone, "'"),
                )
              ),
              
              tabPanel(
                title = "Bachillerato",
                htmlTemplate(
                  "bachillerato.html",
                  highschool = str_c("'", data$user_data$highschool$school, "'"),
                  campus = str_c("'", data$user_data$highschool$campus, "'"),
                  location = str_c("'", data$user_data$highschool$city, ", ", data$user_data$highschool$state, ", ", data$user_data$highschool$country, "'"),
                  school_system = data$user_data$highschool$school_system
                )
              )
            )
          ),

          footer = p(
              class = "text-muted",
              paste0("Última actualización: ", get_user_last_updated(data$id_user))
            )
        ) 

      )

    )
  })

}

options(shiny.port = 5000)
options(shiny.autoreloader = TRUE)
shinyApp(ui, server)
