from . import setup_database
# from setup_database import mydb
from django.http import HttpResponse

mycol = setup_database.mydb["UserEffect"]

def savedb(list = []):
     for i in list:
          mycol.insert_one(i)
#     message = "Data has been added to the database"
#     return  message
     return True