library(bs4Dash)
library(toastui)

body <- dashboardBody(
    tabItems(
        # Seccion del progreso personal (mapa curricular)
        tabItem(
            tabName = "progress",
            htmlTemplate("breadcrumb.html", link = "Mapa curricular"),
            # h2("Mapa curricular", class = "m-4 mb-5 text-center")
            # uiOutput("curricular_map")
            box(
                title = h5(
                    "Mapa curricular",
                    class = "text-center my-auto"
                ),
                closable = FALSE,
                solidHeader = TRUE,
                collapsible = FALSE,
                width = 12,
                status = "navy",
                footer = p("El mapa curricular depende del programa de estudios", class="text-muted my-0"),
                uiOutput("curricular_map")
            )
        ),
        
        # Seccion de las estadisticas de rendimiento estudiantil
        tabItem(
            tabName = "overview",
            htmlTemplate("breadcrumb.html", link = "Resumen personal"),
            # h2("Resumen personal", class = "m-4 mb-5 text-center"),

            fluidRow(
                infoBoxOutput(outputId = "first_cycle", width = 3),
                infoBoxOutput(outputId = "second_cycle", width = 3),
                infoBoxOutput(outputId = "third_cycle", width = 3),
                infoBoxOutput(outputId = "fourth_cycle", width = 3),
                infoBoxOutput(outputId = "other_subjects", width = 3),
                infoBoxOutput(outputId = "prespeciality", width = 4),
                infoBoxOutput(outputId = "indicators", width = 5)
            ),
                
            fluidRow(
                column(
                    width = 8,
                    height = "400px",
                    box(
                        title = h5(
                            "Promedios por semestre",
                            class = "text-center my-auto"
                        ),
                        width = 12,
                        closable = FALSE,
                        solidHeader = TRUE,
                        collapsible = FALSE,
                        status = "navy",
                        uiOutput("average_grades")
                    )
                ),
                
                br(),

                column(
                    width = 4,
                    height = "200px",
                    box(
                        title = h5(
                            "Años de permanencia",
                            class = "text-center my-auto"
                        ),
                        width = 12,
                        closable = FALSE,
                        solidHeader = TRUE,
                        collapsible = FALSE,
                        status = "navy",
                        uiOutput("dwell_time")
                    )
                )
            )
        ),

        tabItem(
            tabName = "college_fee",
            htmlTemplate("breadcrumb.html", link = "Pagos y adeudos"),
            # h2("Pagos y adeudos", class = "m-4 mb-5 text-center"),

            fluidRow(
                column(
                    width = 6,
                    box(
                        height = "500px",
                        title = h5(
                            "Acumulado de pagos",
                            class = "text-center my-auto"
                        ),
                        closable = FALSE,
                        solidHeader = TRUE,
                        collapsible = FALSE,
                        width = 12,
                        status = "navy",
                        footer = uiOutput("payments_chart_last_updated"),
                        uiOutput("payments_chart")
                    )
                ),

                column(
                    width = 6,
                    box(
                        height = "500px",
                        title = h5(
                            "Tabla de datos",
                            class = "text-center my-auto"
                        ),
                        closable = FALSE,
                        solidHeader = TRUE,
                        collapsible = FALSE,
                        width = 12,
                        status = "navy",
                        footer = uiOutput("payments_table_last_updated"),
                        datagridOutput(outputId = "payments_table", height = "100%")
                    )
                )
            )
        ),

        tabItem(
            tabName = "semester",
            htmlTemplate("breadcrumb.html", link = "Boleta - Horario"),
            # h2("Boleta - Horario", class = "m-4 mb-5 text-center"),
            
            fluidRow(
                column(
                    width = 10,
                    class = "mx-auto",
                    tabBox(
                        id = "semester_card",
                        selected = NULL,
                        width = 12,
                        # height = "500px",
                        side = "left",
                        type = "tabs",
                        footer = uiOutput("grades_last_updated"),# p("Last updated: dd/mm/yyyy", class="text-muted my-0"),
                        status = "navy",
                        solidHeader = TRUE,
                        collapsible = FALSE,
                        closable = FALSE,
                        maximizable = TRUE,
                        icon = icon("circle-info"),
                        # elevation = 2,
                        headerBorder = TRUE,
                        # style = "overflow-x: scroll;",

                        tabPanel(
                            title = "Calificaciones", 
                            uiOutput("grades_dropdown"),
                            
                            br(),

                            uiOutput("grades_table")
                        ),

                        tabPanel(
                            title = "Horario escolar",
                            uiOutput("school_schedule")
                        )
                    )
                )
            )
        ),

        tabItem(
            tabName = "subjects",
            htmlTemplate("breadcrumb.html", link = "Crear un horario / Oferta académica"),
            # h2("Crear un horario / Oferta académica", class = "m-4 mb-5 text-center")

            tabBox(
                id = "oferta_academica",
                title = "Sistema de recomendación",
                width = 12,
                side = "right", 
                selected = "Oferta académica",
                status = "gray-dark",
                label = boxLabel("POWERED BY AI", status = "lime", tooltip = "Model based on Deep Learning algorithm"),
                solidHeader = TRUE,
                collapsible = FALSE,
                maximizable = TRUE,
                type = "tabs",
                footer = uiOutput("academic_offer_last_updated"),
                
                # Tabla de datos interactiva
                tabPanel(
                    title = "Oferta académica",
                    width = 12,
                    datagridOutput("tabla", width = "100%", height = "100%")
                ),
                
                # Selecciones y gráfica de tasa de reprobación
                tabPanel(
                    title = "Selecciones",
                    width = 12,
                    fluidRow(
                        width = 12,
                        uiOutput("alertas")
                    ),

                    fluidRow(
                        column(
                            width = 8, 
                            uiOutput("selecciones")
                        ),

                        column(
                            width = 4, 
                            uiOutput("tasa_reprobacion")
                        )
                    )
                ),

                tabPanel(
                    title = "Automatizado",
                    width = 12, 
                    uiOutput("oferta_automatizada")
                )

            )
        ), 

        tabItem(
            tabName = "practices",
            htmlTemplate("breadcrumb.html", link = "Lista de empresa para prácticas"),
            # h2("Lista de empresas para practicas", class = "m-4 mb-5 text-center")
            box(
                title = h5(
                            "Prácticas profesionales",
                            class = "text-center my-auto"
                ),
                width = 12,
                closable = FALSE,
                solidHeader = TRUE,
                collapsible = FALSE,
                status = "navy",
                uiOutput("practices_dropdown"),
                datagridOutput(outputId = "professional_practices", height = "100%")
            )
            
        ),

        tabItem(
            tabName = "service",
            htmlTemplate("breadcrumb.html", link = "Lista de instituciones para servicio social"),
            # h2("Lista de instituciones para servicio social", class = "m-4 mb-5 text-center")
            box(
                title = h5(
                            "Servicio social",
                            class = "text-center my-auto"
                ),
                width = 12,
                closable = FALSE,
                solidHeader = TRUE,
                collapsible = FALSE,
                status = "navy",
                datagridOutput(outputId = "social_service", width = "100%", height = "100%")
            )
        ),

        tabItem(
            tabName = "calendar",
            htmlTemplate("breadcrumb.html", link = paste0("Calendario escolar - ", format(Sys.Date(), "%Y"))),
            # h2("Calendario escolar", class = "m-4 mb-5 text-center")
            calendarOutput(outputId = "school_calendar", width = "100%", height = "100%")
        ),

        tabItem(
            tabName = "educators",
            htmlTemplate("breadcrumb.html", link = "Evaluación al desempeño docente"),
            # h2("Evaluación al desempeño docente", class = "m-4 mb-5 text-center")
            # uiOutput(outputId = "teachers_forms")
            div(
                class = "mt-5",
                HTML('<center><img src="images/assets/in_progress.png" width="400" height="341"/></center>')
            )

        ),

        tabItem(
            tabName = "config",
            htmlTemplate("breadcrumb.html", link = "Información personal"),
            # h2("Información personal", class = "m-4 mb-5 text-center")
            uiOutput(outputId = "user_information"), class = "mx-auto"
        )
    )
)