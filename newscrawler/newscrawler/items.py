# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class SubstanceItem(scrapy.Item):
    nom_substance = scrapy.Field()
    lien_substance  = scrapy.Field()
    fiche = scrapy.Field()
    indication = scrapy.Field()

    def __str__(self):
        return ""

class SubstanceItem_med(scrapy.Item):
    nom_substance = scrapy.Field()
    liste_medicament = scrapy.Field()

    def __str__(self):
        return ""

class MedicamentItem(scrapy.Item):
    nom_medicament = scrapy.Field()
    lien_medicament = scrapy.Field()
    substance = scrapy.Field()
    activeIngredient = scrapy.Field()
    descriptif = scrapy.Field()

    def __str__(self):
        return ""

class jai_mal_item(scrapy.Item):
    name = scrapy.Field()
    lien = scrapy.Field()
    intro = scrapy.Field()
    que_faire = scrapy.Field()
    conduite = scrapy.Field()
    comment_med = scrapy.Field()
