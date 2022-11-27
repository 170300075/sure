my_packages <- c("shiny", "bs4Dash", "sortable", "DBI", "devtools",
              "RMariaDB", "dplyr", "data.table", "DiagrammeR",
              "reticulate", "shinyWidgets", "highcharter", "plotly",
              "toastui", "DT", "telegram.bot", "mapboxer", "mongolite") 


# Install required packages
lapply(my_packages, install.packages, character = TRUE)
devtools::install_github("colearendt/shinycookie")
lapply(my_packages, require, character = TRUE)