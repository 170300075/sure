const observer = new MutationObserver(function() {
    if(document.querySelector(".fa-th")){
        controlbar_icon = document.querySelector(".fa-th")
        controlbar_icon.className = "fa fa-list"
        console.log("Controlbar icon changed!")
    }
  })
  
const target = document.querySelector("body");
const config = {childList : true};

observer.observe(target, config)