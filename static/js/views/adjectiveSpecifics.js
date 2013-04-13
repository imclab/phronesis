var app = app || {};

app.AdjectiveSpecifics = Backbone.View.extend({

    state : 1,

    initialize : function() {

        var self = this

        if ( !($.isFunction(this.template)) ){

            $.get('/static/js/templates/adjectiveSpecifics.handlebars', function(tmpl){
                self.template = tmpl
                self.render()
            })

        } else {

            console.log("gots the template")

        }

    },

    render : function() {

        // $.when( $.getJSON(this.model.wiki_url) )
        //  .done(
        //     function(data){
        //         var pageId = Object.keys(data.query.pages)[0],
        //             content = data.query.pages[pageId].revisions[0]
        //         $('#wiki_definition').html(wiky.process(content["*"]))
        //     }
        //  )

        var source = $(this.template).html()
        var template = Handlebars.compile( source );
        this.$el.html( template( this.model ) )

       $('#adjective_specifics').delay(500).css({ 
            "opacity" : 1,
            "z-index" : 2
        })

    },

    events : {
        "click .adjective-attribute" : "advanceAttributes"
    },

    advanceAttributes : function( ev ){

    }

})