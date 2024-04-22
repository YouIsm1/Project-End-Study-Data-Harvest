import pprint

from .CollFromEbay import collection, ReturnOneDocFromEbay

def SelectCommentsFromEbay():
    dataFromEbay = ReturnOneDocFromEbay(0)

    # print(type(dataFromEbay))
    # pprint.pprint(dataFromEbay[0]) # type: ignore
    
    ListCommentProd = []
    
    for i in range(len(dataFromEbay)):
        prodComment = []
        prodCommentinfo = {}
        prodCommentinfo['nameProd'] = dataFromEbay[i]['name'] # type: ignore
        for j in range(len(dataFromEbay[i]['un_separated_comments'])): # type: ignore
            if 'comment' in dataFromEbay[i]['un_separated_comments'][j]: # type: ignore
                comment = dataFromEbay[i]['un_separated_comments'][j]['comment'] # type: ignore
                # do something with the 'comment'
            else:
                # handle the case where the 'comment' key does not exist
                continue
            prodComment.append(comment)
        prodCommentinfo["listComment"] = prodComment
        ListCommentProd.append(prodCommentinfo)
    
    for document in collection.find():
        for i in range(len(ListCommentProd)):
            if document["name"] == ListCommentProd[i]["nameProd"]: # type: ignore
                # Ajouter le dictionnaire des commentaires à l'attribut "info_comment" du document
                collection.update_one(
                    {"name": ListCommentProd[i]["nameProd"]}, # type: ignore
                    {"$set": {"info_comment": {"listComment": ListCommentProd[i]["listComment"], "name": ListCommentProd[i]["nameProd"]}}} # type: ignore
                )