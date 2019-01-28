# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from ..items import SubstanceItem

class VidalSpider(scrapy.Spider):
    name = 'vidal'
    custom_settings = {
        'ITEM_PIPELINES': {
            'newscrawler.pipelines.TextPipeline_substance': 100,
            'newscrawler.pipelines.MongoPipeline': 300
        }
    }
    allowed_domains = ['vidal.fr']
    start_urls = ['https://www.vidal.fr/substances/Substances-A.htm']

    def parse(self, response):

        letter_link = [response.urljoin(url)
            for url in response.xpath("//ul[@class='menu_index']").css("a::attr(href)").extract()
            ]

        for lien in letter_link:
            yield Request(lien, callback=self.parse_letter)

    def parse_letter(self, response):

        substance_list = [
            [name, response.urljoin(url)]
            for name, url in zip(
            response.xpath("//ul[@class='substances list_index']").css("a::text").extract(),
            response.xpath("//ul[@class='substances list_index']").css("a::attr(href)").extract()
            )]

        for i in substance_list:
            yield Request(i[1], callback=self.parse_substance, meta={'nom':i[0], 'lien':i[1]})

    def parse_substance(self, response):

        nom = response.meta.get('nom')
        lien = response.meta.get('lien')
        fiche = response.xpath("//div[@itemprop='mechanismOfAction']//text()").extract()
        indication = response.xpath("//div[@itemprop='Indication']//text()").extract()

        yield SubstanceItem(
            Nom_Substance = nom,
            Lien_Substance = lien,
            Fiche = fiche,
            Indication = indication
            )
