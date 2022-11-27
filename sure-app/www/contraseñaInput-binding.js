var contraseñaInputBinding = new Shiny.InputBinding();

$.extend(contraseñaInputBinding, {

    find: function(scope){
        return $(scope).find('input[type="password"]');
    },

    getId: function(el){
        return el.id;
    },

    getValue: function(el){
        return el.value;
    },

    setValue: function(el, value){
        el.value = value;
    },

    subscribe: function(el, callback){
        $(el).on("keyup.contraseñaInputBinding input.contraseñaInputBinding", function(event) {
            callback(true);
        });

        $(el).on("change.contraseñaInputBinding", function(event) {
            callback(false);
        });
    },

    unsubscribe: function(el){
        $(el).off(".contraseñaInputBinding");
    },

    receiveMessage: function(el, data){
        if(data.hasOwnProperty("value"))
            this.setValue(el, data.value);

        if(data.hasOwnProperty("label"))
            $(el).parent().find('label[for="' + $escape(el.id) + '"]').text(data.label);

        $(el).trigger("change");
    },

    getState: function(el) {
        return {
            label: $(el).parent().find('label[for="' + $escape(el.id) + '"]').text(), value: el.value
        };
    },

    getRatePolicy: function() {
        return{
            policy: "debounce",
            delay: 500
        };
    }
});


Shiny.InputBindings.register(contraseñaInputBinding, "shiny.contraseñaInput")