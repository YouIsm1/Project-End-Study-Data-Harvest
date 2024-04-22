import pprint

# import setup_database  as db
from .CollFromAmazon import ReturnOneDocFromAmazon, collectiondb

def selectCommentsFromAmaz():
    datafromamazon = ReturnOneDocFromAmazon(0)
    # pprint.pprint(datafromamazon)
    
    # print(type(datafromamazon))
    # pprint.pprint(datafromamazon[0]['un_separated_comments'][0]) # type: ignore
    
    ListCommentProd = []
    
    for i in range(len(datafromamazon)):
        prodComment = []
        prodCommentinfo = {}
        prodCommentinfo['nameProd'] = datafromamazon[i]['name'] # type: ignore
        for j in range(len(datafromamazon[i]['un_separated_comments'])): # type: ignore
            if 'comment' in datafromamazon[i]['un_separated_comments'][j]: # type: ignore
                comment = datafromamazon[i]['un_separated_comments'][j]['comment'] # type: ignore
                # do something with the 'comment'
            else:
                # handle the case where the 'comment' key does not exist
                continue
            prodComment.append(comment)
        prodCommentinfo["listComment"] = prodComment
        ListCommentProd.append(prodCommentinfo)
    
    # pprint.pprint(ListCommentProd[0])
    # print(len(ListCommentProd))
    # print(len(ListCommentProd[0]))
    
    # print(len(datafromamazon))
    # print(len(datafromamazon[0]['un_separated_comments']))
    
    # Boucle à travers les données des commentaires
    for document in collectiondb.find():
        for i in range(len(ListCommentProd)):
            if document["name"] == ListCommentProd[i]["nameProd"]: # type: ignore
                # Ajouter le dictionnaire des commentaires à l'attribut "info_comment" du document
                collectiondb.update_one(
                    {"name": ListCommentProd[i]["nameProd"]}, # type: ignore
                    {"$set": {"info_comment": {"listComment": ListCommentProd[i]["listComment"], "name": ListCommentProd[i]["nameProd"]}}} # type: ignore
                )