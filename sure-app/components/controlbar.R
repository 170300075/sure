# The Dashboard Controlbar
controlbar <- dashboardControlbar(
    id = "controlbar",
    skin = "dark",
    icon = icon("circle-half-stroke"),
    collapsed = TRUE,
    overlay = TRUE,
    div(
        class = "p-4",
        skinSelector()
    )
)