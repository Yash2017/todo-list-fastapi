import json
class JSONEncoder(json.JSONEncoder):
    def encode(self, id):
        if '_id' in id:
            id['_id'] = str(id['_id'])
        return id