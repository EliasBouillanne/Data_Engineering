# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from ..items import jai_mal_item

class VidalSpider(scrapy.Spider):
    name = 'vidal_jai_mal'

    custom_settings = {
        'ITEM_PIPELINES': {
            'newscrawler.pipelines.TextPipeline_jai_mal': 100
            #'newscrawler.pipelines.MongoPipeline': 300
        }
    }

    allowed_domains = ['https://eurekasante.vidal.fr/']
    start_urls = ['https://eurekasante.vidal.fr/maladies/j-ai-mal-a.html']

    def parse(self, response):
        response = response.xpath("//div[@class='frame clearFix']/ul/li/a/@href|//div[@class='frame clearFix']/ul/li/a/text()").extract()
        jai_mal_dict = dict()

        while(i != len(response)-1):
            jai_mal_dict[response[i]] : response.urljoin(response[i])

        for name, lien in jai_mal_dict.items():
            yield Request(lien, callback=self.parse_jai_mal, meta={'name':name, 'lien':lien})

    def parse_jai_mal(self, response):
        name = response.meta.get('name')
        lien = response.meta.get('lien')

        #Intro
        intro = response.xpath("//p[@class='intro']//text()").extract()

        yield Request(lien+"?pb=que-faire", callback=self.parse_que_faire, meta={'name':name, 'lien':lien, 'intro':intro})
        yield Request(lien+"?pb=traitements", callback=self.parse_traitements)

    def parse_que_faire(self, response):
        name = response.meta.get('name')
        lien = response.meta.get('lien')
        intro = response.meta.get('intro')

        #Que faire ?
        #faire un ''.join()
        que_faire = response.xpath("//ul[@class='tiret']//text()").extract()

        #Conduite à tenir ?
        #split '/r/n' et lstrip puis ''.join
        conduite = {'rouge': response.xpath("//td[@class='pathotabloreagirrouge2']//text()").extract(),
            'orange': response.xpath("//td[@class='pathotabloreagirorange2']//text()").extract(),
            'jaune': response.xpath("//td[@class='pathotabloreagirjaune2']//text()").extract(),
            'vert': response.xpath("//td[@class='pathotabloreagirvert2']//text()").extract()
            }

        yield Request(lien+"?pb=traitements", callback=self.parse_traitements, meta={'name':name, 'lien':lien, 'intro':intro, 'que_faire':que_faire, 'conduite':conduite})



    def parse_traitements(self, response):
        name = response.meta.get('name')
        lien = response.meta.get('lien')
        intro = response.meta.get('intro')
        que_faire = response.meta.get('que_faire')
        conduite = response.meta.get('conduite')

        #Comment soigner ?
        #''.join(
        #comment_soigner = response.xpath("//div[@class='frame clearFix']/p//text()").extract()

        #Comment_soigner + Médicament associé
        comment_med = response.xpath("//div[@class='frame clearFix']/h2|//div[@class='frame clearFix']/p//text()|//div[contains(@class, 'list_item')]/ul/li/a/@href").extract()

        yield jai_mal_item(
            Name = name,
            Lien = lien,
            Intro = intro,
            Que_faire = que_faire,
            Conduite = conduite,
            comment_med = comment_med
            )
