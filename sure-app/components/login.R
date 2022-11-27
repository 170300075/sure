library(shiny)

login <- div(
  id = "login",

  tags$head(
    tags$link(rel="stylesheet", href = "hiddenScrollbar.css"),
    tags$script(src = "showPassword.js"),
    tags$link(rel = "stylesheet", type="text/css", href="matricula-style.css"),
    tags$script(src = "styling.js"),
    # Ya se importan con bslib pero el checkbox no funciona sin estos
    tags$script(src = "bootstrap.bundle.min.js"),
    tags$link(rel = "stylesheet", type="text/css", href="bootstrap.min.css")
  ),

  div(
    class = "bg-light",
    div(
      class = "container",
      div(
        class = "row vh-100 justify-content-center align-items-center",
        div(
          class = "col",
          div(
            class = "card mb-3 border-0 shadow-lg mx-auto",
            style = "max-width: 600px;",
            div(
              class = "row",
              div(
                class = "col-md-4",
                style = "background-image: url('./images/assets/entrada.jpeg'); background-size: cover; background-repeat: no-repeat; background-position: center; background-attachment: scroll;"
              ),
              
              div(
                class = "col-md-8",
                div(
                  class = "card-body",
                  h5(
                    class = "card-title mt-3 mb-4 text-center lead fs-2", # nolint
                    "Bienvenido a ",
                    span(
                      class="fst-italic fw-bold",
                      "SURE"
                    )
                  ),
                  
                  # ID USER
                  tags$div(
                    class = "input-group has-validation px-3 mb-4",
                    matriculaInput(inputId = "id_user", label = "Tu matricula")
                  ),

                  # PASSWORD
                  tags$div(
                    class = "input-group has-validation px-3 mb-4",
                    contraseñaInput(inputId = "password", label = "Contraseña")
                  ),
                    
                  # CHECKBOX
                  div(
                    class = "form-check px-5 mb-4",
                    tags$input(
                      type = "checkbox",
                      class = "form-check-input",
                      id = "exampleCheck1",
                      "onclick"="showPassword()",
                      tags$label(
                        class = "form-check-label user-select-none",
                        `for` = "exampleCheck1",
                        span("Mostrar contraseña", class = "lead fs-6")
                      )
                    )
                  ),
                  
                  # SUBMIT
                  actionButton(
                    inputId = "login",
                    label = "Acceder",
                    class = "btn btn-primary mx-3 mb-3"
                  ),

                  # REGISTER LINK
                  a(href = "#", "Crear una cuenta", 
                    class = "mx-3 mb-3 text-decoration-none text-end", 
                    style = "display: block",
                    `onclick` = "document.cookie='token=register'"
                  )
                )
              )
            )
          )
        )
      )   
    )
  )
)