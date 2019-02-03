# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from ..items import SubstanceItem_med

class Vidal1Spider(scrapy.Spider):
    #Spider permettant de scrapper toutes les médicaments associés à chaque substances
    name = 'vidal1'
    custom_settings = {
        'ITEM_PIPELINES': {
            'newscrawler.pipelines.MongoPipeline': 300
        }
    }
    allowed_domains = ['vidal.fr']
    start_urls = ['https://www.vidal.fr/Sommaires/Substances-A.htm']

    def parse(self, response):
        #Récupération du lien de l'index pour chaque lettres de l'alaphabet des substances associés aux médicaments
        letter_link = [
            response.urljoin(url)
            for url in response.xpath("//ul[@class='menu_index']").css("a::attr(href)").extract()
            ]

        for lien in letter_link:
            yield Request(lien, callback=self.parse_letter)

    def parse_letter(self, response):
        #Récupération du lien de toutes les substances associés aux médicaments
        substance_list = [
            [name, response.urljoin(url)]
            for name, url in zip(
            response.xpath("//ul[@class='substances list_index has_children']").css("a::text").extract(),
            response.xpath("//ul[@class='substances list_index has_children']").css("a::attr(href)").extract()
            )]

        #On transfert à la fonction suivante les données scrapées
        for i in substance_list:
            yield Request(i[1], callback=self.parse_substance, meta={'nom':i[0]})

    def parse_substance(self, response):

        nom = response.meta.get('nom')
        medicament = [
            {"Nom_Medicament" : name, "Lien_Medicament" : response.urljoin(url)}
            for name, url in zip(
            response.xpath("//ul[@class='list_index']").css("a::text").extract(),
            response.xpath("//ul[@class='list_index']").css("a::attr(href)").extract()
            )]

        #On crée l'item avec toutes les informations pour l'envoyer aux pipelines
        yield SubstanceItem_med(
            nom_substance = nom,
            liste_medicament = medicament
            )
