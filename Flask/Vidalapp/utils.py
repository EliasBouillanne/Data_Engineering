from pymongo import MongoClient

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import json

class MongoDB():
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client['Vidal']

    def find(self, collection):
        return self.db[collection].find()

    def collection(self):
        return self.db.list_collection_names()

class ElasticsearchDB():
    def __init__(self):
        self.mongo = MongoDB()
        self.client = Elasticsearch()

    def index_bulk(self):
        for collection in self.mongo.collection():
            bulk(client=self.client, actions=self.index_mongo(collection))

    def index_mongo(self, collection):
        cursor = self.mongo.find(collection)
        for item in cursor:
            _id = str(item['_id'])
            del item['_id']
            action = {
                '_op_type': 'index',
                "_index" : collection,
                "_type"  : collection+"_document",
                "_id"    : _id,
                "_source": item
            }
            yield action

    def search_insubstance(self, substance):
        query = json.dumps({
          "query": {
            "bool" : {
              "must" : [
                  {
                "term" : { "nom_substance" : substance }},
              ]
          }
        }
        })

        result = self.client.search(index="substance_items", body=query)
        return result['hits']['hits']

    def search_inmedicament(self, substance, excipient=False):
        if excipient==False:
            query = json.dumps({
              "query": {
                "bool" : {
                    "should": [
                      { "term": { "substance": substance } }
                      ]
              }
            }
            })
        else:
            query = json.dumps({
              "query": {
                "bool" : {
                  "must_not" : {
                          "term" : { "excipient" : excipient }
                  },
                  "should": [
                    { "term": { "substance": substance } }
                    ]
                 }
              }
            })

        result = self.client.search(index="medicament_items", body=query)
        return result['hits']['hits']


    def format_results(self, result, content):
        """Print results nicely:
        doc_id) content
        """
        data = [doc for doc in result['hits']['hits']]
        for doc in data:
            print("%s" % (doc['_source'][content]))

def reshape_to_3_columns(_list):
    list_out = list()
    row = 0
    i = 0
    while i < len(_list):
        list_out.append([_list[i]])
        i += 1
        count = 0
        while i < len(_list) and count < 2:
            list_out[row].append(_list[i])
            i += 1
            count += 1
        row += 1
    return list_out

def init_db():
    elastic = ElasticsearchDB()
    elastic.index_bulk()
