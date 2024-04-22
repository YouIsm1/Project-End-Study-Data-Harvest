import pprint

from .CollFromAliExpress import colaliexpress, ReturnOneDocFromAliExpres
# import setup_database  as db


def selectCommentsFromAliex():
    dataFromAliExpres = ReturnOneDocFromAliExpres(0)

    # pprint.pprint(dataFromAliExpres[0]) # type: ignore
    # print(type(dataFromAliExpres))
    
    ListCommentProd = []
    
    for i in range(len(dataFromAliExpres)):
        prodComment = []
        prodCommentinfo = {}
        prodCommentinfo['nameProd'] = dataFromAliExpres[i]['name'] # type: ignore
        #pprint.pprint(dataFromAliExpres)
        for j in range(len(dataFromAliExpres[i]['un_separated_comments'])): # type: ignore
            if 'comment' in dataFromAliExpres[i]['un_separated_comments'][j]: # type: ignore
                comment = dataFromAliExpres[i]['un_separated_comments'][j]['comment'] # type: ignore
                # do something with the 'comment'
            else:
                # handle the case where the 'comment' key does not exist
                continue
            prodComment.append(comment)
        prodCommentinfo["listComment"] = prodComment
        ListCommentProd.append(prodCommentinfo)
    #
    for document in colaliexpress.find():
        for i in range(len(ListCommentProd)):
            if document["name"] == ListCommentProd[i]["nameProd"]: # type: ignore
                # Ajouter le dictionnaire des commentaires à l'attribut "info_comment" du document
                colaliexpress.update_one(
                    {"name": ListCommentProd[i]["nameProd"]}, # type: ignore
                    {"$set": {"info_comment": {"listComment": ListCommentProd[i]["listComment"], "name": ListCommentProd[i]["nameProd"]}}} # type: ignore
                )