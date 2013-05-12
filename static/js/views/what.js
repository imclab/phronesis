var app = app || {};

app.WhatView = Backbone.View.extend({

    index : undefined,
    highlighedtTrait : undefined,
    cachedTranslate : undefined,
    priorityList : ["firstPriority", "secondPriority", "thirdPriority"],

    initialize : function() {

        var self = this

        if ( !($.isFunction(this.template)) ){

            $.get('/static/js/templates/what.handlebars', function(tmpl){
                self.template = tmpl
                self.render()
            })

        } else {

            console.log("gots the template")

        }

    },

    render : function() {

        var source = $(this.template).html();
        var template = Handlebars.compile( source );
        this.$el.html( template( { "adjectives" : adjectives } ) );

        $('#adjective_container').isotope({
            layoutMode: 'masonryHorizontal',
            masonryHorizontal: {
                rowHeight: 40
            },
            resizesContainer: false,
            gutterWidth: 20
        })

        $('#instructions').removeClass('hidden-top')

        $('.nav-adjective').each(function(i){
            var selector = '#' + $(this).html(),
                accentClass = $(this).html() + "-accent",
                priorityClass = "priority-" + (i + 1) 

            $(selector).parent().addClass('chosen-adj').children().addClass(accentClass + ' ' + priorityClass)
        })

    },

    events : {

        "click .adjective" : "toggleAdjective",
        // "mouseover .chosen-adj" : "showSpecifics",
        "click #adjective_container" : "removeSpecifics",
        "mouseover .adjective-wrap, .more-info" : "showInfo",
        "mouseout .more-info" : "hideInfo",
        "click .more-info" : "expandTrait",
        "dblclick .adjective-wrap" : "contractTrait"

    },

    toggleAdjective : function( ev ){

        var self = this

        if ( $('.chosen-adj').length < 3 ){
            
            console.log("fewer than three")

            if ( $(ev.target).parent().hasClass('chosen-adj') ){

                $(ev.target).parent().removeClass('chosen-adj')
                var adj = $(ev.target).html(),
                    selector = '.' + adj,
                    accentClass = adj + " " + "-accent",
                    newPriority = {}
                
                self.index = $(selector).index()
                newPriority[priorities[self.index]] = undefined
                user.get('adjectives').set(newPriority)
                               

            } else {

                $(ev.target).parent().addClass('chosen-adj')
                var adj = $(ev.target).html(),
                    selector = '.' + adj,
                    newPriority = {}

                self.index = $(selector).index()
                newPriority[priorities[self.index]] = adj
                user.get('adjectives').set( newPriority )

            }

        } else {
            console.log("three or more")
            
            $(ev.target).parent().removeClass('chosen-adj')
            var adj = $(ev.target).html(),
                selector = '.' + adj,
                newPriority = {}
            
            self.index = $(selector).index()
            newPriority[priorities[self.index]] = undefined
            user.get('adjectives').set(newPriority)

        }

    },

    showSpecifics : function( ev ){

        var self = this
        var traits = user.get('traits').toJSON(),
            traitName = $(ev.target).attr('id'),
            specifics

        for ( key in traits ){
            if ( traits[key].attributes !== undefined ){
                traits[key].get('name') === traitName ? specifics = traits[key].get('traitSpecifics') : null
            }
        }

        if ( !($.isFunction(this.specificsTemplate)) ){

            $.get('/static/js/templates/traitSpecificsPopup.handlebars', function(tmpl){
                self.specificsTemplate = tmpl
                self.renderSpecifics( tmpl, specifics, ev.target )
            })

        } else {

            console.log("gots the template")

        }

        this.highlighedtTrait = traitName

    },

    renderSpecifics : function( tmpl, specifics, el ){

        var top = $(el).parent().position().top,
            left = $(el).parent().position().left,
            offset = $(el).parent().width(),
            data = []

        _.each(specifics.models, function(model){
            var heading = model.get('as_heading'),
                trait_specific = model.get('trait_specific'),
                datum = { heading : heading, trait_specific : trait_specific }

            data.push(datum)
        })

        console.log("the outgoing data are", data)

        var source = $(tmpl).html();
        var template = Handlebars.compile( source )

        if ( $('#trait_specifics_container').length === 0 ){
            $('#adjective_container').append( template( { "specifics" : data } ) );
            
            if ( left < 500){ 
                $('#trait_specifics_container').css({ position: 'absolute', top : top, left : (left + offset + 20) })
            } else {
                $('#trait_specifics_container').css({ position: 'absolute', top : top, left : (left - 380) })
            }
        }

    },

    removeSpecifics : function( ev ){
        
        $('#trait_specifics_container').remove()

    },

    showInfo : function( ev ){

        console.log("showing")

        var target = $(ev.target),
            more = target.next()

        more.css({ display : "block"})

    },

    hideInfo : function( ev ){
        
        console.log("hiding")
        $('.more-info').css({ display : "none"})

    },

    expandTrait : function( ev ){    

        console.log("expanding trait")

        var target = $(ev.target).prev(),
            targetParent = target.parent(),
            targetClass = target.attr('class'),
            traitName = target.html(),
            more = target.next(),
            activeTrait

        if ( targetParent.hasClass('chosen-adj') && 
            !(targetParent.hasClass('expanded-trait'))) {

            $('#adjective_container').css({ height : '100%' })
            activeTraitSpecifics = this.returnTraitObject( targetClass )

            this.cachedTranslate = targetParent.css('-webkit-transform')
            console.log("the current translate3d location is", this.cachedTranslate)
            $('#instructions').hide()
            $('.adjective-wrap').not(targetParent).hide()
            targetParent.addClass('expanded-trait').css({ '-webkit-transform' : 'translate3d(0px,0px,0px)'})

        }

    },

    contractTrait : function(){

        var expandedTrait = $('.expanded-trait')
        $('#adjective_container').css({ height : '400px' })
        $('#instructions').show()
        expandedTrait.removeClass('expanded-trait')
                     .css({"-webkit-transform" : this.cachedTranslate})
        $('.adjective-wrap').fadeIn()

    },

    returnTraitObject : function( targetClass ){

        var classes = targetClass.split(" "),
            priorityClass = classes[classes.length - 1],
            priorityIndex = Number(priorityClass.split("-")[1]) - 1,
            priorityString = this.priorityList[priorityIndex],
            priorityObject = user.get('traits').get(priorityString)

        return priorityObject
    },

    highlightTrait : function( ev ){

        console.log("the highlighted trait is", this.highlighedtTrait)

        var accentClass = this.highlighedtTrait + "-accent"
        $(ev.target).addClass(accentClass)

    },

    highlightTrait : function( ev ){

        var accentClass = this.highlighedtTrait + "-accent"
        $(ev.target).removeClass(accentClass)

    },

    toggleTraitSpecific : function( ev ) {

        console.log("the event id is", ev.target)

    }

})