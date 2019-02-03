# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
import pymongo
import numpy as np

class MongoPipeline(object):
    #class permettant l'importation et la mis à jour des données
    #dans la base de données mongo "Vidal"

    collection_name = str()

    def open_spider(self, spider):
        #On instencie une connexion à la base de données
        self.client = pymongo.MongoClient()
        self.db = self.client["Vidal"]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        #Vérification de la collection à utiliser en fonction de l'item
        if "nom_substance" in item:
            nom = "nom_substance"
            self.collection_name = 'substance_items'
        elif "nom_medicament" in item:
            nom = "nom_medicament"
            self.collection_name = 'medicament_items'
        else:
            #Si l'item ne correspond à aucune collection, il est supprimé
            DropItem("Item non valide pour importation dans DB" % item)

        try:
            #Insertion de l'item dans la base de données, si il est déjà présent
            #il est mis à jours avec les nouveaux champs.
            self.db[self.collection_name].update(
                {nom : item[nom]},
                {"$set" : dict(item)},
                upsert=True)
            return item
        except:
            DropItem("Item non valide pour importation dans DB" % item)

class TextPipeline_substance(object):
    #Class permettant de traiter les données de l'item substance
    def process_item(self, item, spider):
        try:
            item['fiche'] = clean(item['fiche'])
            item['indication'] = clean(item['indication'])
            return item
        except:
            DropItem("Missing fiche/indication in %s" % item)

class TextPipeline_medicament(object):
    #Class permettant de traiter les données de l'item medicament
    def process_item(self, item, spider):
        #Vérification que l'item est valide (non nul)
        if type(item) == 'NoneType':
            DropItem("Item non valide pour transformation" % item)
        else :
            try :
                #Traitement des substances
                del item['substance'][0]
                item['substance'] = [i for i in item['substance'] if i.rstrip() != '']

                #Traitement du descriptif
                del item['descriptif'][0]
                #On supprime les élements en double et on met en minuscule tout les caractères
                #afin de faciliter le traitement
                item['descriptif'] = lower(list(set(item['descriptif'])))
                #Traitement du code cip
                item['descriptif'] = check_cip(item['descriptif'])
                #Supression des espaces en fin de chaine et des \n \r
                item['descriptif'] = [clean(i) for i in item['descriptif']]
                #Armonisation des champs entre tous les médicaments
                item['descriptif'] = str_sup('non agréé aux collectivités', item['descriptif'])
                item['descriptif'] = str_sup('supprimé', item['descriptif'])
                item['descriptif'] = str_in('agréé aux collectivités', item['descriptif'])
                item['descriptif'] = str_in('commercialisé', item['descriptif'])
                item['descriptif'] = str_in('modèle hospitalier', item['descriptif'])
                item['descriptif'] = check_remboursement(item['descriptif'])
                #On convertit en dictionnaire la liste afin de l'importer dans la base de données
                item['descriptif'] = list_to_dict(item['descriptif'])
                return item
            except:
                DropItem("Item non valide pour transformation" % item)


class TextPipeline_jai_mal(object):
    #Class permettant de traiter les données de l'item jai_mal
    def process_item(self, item, spider):
        try:
            item['que_faire'] = clean(item['que_faire'])
            item['conduite'] = clean1(item['conduite'])
            item['comment_med'] = clean_med(item['comment_plus_med'])
            return item
        except:
            DropItem("Missing fiche/indication in %s" % item)


def lower(liste):
    '''
        Met en minuscule toutes les strings de la liste entrée en paramètre.

        :param a: une liste de string
        :type a: list

        :Example:
        >>> lower(["AnkA", "bOnjour"])
        ["anka", "bonjour"]
    '''
    return [i.lower() for i in liste]

def clean(liste_):
    '''
        Supprime les \n, remplace les \r par des espaces et aggrège la listeself.
        Supprime enfin les espaces en début et fin de la chaîne obtenu.

        :param a: une liste de string
        :type a: list

        :Example:
        >>> clean(["   anka/rj", "\rbonjour/n "])
        ["anka j bonjour"]
    '''
    string_ = ''.join(liste_).replace('\r', " ").replace('\n', "")
    return string_.strip()

def clean1(liste_):
    '''
        Supprime les \n, remplace les \r par des espaces et supprime les espaces en début
        et fin de la chaîne obtenu.

        :param a: une liste de string
        :type a: list

        :Example:
        >>> clean1(["   anka/rj", "\rbonjour/n "])
        ["anka j", "bonjour"]
    '''
    liste_ = liste_.replace('\r', " ").replace('\n', "")
    return string_.strip()

def str_in(string, liste):
    '''
        Vérifie si un élement est présent dans liste, si oui la fontion rajout
        ":oui", si non elle rajoute le nom de l'élément suivis de ":non"

        :param a: une string
        :param b: une liste de string
        :type a: str
        :type b: list

        :Example:
        >>> str_in("bonjour", ["bonjour", "remboursement"])
        ["bonjour:oui", "remboursement"]
    '''
    a=0
    for i in range(len(liste)):
        if liste[i].find(string) != -1:
            liste[i] = liste[i] + ':oui'
            a=1
    if a==0:
        liste.append(string + ':non')
    return liste

def str_sup(string, liste):
    '''
    Supprime l'élement de la liste passé en paramètre.

        :param a: une string
        :param b: une liste de string
        :type a: str
        :type b: list

        :Example:
        >>> str_sup("bonjour", ["bonjour", "remboursement"])
        ["remboursement"]
    '''
    try:
        liste.remove(string)
        return liste
    except:
        return liste

def check_remboursement(liste):
    '''
        Vérifie si la liste passé en paramètre contient l'élément "remboursement".
        Sinon rajoute à la liste "remboursement:nc".

        :param a: une liste
        :type a: list

        :Example:
        >>> str_sup("bonjour", ["bonjour", "remboursement"])
        ["remboursement"]
    '''
    a=0
    for i in range(len(liste)):
        if 'remboursement' in liste[i]:
            a=1
    if a==0:
        liste.append('remboursement:nc')
    return liste

def check_cip(liste):
    '''
        Met en forme le cip de la liste passé en paramètre.

        :param a: une liste
        :type a: list

        :Example:
        >>> check_cip(["bonjour80039", "cip:7890", "remboursement", "80090"])
        ["bonjour", "cip:78908003980090", "remboursement"]
    '''
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
