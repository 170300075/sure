library(bs4Dash)
library(bslib)

# Ruta base
base_path <- paste0(getwd(), "/components/")
# Importar los componentes
source(paste0(base_path, "header.R"))
source(paste0(base_path, "sidebar.R"))
source(paste0(base_path, "body.R"))
source(paste0(base_path, "footer.R"))
source(paste0(base_path, "controlbar.R"))

# Crear dashboard
dashboard <- dashboardPage(
  header,                   # Header de tablero
  sidebar,                  # Sidebar de tablero
  body,                     # Body de tablero
  footer,                   # Footer de tablero
  controlbar = controlbar   # Barra de control de colores
)


# Aplicar estilos y nombre de pagina
dashboard_page <- bootstrapPage(
  dashboard, 
  title = "My dashboard",
  theme = bslib::bs_theme(
    version = 5
  )
)
