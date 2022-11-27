library(bs4Dash)

# Definir los elementos del navbar
header <- dashboardHeader(
    status = "dark",    # Configurar color de navbar
    border = TRUE,      # Aplicar borde
    fixed = TRUE,        # Fijar navbar

    # Agregar logout de usuario a la derecha del navbar
    rightUi = userOutput("user"),

    # Agregar barra de notificaciones a la izq. del navbar
    leftUi = tagList(
        # Menú de mensajes
        dropdownMenuOutput(outputId = "messageMenu"),
        # Menú de notificaciones
        dropdownMenuOutput(outputId = "notificationMenu"),
        # Menú de tareas
        dropdownMenuOutput(outputId = "taskMenu")
    )
)