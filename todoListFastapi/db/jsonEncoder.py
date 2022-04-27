import json
from bson import ObjectId

class JSONEncoder(json.JSONEncoder):
    def encode(self, o):
        if '_id' in o:
            o['_id'] = str(o['_id'])
        return o
