# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class SubstanceItem(scrapy.Item):
    Nom_Substance = scrapy.Field()
    Lien_Substance  = scrapy.Field()
    Fiche = scrapy.Field()
    Indication = scrapy.Field()

    def __str__(self):
        return ""

class SubstanceItem_med(scrapy.Item):
    Nom_Substance = scrapy.Field()
    Liste_Medicament = scrapy.Field()

    def __str__(self):
        return ""

class MedicamentItem(scrapy.Item):
    Nom_Medicament = scrapy.Field()
    Lien_Medicament = scrapy.Field()
    Substance = scrapy.Field()
    ActiveIngredient = scrapy.Field()
    Descriptif = scrapy.Field()

    def __str__(self):
        return ""

def jai_mal_item(scrapy.Item):
    Name = scrapy.Field()
    Lien = scrapy.Field()
    Intro = scrapy.Field()
    Que_faire = scrapy.Field()
    Conduite = scrapy.Field()
    comment_med = scrapy.Field()
