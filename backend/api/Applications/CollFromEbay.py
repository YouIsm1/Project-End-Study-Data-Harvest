# import setup_database  as db
from . import setup_database as db
import pprint

collection = db.mydb["ebay_product_collection"] 

def extract_data(document):
    extracted_data = {
        "name": document.get("name", ""),
        "image_table": document.get("images", []),
        "price": document.get("price", ""),
        # "rating": document.get("rating", ""),
        "description": document.get("description", []),
        "un_separated_comments": document.get("un_separated_comments", []),
        "info_comment" : document.get("info_comment", {}),
        "info_comment_Sent" : document.get("info_comment_Sent", {})
    }
    return extracted_data

def extract_data_one(document):
    extracted_data = {
        "name": document["name"] if "name" in document else "",
        "image_table": document["images"] if "images" in document else [],
        "price": document["price"] if "price" in document else "",
        # "rating": document["rating"] if "rating" in document else "",
        "description": document["description"] if "description" in document else [],
        "un_separated_comments": document["un_separated_comments"] if "un_separated_comments" in document else [],
        "info_comment" : document["info_comment"] if  "info_comment" in document else {},
        "info_comment_Sent" : document["info_comment_Sent"] if  "info_comment_Sent" in document else {}
    }
    return extracted_data

def ReturnOneDocFromEbay(NbrDOC):
    cursor = collection.find({}).limit(NbrDOC)
    nbrDoccoll = 0
    if NbrDOC == 1 :
        document = cursor.next()
        extracted_documents = extract_data_one(document)
        nbrDoccoll = 1
        # pprint.pprint(document)
    else:
        extracted_documents = []
        for document in cursor:
            extracted_documents.append(extract_data(document))
            nbrDoccoll += 1
    return extracted_documents

# all_documents = ReturnOneDocFromEbay(1)
# print(all_documents["name"])
# pprint.pprint(all_documents)