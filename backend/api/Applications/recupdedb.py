from . import setup_database as stp

def recupdedb(collc, userVal):
    listRes = []
    for i in collc.find({'username':userVal}):
        listRes.append(i)
    return listRes

def recupdedb2(collc, userVal):
    res = collc.find({'username':userVal})
    return res