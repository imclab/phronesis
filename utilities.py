# -*- coding: utf8 -*- 
# from types import ModuleType
import os
import sys
import types
from itertools import groupby
import time

from mongoengine import *
import mongoengine
import simplejson
from bson.objectid import ObjectId

#for scraping, eg chipotle
import urllib2
from BeautifulSoup import BeautifulSoup

from xml.dom.minidom import parse, parseString
import models.mypyramid as pyramid
import models.nutrition as nutrition
import models.flickr as flickr

def encode_model(obj):
    if isinstance(obj, (mongoengine.Document, mongoengine.EmbeddedDocument)):
        out = dict(obj._data)
        for k,v in out.items():
            if isinstance(v, ObjectId):
                out[k] = str(v)
    elif isinstance(obj, mongoengine.queryset.QuerySet):
        out = list(obj)
    elif isinstance(obj, types.ModuleType):
        out = None
    elif isinstance(obj, groupby):
        out = [ (g,list(l)) for g,l in obj ]
    elif isinstance(obj, (list,dict)):
        out = obj
    else:
        raise TypeError, "Could not JSON-encode type '%s': %s" % (type(obj), str(obj))
    return out
    """
    and use this line " result = simplejson.dumps(base, default=encode_model)   "
    Example
    """

def parse_pyramid():
    connect('local_db')

    doc = parse('data/MyfoodapediaData/Food_Display_Table.xml')
    foods = doc.getElementsByTagName('Food_Display_Row')

    for food in foods:
        new_food = pyramid.MyPyramidReferenceInfo(
                food_code = food.getElementsByTagName('Food_Code')[0].firstChild.nodeValue,
                display_name = food.getElementsByTagName('Display_Name')[0].firstChild.nodeValue,
                portion_default = float(food.getElementsByTagName('Portion_Default')[0].firstChild.nodeValue),
                portion_amount = float(food.getElementsByTagName('Portion_Amount')[0].firstChild.nodeValue),
                portion_display_name = food.getElementsByTagName('Portion_Display_Name')[0].firstChild.nodeValue,
                factor = float(food.getElementsByTagName('Factor')[0].firstChild.nodeValue) if len(food.getElementsByTagName('Factor')) > 0 else None,
                increment = float(food.getElementsByTagName('Increment')[0].firstChild.nodeValue),
                multiplier = float(food.getElementsByTagName('Multiplier')[0].firstChild.nodeValue),
                grains = float(food.getElementsByTagName('Grains')[0].firstChild.nodeValue),
                whole_grains = float(food.getElementsByTagName('Whole_Grains')[0].firstChild.nodeValue),
                vegetables = float(food.getElementsByTagName('Vegetables')[0].firstChild.nodeValue),
                orange_vegetables = float(food.getElementsByTagName('Orange_Vegetables')[0].firstChild.nodeValue),
                drkgreen_vegetables = float(food.getElementsByTagName('Drkgreen_Vegetables')[0].firstChild.nodeValue),
                starchy_vegetabels = float(food.getElementsByTagName('Starchy_vegetables')[0].firstChild.nodeValue),
                other_vegetables = float(food.getElementsByTagName('Other_Vegetables')[0].firstChild.nodeValue),
                fruits = float(food.getElementsByTagName('Fruits')[0].firstChild.nodeValue),
                milk = float(food.getElementsByTagName('Milk')[0].firstChild.nodeValue),
                meats = float(food.getElementsByTagName('Meats')[0].firstChild.nodeValue),
                soy = float(food.getElementsByTagName('Soy')[0].firstChild.nodeValue),
                drybeans_peas = float(food.getElementsByTagName('Drybeans_Peas')[0].firstChild.nodeValue),
                oils = float(food.getElementsByTagName('Oils')[0].firstChild.nodeValue),
                solid_fats = float(food.getElementsByTagName('Solid_Fats')[0].firstChild.nodeValue),
                added_sugars = float(food.getElementsByTagName('Added_Sugars')[0].firstChild.nodeValue),
                alcohol = float(food.getElementsByTagName('Alcohol')[0].firstChild.nodeValue),
                calories = float(food.getElementsByTagName('Calories')[0].firstChild.nodeValue),
                saturated_fats = float(food.getElementsByTagName('Saturated_Fats')[0].firstChild.nodeValue)
            )
        
        if new_food.save():
            print "food saved"
        else:
            print "didn't save"


def remove_records():
    connect('local_db')

    foods = pyramid.MyPyramidReferenceInfo.objects()
    foods.delete()

    print len(foods)


class Parse_SR25():
    connect('local_db')
    def parse_food_desc(self):
        numpass = 0
        f = open('data/sr25/FOOD_DES.txt')
        lines = f.readlines()
        for line in lines:
            food = line.replace('~', '').strip().split('^')
            des = nutrition.SR25FoodDescription(
                    NBD_No = food[0].decode('cp1252', 'ignore'),
                    FdGrp_Cd = food[1].decode('cp1252', 'ignore'),
                    Long_Desc = food[2].decode('cp1252', 'ignore'),
                    Shrt_Desc = food[3].decode('cp1252', 'ignore'),
                    ComName = food[4].decode('cp1252', 'ignore') if len(food[4]) > 0 else None,
                    ManufacName = food[5].decode('cp1252', 'ignore') if len(food[5]) > 0 else None,
                    Survey = food[6].decode('cp1252', 'ignore') if len(food[6]) > 0 else None,
                    Ref_desc = food[7].decode('cp1252', 'ignore') if len(food[7]) > 0 else None,
                    Refuse = float(food[8]) if len(food[8]) > 0 else None,
                    SciName = food[9].decode('cp1252', 'ignore') if len(food[9]) > 0 else None,
                    N_Factor = float(food[10]) if len(food[10]) > 0 else None,
                    Pro_Factor = float(food[11]) if len(food[11]) > 0 else None,
                    Fat_Factor = float(food[12]) if len(food[12]) > 0 else None,
                    CHO_Factor = float(food[13]) if len(food[13]) > 0 else None
                )

            try:
                des.save()
                print "description saved"
            except:
                numpass += 1
                print numpass
                pass


    def parse_nutrient_data(self):
        f = open('data/sr25/NUT_DATA.txt')
        lines = f.readlines()
        for line in lines:
            food = line.replace('~', '').strip().split('^')
            nut = nutrition.SR25NutrientData(
                    NDB_No = food[0].decode('cp1252', 'ignore'),
                    Nutr_No = food[1].decode('cp1252', 'ignore'),
                    Nutr_Val = float(food[2]),
                    Num_Data_Pts = float(food[3]),
                    Std_Error = float(food[4]) if len(food[4]) > 0 else None,
                    Src_Cd = food[5].decode('cp1252', 'ignore'),
                    Deriv_Cd = food[6].decode('cp1252', 'ignore') if len(food[6]) > 0 else None,
                    Ref_NDB_No = food[7].decode('cp1252', 'ignore') if len(food[7]) > 0 else None,
                    Add_Nutr_Mark = food[8].decode('cp1252', 'ignore') if len(food[8]) > 0 else None,
                    Num_Studies = food[9].decode('cp1252', 'ignore') if len(food[9]) > 0 else None,
                    Min = float(food[10]) if len(food[10]) > 0 else None,
                    Max = float(food[11]) if len(food[11]) > 0 else None,
                    DF = food[12].decode('cp1252', 'ignore') if len(food[12]) > 0 else None,
                    Low_EB = float(food[13]) if len(food[13]) > 0 else None,
                    Up_EB = float(food[14]) if len(food[14]) > 0 else None,
                    Stat_cmt = food[15].decode('cp1252', 'ignore') if len(food[15]) > 0 else None,
                    AddMod_Date = food[16].decode('cp1252', 'ignore') if len(food[16]) > 0 else None,
                    CC = food[17].decode('cp1252', 'ignore') if len(food[17]) > 0 else None
                )

            nut.save()
        print "done"

    def parse_weight(self):
        f = open('data/sr25/WEIGHT.txt')
        lines = f.readlines()
        for line in lines:
            food = line.replace('~', '').strip().split('^')
            weight = nutrition.SR25Weight(
                    NDB_No = food[0].decode('cp1252', 'ignore'),
                    Seq = food[1].decode('cp1252', 'ignore'),
                    Amount = float(food[2]),
                    Msre_Desc = food[3].decode('cp1252', 'ignore'),
                    Gm_Wgt = float(food[4]),
                    Num_Data_Pts = food[5].decode('cp1252', 'ignore') if len(food[5]) > 0 else None, 
                    Std_Dev = float(food[6]) if len(food[6]) > 0 else None
                )

            if weight.save():
                pass
            else:
                print "not saved"


    def parse_food_group(self):
        f = open('data/sr25/FD_GROUP.txt')
        lines = f.readlines()
        for line in lines:
            food = line.replace('~', '').strip().split('^')
            group = nutrition.SR25FoodGroup(
                    FdGrp_Cd = food[0].decode('cp1252', 'ignore') if len(food[0]) > 0 else None,
                    Fdrp_Desc = food[1].decode('cp1252', 'ignore') if len(food[1]) > 0 else None
                )

            if group.save():
                pass
            else:
                print "not saved"


    def parse_abbrev(self):
        f = open('data/sr25/ABBREV.txt')
        lines = f.readlines()
        l = 0
        for line in lines:
            food = line.replace('~', '').strip().split('^')
            try:
                water = float(food[2])
            except:
                water = None

            abrev = nutrition.SR25Abbrev(
                    NDB_No = food[0].decode('cp1252', 'ignore') if len(food[0]) > 0 else None,
                    Shrt_Desc = food[1].decode('cp1252', 'ignore') if len(food[1]) > 0 else None,
                    Water = water,
                    Energ_Kcal = food[3].decode('cp1252', 'ignore') if len(food[3]) > 0 else None,
                    Protein = float(food[4]) if len(food[4]) > 0 else None,
                    Lipid_Tot = float(food[5]) if len(food[5]) > 0 else None,
                    Ash = float(food[6]) if len(food[6]) > 0 else None,
                    Carbohydrt = float(food[7]) if len(food[7]) > 0 else None,
                    Fiber_TD = float(food[8]) if len (food[8]) > 0 else None,
                    Sugar_Tot = float(food[9]) if len (food[9]) > 0 else None,
                    Calcium = food[10].decode('cp1252', 'ignore') if len(food[10]) > 0 else None,
                    Iron = float(food[11]) if len(food[11]) > 0 else None,
                    Magnesium = food[12].decode('cp1252', 'ignore') if len(food[12]) > 0 else None,
                    Potassium = food[13].decode('cp1252', 'ignore') if len(food[13]) > 0 else None,
                    Sodium = food[14].decode('cp1252', 'ignore') if len(food[14]) > 0 else None,
                    Zinc = float(food[15]) if len(food[15]) > 0 else None,
                    Copper = float(food[16]) if len(food[16]) > 0 else None,
                    Manganese = float(food[17]) if len(food[17]) > 0 else None,
                    Selenium = float(food[18]) if len(food[18]) > 0 else None,
                    Vit_c = float(food[19]) if len(food[19]) > 0 else None,
                    Thiamin = float(food[20]) if len(food[20]) > 0 else None,
                    Riboflavin = float(food[21]) if len(food[21]) > 0 else None,
                    Niacin = float(food[22]) if len(food[22]) > 0 else None,
                    Panto_acid = float(food[23]) if len(food[23]) > 0 else None,
                    Vit_B6 = float(food[24]) if len(food[24]) > 0 else None,
                    Folate_Tot = float(food[25]) if len(food[25]) > 0 else None,
                    Folic_acid = food[26].decode('cp1252', 'ignore') if len(food[26]) > 0 else None,
                    Food_Folate = food[27].decode('cp1252', 'ignore') if len(food[27]) > 0 else None,
                    Folate_DFE = food[28].decode('cp1252', 'ignore') if len(food[28]) > 0 else None,
                    Choline_Tot = food[29].decode('cp1252', 'ignore') if len(food[29]) > 0 else None,
                    Vit_B12 = float(food[30]) if len(food[30]) > 0 else None,
                    Vit_A_IU = float(food[31]) if len(food[31]) > 0 else None,
                    Vit_A_RAE = food[32].decode('cp1252', 'ignore') if len(food[32]) > 0 else None,
                    Retinol = food[33].decode('cp1252', 'ignore') if len(food[33]) > 0 else None,
                    Alpha_Carot = food[34].decode('cp1252', 'ignore') if len(food[34]) > 0 else None,
                    Beta_Carot = food[35].decode('cp1252', 'ignore') if len(food[35]) > 0 else None,
                    Beta_Crypt = food[36].decode('cp1252', 'ignore') if len(food[36]) > 0 else None,
                    Lycopene = food[37].decode('cp1252', 'ignore') if len(food[37]) > 0 else None,
                    LutZea = food[38].decode('cp1252', 'ignore') if len(food[38]) > 0 else None,
                    Vit_E = float(food[39]) if len(food[39]) > 0 else None,
                    Vit_D_mcg = float(food[40]) if len(food[40]) > 0 else None,
                    Vit_D_IU = float(food[41]) if len(food[41]) > 0 else None,
                    Vit_K = float(food[42]) if len(food[42]) > 0 else None,
                    FA_Sat = float(food[43]) if len(food[43]) > 0 else None,
                    FA_Poly = float(food[44]) if len(food[44]) > 0 else None,
                    Cholestrl = float(food[45]) if len(food[45]) > 0 else None,
                    GmWt_1 = float(food[46]) if len(food[46]) > 0 else None,
                    GmWt_Desc1 = food[47].decode('cp1252', 'ignore') if len(food[47]) > 0 else None,
                    GmWt_2 = float(food[48]) if len(food[48]) > 0 else None,
                    GmWt_Desc2 = food[49].decode('cp1252', 'ignore') if len(food[49]) > 0 else None,
                    Refuse_Pct = float(food[50]) if len(food[50]) > 0 else None
                )
            
            if abrev.save():
                print "saved"
            else:
                print "you f'd up"


# p = nutrition.SR25Abbrev.objects()
# p.delete()

def scrape_chipotle():
    soup = BeautifulSoup(urllib2.urlopen('http://www.chipotle.com/en-us/menu/nutritional_information/nutritional_information.aspx').read())

    headings = soup('table')

    unit = [
        "", "", "g", "g", 
        "g", "mg", "mg", 
        "g", "g", "g", "g", 
        "% daily value", 
        "% daily value", 
        "% daily value",
        "% daily value" 
    ]

    for idx, tr in enumerate(headings[3]('tr')):
        if idx != 0:
            ingredient = tr('span')[0].string
            serving_size = tr('span')[1].string
            cals = tr('span')[2].string
            fat_cals = tr('span')[3].string
            total_fat = tr('span')[4].string
            sat_fat = tr('span')[5].string
            trans_fat = tr('span')[6].string
            cholesterol = tr('span')[7].string.replace("<", "")
            sodium = tr('span')[8].string
            carbs = tr('span')[9].string.replace("<", "")
            dietary_fiber = tr('span')[10].string.replace("<", "")
            sugars = tr('span')[11].string.replace("<", "")
            protein = tr('span')[12].string.replace("<", "")
            vit_a = tr('span')[13].string.string.replace("%","")
            vit_c = tr('span')[14].string.string.replace("%","")
            calcium = tr('span')[15].string.string.replace("%","")
            iron = tr('span')[16].string.string.replace("%","")

            food_item = nutrition.StandardNutritionLabelMealItem(
                    name = ingredient,
                    unit = serving_size,
                    calories = int(cals),
                    calories_from_fat = int(fat_cals),
                    total_fat = float(total_fat),
                    saturated_fat = float(sat_fat),
                    trans_fat = float(trans_fat),
                    cholesterol = float(cholesterol),
                    sodium = float(sodium),
                    total_carbs = float(carbs),
                    dietary_fiber = float(dietary_fiber),
                    sugar = float(sugars),
                    protein = float(protein),
                    vit_a = int(vit_a),
                    vit_c = int(vit_c),
                    calcium = int(calcium),
                    iron = int(iron),
                    source = "Chipotle Mexican Grill"
                )

            if food_item.save():
                print "saved"
            else:
                print "didn't save"

# scrape_chipotle()

# objs = nutrition.StandardNutritionLabelMealItem.objects()
# objs.delete()
# print len(objs)

class NutritionEtl():
    def last_meal(self):
        last_nutr = nutrition.NutritionRecord.objects()

        if len(last_nutr) == 0:
            meals = flickr.FlickrPhoto.objects()
            return meals
        else:
            last_record = nutrition.NutritionRecord.objects().order_by("-created_at")
            latest = last_record[0].created_at
            new_records = nutrition.NutritionRecord.objects(created_at__gte=latest)

            if len(new_records) == 0:
                print "all updated"
            else:
                print "records to update"


    def create_new_meals(self):
        meals = self.last_meal()
        if meals != None:
            for pic in meals:
                if pic.info != None:
                    ref_info = nutrition.FlickrRefInfo(
                            photo_id = pic.photo_id,
                            farm = pic.info.farm,
                            server = pic.info.server,
                            secret = pic.info.secret
                        )

                    dates = nutrition.FlickrDates(
                            taken = pic.info.dates.taken,
                            last_update = pic.info.dates.last_update,
                            taken_granularity = pic.info.dates.taken_granularity,
                            posted = pic.info.dates.posted
                        )

                    meal = nutrition.NutritionRecord(
                        phro_created_at = int(time.time()),
                        username = "pdarche",
                        created_at = int(time.mktime(time.strptime(pic.info.dates.taken,'%Y-%m-%d %H:%M:%S'))),
                        flkr_ref_info = ref_info,
                        flkr_dates = dates,
                        meal_item_name = pic.title,
                        img_url = "http://farm%s.staticflickr.com/%s/%s_%s_q.jpg" % (pic.info.farm, pic.server, pic.photo_id, pic.secret),
                        meal = None, #there will be some analysis of the title to extract a meal
                        venue = None, #there will be a guess of venue based on chekcins
                        venue_category = None, #there will be a guess of venue_category based on chekcins
                        from_loc = [ pic.info.location.lon, pic.info.location.lat ] if pic.info.location != None else None,
                        eaten_loc = None, #there will be a guess of venue based on chekcins
                        unit = None,
                        calories = None,
                        calories_from_fat = None,
                        total_fat = None,
                        saturated_fat = None,
                        trans_fat = None,
                        cholesterol = None,
                        sodium = None,
                        total_carbs = None,
                        dietary_fiber = None,
                        sugar = None,
                        protein = None,
                        vit_a = None,
                        vit_c = None,
                        calcium = None,
                        iron = None,
                        source = None,
                        ingredients = None
                    )

                    if meal.save():
                        print "meal saved"
                    else:
                        print "meal didn't save"
            
# m = NutritionEtl()
# m.create_new_meals()


