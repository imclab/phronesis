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

        $(ev.target).parent().hasClass('chosen-adj') ? $(ev.target).parent().removeClass('chosen-adj') : 
                                                       $(ev.target).parent().addClass('chosen-adj');

        if ( $('.chosen-adj').length === 3 ){

            $('#adjective_specifics').fadeIn()

            $('.chosen-adj').each(function(i, obj){
                var selector = '#adjective_' + (i + 1),
                    adjective = $(obj).find('.adjective').html()

                $(selector).html(adjective)
            })

            $('#adjective_container').isotope({
                    layoutMode : 'straightDown',
                    filter : '.chosen-adj',
                    columnWidth : 240,
                    gutterWidth : 20
                })

            $('.chosen-adj').each(function(i){
                var newClass = 'chosen-adj-' + i 
                console.log(this)
                $(this).addClass(newClass)
            })

            self.expandChosen()
        
        }

    },

    expandChosen : function(){


        this.$el.undelegate('.adjective-wrap', 'click')
        $('.adjective-wrap').not('.chosen-adj').remove() 
        $('#instructions p').html("These are <span id='three'>big</span> categories. More <span>precisely...</span>")
        // $('.adjective-specifics').eq(0).delay(500).slideDown()
        //unbind adjective choice
        this.toggleSpecifics()

    },

    toggleSpecifics : function(){

        var self = this,
            activeAdj = '.chosen-adj-'+ this.state,
            adjName = $(activeAdj).find('div').html()

        $('.active-adj').removeClass('active-adj')
        $('.chosen-adj').eq(this.state).find('.adjective').addClass('active-adj')

        var specific = new app.AdjectiveSpecifics({ 
            el : $('#adjective_specifics'),
            model : adj[adjName]
        })

        this.state++

        if (this.state === 4){
            setTimeout( self.showTrackers, 500)
        }
    },

    showGrid : function(){
        $('#heading').fadeIn()
        window.location.hash = 'grid'
    },

    showProfile : function(){
        $('#heading').fadeIn()
        window.location.hash = 'profile'
    },

    showTrackers : function(){
        window.location.hash = 'addTrackers'
    }

})