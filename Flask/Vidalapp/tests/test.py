from pymongo import MongoClient

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

class MongoDB():
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client['Vidal']

class ElasticsearchDB():
    def __init__(self):
        self.mongo = MongoDB()
        self.client = Elasticsearch()
        bulk(self.client, self.index_mongo('substance_items'), request_timeout=30)
        bulk(self.client, self.index_mongo('medicament_items'), request_timeout=30)

    def index_mongo(self, index):
        cursor = list(self.mongo.db[index].find())
        print(len(cursor))
        for item in cursor:
            _id = str(item['_id'])
            del item['_id']
            document = {
                "_index" : index,
                "_type"  : index+"_document",
                "_id"    : _id,
                "_source": item
            }
            yield document

elastic = ElasticsearchDB()
