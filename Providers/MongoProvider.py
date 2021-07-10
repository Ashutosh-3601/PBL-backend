import pymongo

class MongoStore:
    def __init__(self, url, ip = None, port = None) :
        self.connectionURL = url if url is not None else 'https://'+ip+':'+port

    def connect(self):
        try:
           self.client = pymongo.MongoClient(self.connectionURL)
        except:
            raise RuntimeError('[MongoStore] Connection to DB failed!')
        
    def get(self, collection, doc):
        DB = self.client['PBL']
        col = DB[collection]
        result = col.find_one(doc)
        return result
        
    def insert(self, collection, doc):
        DB = self.client['PBL']
        col = DB[collection]
        result = col.insert_one(doc)
        return result