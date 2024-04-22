# from .. import setup_database as db 
# from ..Applications import setup_database as db
# from Applications import setup_database as db
# import setup_database from Applications as db
# import setup_database  as db
from . import setup_database as db
import pprint

colaliexpress = db.mydb["alibaba_product_collection"] 

# Define function to extract required fields
def extract_data(document):
    extracted_data = {
        "name": document.get("name", ""),
        "image_table": document.get("images", []),
        "price": document.get("price", ""),
        "description": document.get("description", []),
        "un_separated_comments": document.get("un_separated_comments", []),
        "info_comment" : document.get("info_comment", {}),
        "info_comment_Sent" : document.get("info_comment_Sent", {}),
    }
    return extracted_data

def extract_data_one(document):
    extracted_data = {
        "name": document["name"]if "name" in document else "",
        "image_table": document["images"] if "images" in document else [],
        "price": document["price"] if "price" in document else "",
        "description": document["description"] if "description" in document else [],
        "un_separated_comments": document["un_separated_comments"] if "un_separated_comments" in document else [],
        "info_comment" : document["info_comment"] if  "info_comment" in document else {},
        "info_comment_Sent" : document["info_comment_Sent"] if  "info_comment_Sent" in document else {}
    }
    return extracted_data

def ReturnOneDocFromAliExpres(NbrDOC):
    cursor = colaliexpress.find({}).limit(NbrDOC)
    if NbrDOC == 1 :
        document = cursor.next()
        extracted_documents = extract_data_one(document)
    else:
        extracted_documents = []
        for document in cursor:
            extracted_documents.append(extract_data(document))
    return extracted_documents

# def extract_data_one(document):
#     extracted_data = {
#         "name": document.name,
#         "image_table": document.images,
#         "price": document.price,
#         "description": document.description,
#         "un_separated_comments": document.un_separated_comments
#     }
#     return extracted_data

# def extract_data_one(document):
#     extracted_data = {
#         "name": document.get("name", ""),
#         "image_table": document.get("images", []),
#         "price": document.get("price", ""),
#         "description": document.get("description", []),
#         "un_separated_comments": document.get("un_separated_comments", [])
#     }
#     return extracted_data




# def get_documents():
#     # Fetch documents from MongoDB collection
#     cursor = colaliexpress.find({}).limit(1)  # You can add query conditions within find() if needed
#     # cursor = colaliexpress.findOne()  # You can add query conditions within find() if needed

#     # Initialize a list to store extracted documents
#     extracted_documents = []

#     # Extract data from each document and append to the list
#     for document in cursor:
#         extracted_documents.append(extract_data(document))

#     return extracted_documents

# def ReturnOneDocFromAliExpres(NbrDOC):
#     cursor = colaliexpress.find({}).limit(NbrDOC)
#     # pprint.pprint(cursor.next())
#     if NbrDOC == 1 :
#         # extracted_documents = extract_data_one(cursor)
#         # extracted_documents = extract_data_one(cursor.next())
#         # extracted_documents = 0

#         # Obtenir le prochain document du curseur
#         document = cursor.next()
#         # Extraire les données du document avec extract_data_one
#         # extracted_documents = extract_data_one(document)
#         extracted_documents = extract_data_one(document)

#         # pprint.pprint(extracted_documents)
#     else:
#         extracted_documents = []
#         for document in cursor:
#             extracted_documents.append(extract_data(document))
#     return extracted_documents




# Usage example:
# all_documents = ReturnOneDocFromAliExpres(3)
# all_documents = ReturnOneDocFromAliExpres(1)
# # for doc in all_documents:
# #     pprint.pprint(doc)
# pprint.pprint(all_documents)
# print(type(all_documents))
# # print(all_documents["un_separated_comments"][0]["comment"])
# # print(all_documents)
# print(all_documents[2]["description"][1]["value"])

