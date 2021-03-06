 var app = app || {};

 var Meal = Backbone.Model.extend({
        defaults: {
            phro_created_at : undefined,
            username : "pdarche",
            created_at : undefined,
            flkr_ref_info : {
                photo_id : undefined,
                farm : undefined,
                server : undefined,
                secret : undefined
            },
            flkr_dates : {
                taken : undefined,
                last_update : undefined,
                taken_granularity : undefined
            },
            meal_item_name : undefined,
            img_url : undefined,
            meal : undefined,
            venue : undefined,
            venue_category : undefined,
            from_loc : [],
            eaten_loc : undefined,
            unit : undefined,
            calories : undefined,
            calories_from_fat : undefined,
            total_fat : undefined,
            saturated_fat : undefined,
            trans_fat : undefined,
            cholesterol : undefined,
            sodium : undefined,
            total_carbs : undefined,
            dietary_fiber : undefined,
            sugar : undefined,
            protein : undefined,
            vit_a : undefined,
            vit_c : undefined,
            calcium : undefined,
            iron : undefined,
            source : undefined, 
            ingredients : []
        },
        initialize: function(){

            this.on("change", function(model){
                console.log("things have changed")
                model.save()
            })
        }
});

var Meals = Backbone.Collection.extend({
    model: Meal,
    url : '/v1/data/pdarche/body/nutrition?created_at__gte=1359349200'
});


