import pprint
from nltk.sentiment.vader import SentimentIntensityAnalyzer

from .CollFromAmazon import ReturnOneDocFromAmazon, collectiondb
from .CollFromAliExpress import ReturnOneDocFromAliExpres, colaliexpress
from .CollFromEbay import ReturnOneDocFromEbay, collection

def DictClusterComment(Collfunction, collectionsDB):

    data = Collfunction(0)
    for k in range(len(data)): # type: ignore
        ClusterCommentDict = {}
        dicPost = {}
        dicNegt = {}
        positvCommentList = []
        negatvCommentList = []

        ListText = data[k]['info_comment']['listComment']
        name = data[k]['info_comment']['name']
        # print(f"\n {k} name is  : {name} \n")

        # Sentiment Analysis
        sid = SentimentIntensityAnalyzer()
        for i in ListText:
            pol = sid.polarity_scores(i)['compound']
            if pol > 0 :
               positvCommentList.append(i) 
            elif pol < 0 :
                negatvCommentList.append(i)

        nbrComtPost = len(positvCommentList)
        nbrComtNegtv = len(negatvCommentList)

        dicPost["nbrComPost"] = nbrComtPost
        dicPost["listCommPost"] = positvCommentList

        dicNegt["nbrComNegt"] = nbrComtNegtv
        dicNegt["listCommNegt"] = negatvCommentList

        ClusterCommentDict["name"] = name
        ClusterCommentDict["dicPost"] = dicPost
        ClusterCommentDict["dicNegt"] = dicNegt

        collectionsDB.update_one(
            {"name": ClusterCommentDict["name"]}, # type: ignore
            {"$set": {"info_comment_Sent": ClusterCommentDict}} # type: ignore
        )


    # return ClusterCommentDict

#listFunColl = [ReturnOneDocFromAmazon, ReturnOneDocFromAliExpres, ReturnOneDocFromEbay]
#listCollectionsDB = [collectiondb, colaliexpress, collection]
#        
## listFunColl = [ReturnOneDocFromAmazon]
## listCollectionsDB = [collectiondb]
#
#for z, x in zip(listFunColl, listCollectionsDB):
#    DictClusterComment(z, x)


# pprint.pprint(ClusterCommentDict)