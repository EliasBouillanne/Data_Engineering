# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
import pymongo
import numpy as np

class MongoPipeline(object):

    collection_name = str()

    def open_spider(self, spider):
        self.client = pymongo.MongoClient()
        self.db = self.client["Vidal"]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if "Nom_Substance" in item:
            nom = "Nom_Substance"
            self.collection_name = 'Substance_Items'
        elif "Nom_Medicament" in item:
            nom = "Nom_Medicament"
            self.collection_name = 'Medicament_Items'
        else:
            DropItem("Item non valide pour importation dans DB" % item)

        try:
            self.db[self.collection_name].update(
                {nom : item[nom]},
                {"$set" : dict(item)},
                upsert=True)
            return item
        except:
            DropItem("Item non valide pour importation dans DB" % item)

class TextPipeline_substance(object):

    def process_item(self, item, spider):
        try:
            item['Fiche'] = clean(item['Fiche'])
            item['Indication'] = clean(item['Indication'])
            return item
        except:
            DropItem("Missing Fiche/Indication in %s" % item)

class TextPipeline_medicament(object):

    def process_item(self, item, spider):
        if type(item) == 'NoneType':
            DropItem("Item non valide pour transformation" % item)
        else :
            try :
                del item['Substance'][0]
                item['Substance'] = [i for i in item['Substance'] if i.rstrip() != '']

                del item['Descriptif'][0]
                item['Descriptif'] = check_cip(item['Descriptif'])
                item['Descriptif'] = [clean(i) for i in item['Descriptif']]
                item['Descriptif'] = str_sup('Non agréé aux Collectivités', item['Descriptif'])
                item['Descriptif'] = str_sup('Supprimé', item['Descriptif'])
                item['Descriptif'] = str_in('Agréé aux Collectivités', item['Descriptif'])
                item['Descriptif'] = str_in('Commercialisé', item['Descriptif'])
                item['Descriptif'] = str_in('Modèle hospitalier', item['Descriptif'])
                item['Descriptif'] = check_remboursement(item['Descriptif'])
                item['Descriptif'] = list_to_dict(item['Descriptif'])
                return item
            except:
                DropItem("Item non valide pour transformation" % item)


class TextPipeline_jai_mal(object):
    def process_item(self, item, spider):
        try:
            item['que_faire'] = clean(item['que_faire'])
            item['conduite'] = clean1(item['conduite'])
            item['comment_med'] = clean_med(item['comment_plus_med'])
            return item
        except:
            DropItem("Missing Fiche/Indication in %s" % item)


def clean(string_):
    string_ = ''.join(string_).replace('\r', " ").replace('\n', "")
    return string_.strip()

def clean1(string_):
    string_ = string_.replace('\r', " ").replace('\n', "")
    return string_.strip()

def str_in(string, liste):
    a=0
    for i in range(len(liste)):
        if liste[i].find(string) != -1:
            liste[i] = liste[i] + ':oui'
            a=1
    if a==0:
        liste.append(string + ':non')
    return liste

def str_sup(string, liste):
    try:
        liste.remove(string)
        return liste
    except:
        return liste

def str_change(string, new_string, liste):
    for i in range(len(liste)):
        if liste[i] == string:
            liste[i] = new_string
    return liste

def check_remboursement(liste):
    a=0
    for i in range(len(liste)):
        if 'Remboursement' in liste[i]:
            a=1
    if a==0:
        liste.append('Remboursement:NC')
    return liste

def check_cip(liste):
    index_to_r =  list()
    for index, i in enumerate(liste):
        try:
            liste[0] = liste[0] + str(int(i))
            index_to_r.append(index)
        except:
            pass
    return list(np.delete(np.array(liste), index_to_r))


def list_to_dict(liste):
    d = dict()
    for i in liste:
        s = i.split(':', maxsplit=1)
        d[s[0].strip().replace(' ','_')] = s[1].strip()
    return d

def clean__med(liste):
    for i in liste:
        while i[0:1] != "<h":
            i = i.split('<h2')[1]
