# import setup_database  as db
# from setup_database import mydb
from . import setup_database as db
import pprint

collectiondb = db.mydb["amazon_product_collection"] 
# collectiondb = mydb["scrapedatatestAmazon"] 

#converter from inr to dollar
def from_inr_to_dollar(prix):
    prix = prix.replace(",", "")
    if isinstance(prix, str):
        try:
            prix = float(prix)
        except ValueError:
            return None
    tauxChange = 0.012
    prixDollar = tauxChange * prix
    return prixDollar

def extract_data(document):
    prix_inr = document.get("price", "")
    prixDollar = from_inr_to_dollar(prix_inr)
    extracted_data = {
        "name": document.get("name", ""),
        # "image_table": list(document.get("img", [])),
        #"price": document.get("price", ""),
        "price" : prixDollar,
        "rating": document.get("rating", ""),
        "description": document.get("description", []),
        "un_separated_comments": document.get("un_separated_comments", []),
        "info_comment" : document.get("info_comment", {}),
        "info_comment_Sent" : document.get("info_comment_Sent", {})
    }
    return extracted_data

def extract_data_one(document):
    prix_inr = document["price"] if "price" in document else "" 
    prixDollar = from_inr_to_dollar(prix_inr)
    extracted_data = {
        "name": document["name"] if "name" in document else "",
        #"price": document["price"] if "price" in document else "",
        # "image_table": list(document["img"]) if "img" in document else [],
        "price" : prixDollar,
        "rating": document["rating"] if "rating" in document else "",
        "description": document["description"] if "description" in document else [],
        "un_separated_comments": document["un_separated_comments"] if "un_separated_comments" in document else [],
        "info_comment" : document["info_comment"] if  "info_comment" in document else {},
        "info_comment_Sent" : document["info_comment_Sent"] if  "info_comment_Sent" in document else {}
    }
    return extracted_data

def ReturnOneDocFromAmazon(NbrDOC):
    cursor = collectiondb.find({}).limit(NbrDOC)
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

# def ReturnOneDocFromAmazon(NbrDOC):
#     cursor = colaliexpress.find({}).limit(NbrDOC)
#     # pprint.pprint(cursor.next())
#     nbrDoccoll = 0
#     if NbrDOC == 1 :
#         document = cursor.next()
#         # Extraire les données du document avec extract_data_one
#         # extracted_documents = extract_data_one(document)
#         extracted_documents = extract_data_one(document)
#         # extracted_documents = 0
#         # pprint.pprint(extracted_documents)
#         nbrDoccoll = 1
#     else:
#         extracted_documents = []
#         for document in cursor:
#             extracted_documents.append(extract_data(document))
#             nbrDoccoll += 1
#     # return extracted_documents, nbrDoc
#     # return nbrDoccoll, extracted_documents
#     return extracted_documents




# nbrDoccoll, all_documents = ReturnOneDocFromAliExpres(1)
# all_documents = ReturnOneDocFromAliExpres(0)
# all_documents = ReturnOneDocFromAliExpres(0)
# all_documents = ReturnOneDocFromAmazon(1)
# all_documents = dict(all_documents)
# print(all_documents[2]["un_separated_comments"][7]["imgs"])
# pprint.pprint(all_documents[2]["un_separated_comments"][7]["imgs"])
# print(all_documents[0]["price"])
# print(all_documents["price"])
# print(type(all_documents))
# print(all_documents.keys())
# print(nbrDoc)
# print(all_documents['un_separated_comments'][0]['comment'])
# print(nbrDoccoll)
# print(all_documents[3]["un_separated_comments"][0]["comment"])
# pprint.pprint(all_documents[1]["un_separated_comments"][0]["comment"])
# comment_type = type(all_documents[1]["un_separated_comments"][0]["comment"])
# print(comment_type)

# pprint.pprint(all_documents["un_separated_comments"])
# pprint.pprint(all_documents.un_separated_comments)
# print(all_documents["un_separated_comments"][3])

# print(all_documents[1]["un_separated_comments"][0]["comment"])
# print(all_documents[1][1]["rating"])
# print(all_documents["rating"])
# print(type(all_documents[1]["rating"]))
# pprint.pprint(all_documents)