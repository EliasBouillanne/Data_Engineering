# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from ..items import MedicamentItem

class Vidal2Spider(scrapy.Spider):
    #Spider permettant de scraper tous les médicaments du vidal
    name = 'vidal2'
    custom_settings = {
        'ITEM_PIPELINES': {
            'newscrawler.pipelines.TextPipeline_medicament': 100,
            'newscrawler.pipelines.MongoPipeline': 300
        }
    }
    allowed_domains = ['vidal.fr']
    start_urls = ['https://www.vidal.fr/Sommaires/Medicaments-A.htm']

    def parse(self, response):
        #Récupération du lien de l'index pour chaque lettres de l'alaphabet des médicaments
        letter_link = [response.urljoin(url)
            for url in response.xpath("//ul[@class='menu_index']").css("a::attr(href)").extract()
            ]

        for lien in letter_link:
            yield Request(lien, callback=self.parse_letter)

    def parse_letter(self, response):
        #Récupération de tous les liens à scraper pour chaque médicaments
        medicament_list = [
            [name, response.urljoin(url)]
            for name, url in zip(
            response.xpath("//ul[@class='medicaments list_index']").css("a::text").extract(),
            response.xpath("//ul[@class='medicaments list_index']").css("a::attr(href)").extract()
            )]
        #On transfert à la fonction suivante les données scrappées
        for i in medicament_list:
            yield Request(i[1], callback=self.parse_medicament, meta={'nom':i[0], 'lien':i[1]})

    def parse_medicament(self, response):

        nom = response.meta.get('nom')
        lien = response.meta.get('lien')
        substance = response.xpath("//div[@class='mono_content']//div[@class='compositionTable']//text()").extract()
        excipient = response.xpath("//div[@class='mono_content']//span[@itemprop='activeIngredient']//text()").extract()
        descriptif = response.xpath("//div[@class='mono_content']//div[@class='package_description']//text()").extract()

        #On crée l'item avec toutes les informations pour l'envoyer aux pipelines
        yield MedicamentItem(
            nom_medicament = nom,
            lien_medicament = lien,
            substance = substance,
            excipient = excipient,
            descriptif = descriptif
            )
