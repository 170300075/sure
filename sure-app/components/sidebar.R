library(bs4Dash)

sidebar <- dashboardSidebar(
    skin = "dark",      # Colo de barra lateral
    status = "lime",    # Color de los botones de barra lateral
    elevation = "3",    # Sombra de elevacion del sidebar
    collapsed = FALSE,  # Barra no colapsada al inicio
    expandOnHover = FALSE, # Barra no se expande al pasar mouse

    # Panel de usuario en sidebar
    uiOutput(outputId = "user_panel"),

    # El menu para informacion de la carrera
    sidebarMenu(
        id = "career_menu",
        sidebarHeader("Carrera"),

        # Menu para el progreso personal (mapa curricular)
        menuItem(
            text = "Mi progreso",
            tabName = "progress",
            icon = icon("diagram-successor")
        ),

        # Menú de estadísticas de rendimiento estudiantil
        menuItem(
            text = "Resumen",
            tabName = "overview",
            icon = icon("chart-column"),
            selected = TRUE
        ),

        # Menú de pagos y adeudos
        menuItem(
            text = "Pagos y adeudos",
            tabName = "college_fee",
            icon = icon("dollar-sign")
        )
    ),

    # El menu para la informacion de las asignaturas
    sidebarMenu(
        id = "subjects_menu",
        sidebarHeader("Asignaturas"),

        # Menu para boleta y horario
        menuItem(
            text = "Mi semestre",
            startExpanded = TRUE, 
            tabName = "semester",
            icon = icon("person-chalkboard")
        ),

        # Menu para la oferta de asignaturas y el sistema de recomendacion
        menuItem(
            text = "Crear horario",
            tabName = "subjects",
            icon = icon("hand-pointer"),
            badgeLabel = "NUEVO",
            badgeColor = "danger"
            # selected = TRUE
        ),

        # Menu para la lista de empresas de practicas profesionales
        menuItem(
            text = "Oferta de prácticas",
            tabName = "practices", 
            icon = icon("briefcase")
        ),

        # Menu para la lista de instituciones de servicio social
        menuItem(
            text = "Oferta de servicio",
            tabName = "service",
            icon = icon("people-carry-box")
        )
    ),

    # El menu para secciones adicionales (otros)
    sidebarMenu(
        id = "aditionals",
        sidebarHeader("Adicionales"),

        # Menu para el calendario escolar
        menuItem(
            text = "Calendario escolar",
            tabName = "calendar",
            icon = icon("calendar-day")
        ),
        
        # Menu para la evaluacion al desempeño docente
        menuItem(
            text = "Desempeño docente",
            tabName = "educators",
            icon = icon("chalkboard-user")
        )
    ),

    # El menu para la informacion personal
    sidebarMenu(
        id = "settings",
        sidebarHeader("Información personal"),

        # Menu para visualizar informacion personal
        menuItem(
            text = "Mi cuenta",
            tabName = "config",
            icon = icon("cogs"),
            badgeLabel = "REDISEÑADO",
            badgeColor = "warning"
        )
    )
)