from typing import Any
from pymongo import MongoClient

db = MongoClient()
# == run code ==
# cmd : export FLASK_DEBUG=1
# flask run --port=8001 --host="0.0.0.0"
    

    # metaclass = SingletonMeta

class Mongodb() :
    _instances  = {}
    # mongod 
    def __init__(self, connection_string, db_name : str) :
        self.connection_string = connection_string
        self.db_name = db_name
        self.client = MongoClient(connection_string)
        self.db = self.client[db_name]
    
    def __call__(cls, *args: Any, **kwds: Any) -> Any:
        if cls not in cls._instances :
            cls._instances[cls] = super(Mongodb, cls).__call__(*args, **kwds)
        return cls._instances[cls]
    
    def refreshSock(self) :
        self.client = MongoClient(self.connection_string)
        self.db = self.client[self.db_name]
    
    def get_collection(self, collection_name) :
        
        return self.db[collection_name]
    
    
    def close_connection(self) :
        self.client.close()
        
        

