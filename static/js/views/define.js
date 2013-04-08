var app = app || {};

app.DefineView = Backbone.View.extend({
    state : 0,

    initialize : function() {

        var self = this

        if ( !($.isFunction(this.template)) ){

            $.get('/static/js/templates/defineView.handlebars', function(tmpl){
                self.template = tmpl
                self.render()
                self.transitionIn()
            })

        } else {

            self.render()

        }

    },

    render : function() {

        var source = $(this.template).html()
        var template = Handlebars.compile( source );
        this.$el.html( template( { "adjectives" : adjectives } ) )

        $('#adjective_container').isotope({
            // itemSelector : '.adjective-wrap',
            layoutMode: 'masonryHorizontal',
            masonryHorizontal: {
                rowHeight: 40
            },
            resizesContainer: false,
            gutterWidth: 20
        })

    },

    transitionIn : function(){

        $('#instructions').removeClass('hidden-top')
        $('.adjective-wrap').removeClass('hidden-left')
        $('.top-adj').removeClass('hidden-left')

    },

    events : {

        "click .adjective-wrap" : "toggleAdjective",
        "click .adjective-attribute" : "toggleSpecifics"

    },

    toggleAdjective : function(ev){

        var self = this

        $(ev.target).parent().hasClass('chosen-adj') ? $(ev.target).parent().removeClass('chosen-adj') : $(ev.target).parent().addClass('chosen-adj')

        if ( $('.chosen-adj').length === 3 ){

            $('#adjective_container').isotope({
                    layoutMode : 'straightAcross',
                    filter : '.chosen-adj'
                })

            self.expandChosen()
        
        }

    },

    expandChosen : function(){


        this.$el.undelegate('.adjective-wrap', 'click')
        $('.adjective-wrap').not('.chosen-adj').remove() 
        $('#instructions p').html("These are <span id='three'>big</span> categories. More <span>precisely...</span>")
        $('.adjective-specifics').eq(0).delay(500).slideDown()
        //unbind adjective choice
    },

    toggleSpecifics : function(){

        var self = this

        var index = $(this).index() + 1
        $('.adjective-specifics')
            .eq(this.state).slideUp()
        $('.adjective-specifics')    
            .eq(this.state+1).slideDown()
        this.state++

        if (this.state === 3){
            setTimeout( self.showGrid, 500)
        }
    },

    showGrid : function(){
        window.location.hash = 'grid'
    }

})