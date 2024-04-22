import pymongo as pm

myclient = pm.MongoClient('mongodb://localhost:27017/')

mydb = myclient['products_database']


