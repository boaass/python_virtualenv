import pymongo


client = pymongo.MongoClient()
db = client.example
widgets = db.widgets
widgets.insert({"name": "flibnip", "description": "grade-A industrial flibnip", "quantity": 3})

doc = widgets.find_one({'name':'flibnip'})
doc['quantity'] = 4
db.widgets.save(doc)
widgets.insert({"name": "smorkeg", "description": "for external use only", "quantity": 4})
widgets.insert({"name": "clobbasker", "description": "properties available on request", "quantity": 2})
for doc in widgets.find({'name' : 'smorkeg'}):
    widgets.remove()

# import json
# del doc['_id']
# print json.dumps(doc)