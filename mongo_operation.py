import pymongo
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')

class MongoOperation:
    def __init__(self, username="YOUR_USERNAME", password="YOUR_PASSWORD"):
        try:
            self. username = username
            self.password = password
            self.url = f"mongodb+srv://{username}:{password}@clusterofsurajit.99hrrkq.mongodb.net/?retryWrites=true&w=majority"
        except Exception as e:
            logging.error(str(e))
    
    def get_mongo_client(self):
        try:
            client = pymongo.MongoClient(self.url)
            return client
        except Exception as e:
            logging.error(str(e))
    
    def get_database(self, db_name="ineuron"):
        try:
            client = self.get_mongo_client()
            database = client[db_name]
            return database
        except Exception as e:
            logging.error(str(e))
    
    def get_collection(self, db_name="ineuron", collection_name="courses"):
        try:
            database = self.get_database(db_name)
            collection = database[collection_name]
            return collection
        except Exception as e:
            logging.error(str(e))
