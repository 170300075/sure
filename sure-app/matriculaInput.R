matriculaInput <- function(inputId, label, validation = "", value = NULL) {
    tagList(
        shiny::singleton(
            shiny::tags$head(
                shiny::tags$script(src = "matriculaInput-binding.js"),
                # Estas depedencias las importamos directamente desde la pagina
                # shiny::tags$script(src = "bootstrap.bundle.min.js"),
                # shiny::tags$link(rel = "stylesheet", type="text/css", href="matricula-style.css"),
                # shiny::tags$link(rel = "stylesheet", type="text/css", href="bootstrap.min.css")
            )
        ),

        shiny::tags$div(
            class = paste0("form-floating col-12", validation),
            
            shiny::tags$input(id = inputId, type = "number", class = paste0("form-control ", validation), "onKeyPress"="if(this.value.length==9) return false;", placeholder = "Matricula", value = value),
            shiny::tags$label(span(label, class="lead fs-6"), "for" = inputId),

        ), 

        shiny::tags$div(
            class = "invalid-feedback",
            "El usuario no está registrado"
        )
    )
}

updateMatriculaInput <- function(session, inputId, label = NULL, value = NULL) {
    message <- dropNulls(
        list(
            label = label,
            value = value
        )
    )

    session$sendInputMessage(inputId, message)
}

dropNulls <- function(x) {
    x[!vapply(x, is.null, FUN.VALUE=logical(1))]
}
