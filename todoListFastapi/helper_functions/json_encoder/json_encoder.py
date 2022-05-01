'''
I had to implement my custom json encoder as bson object id was hard to parse
'''
import json
class JSONEncoder(json.JSONEncoder):
    def encode(self, id):
        if '_id' in id:
            id['_id'] = str(id['_id'])
        return id