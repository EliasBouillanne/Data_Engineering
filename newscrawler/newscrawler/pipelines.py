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
        if "nom_substance" in item:
            nom = "nom_substance"
            self.collection_name = 'substance_items'
        elif "nom_medicament" in item:
            nom = "nom_medicament"
            self.collection_name = 'medicament_items'
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
            item['fiche'] = clean(item['fiche'])
            item['indication'] = clean(item['indication'])
            return item
        except:
            DropItem("Missing fiche/indication in %s" % item)

class TextPipeline_medicament(object):

    def process_item(self, item, spider):
        if type(item) == 'NoneType':
            DropItem("Item non valide pour transformation" % item)
        else :
            try :
                del item['substance'][0]
                item['substance'] = [i for i in item['substance'] if i.rstrip() != '']

                del item['descriptif'][0]
                item['descriptif'] = lower(list(set(item['descriptif'])))
                item['descriptif'] = check_cip(item['descriptif'])
                item['descriptif'] = [clean(i) for i in item['descriptif']]
                item['descriptif'] = str_sup('non agréé aux collectivités', item['descriptif'])
                item['descriptif'] = str_sup('supprimé', item['descriptif'])
                item['descriptif'] = str_in('agréé aux collectivités', item['descriptif'])
                item['descriptif'] = str_in('commercialisé', item['descriptif'])
                item['descriptif'] = str_in('modèle hospitalier', item['descriptif'])
                item['descriptif'] = check_remboursement(item['descriptif'])
                item['descriptif'] = list_to_dict(item['descriptif'])
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
            DropItem("Missing fiche/indication in %s" % item)


def lower(liste):
    return [i.lower() for i in liste]

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
        if 'remboursement' in liste[i]:
            a=1
    if a==0:
        liste.append('remboursement:nc')
    return liste

def check_cip(liste):
    index_to_r =  list()
    cip = str()
    for index, i in enumerate(liste):
        try:
            cip += str(int(i))
            index_to_r.append(index)
        except:
            continue
    liste = list(np.delete(np.array(liste), index_to_r))
    for index, i in enumerate(liste):
        if i[0:3]=="cip":
            liste[index] += cip
            return liste
    liste.append("cip:{}".format(cip))
    return liste

def list_to_dict(liste):
    d = dict()
    [liste.remove(i) for i in liste if len(i)==0]
    for i in liste:
        s = i.split(':', maxsplit=1)
        d[s[0].strip().replace(' ','_')] = s[1].strip()
    return d

def clean_med(liste):
    for i in liste:
        while i[0:1] != "<h":
            i = i.split('<h2')[1]
