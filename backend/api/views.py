from bs4 import BeautifulSoup # type: ignore

from email.message import EmailMessage
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from django.core.mail import send_mail
from django.http import HttpResponse
from django.conf import settings

from email.message import EmailMessage
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings

from django.core.mail import EmailMessage

from .Applications import enregistrerdb as enrg
from .Applications import CollFromAmazon as ColAmaz
from .Applications import CollFromAliExpress as ColAliexp
from .Applications import CollFromEbay as ColEbay
from .Applications import ClusterCommentDict as ClsDic

from  .Applications import SelectCommentAliexpr as comm_exp
from  .Applications import SelectCommentAmaz as comm_amz
from  .Applications import SelectCommentEbay as comm_ebay
import subprocess
import os
from .scrappers import run_scrapers as ScrappersRunner

class FormView(APIView):
    def get(self, request):
        return Response({"message": "Hello, World!"})

    def post(self, request):
        searchpro = request.data.get("searchpro")
        if searchpro :
            if enrg.savedb([{'namePoduct' : searchpro}]) :
                #dans ce block on a ajouter main function pour afficher les resultats de la recherche
                           
                try:
                    ScrappersRunner.run()
                except subprocess.CalledProcessError as e:
                    return JsonResponse({
                        "message": f"Erreur lors de l'exécution du script: {e}"
                    })


                comm_amz.selectCommentsFromAmaz()
                comm_exp.selectCommentsFromAliex()
                comm_ebay.SelectCommentsFromEbay()

                dataFromAmazon = ColAmaz.ReturnOneDocFromAmazon(0)
                dataFromAliexpres = ColAliexp.ReturnOneDocFromAliExpres(0)
                dataFromEbay = ColEbay.ReturnOneDocFromEbay(0)

                listFunColl = [ColAmaz.ReturnOneDocFromAmazon, ColAliexp.ReturnOneDocFromAliExpres, ColEbay.ReturnOneDocFromEbay]
                listCollectionsDB = [ColAmaz.collectiondb, ColAliexp.colaliexpress, ColEbay.collection]
                for z, x in zip(listFunColl, listCollectionsDB):
                    ClsDic.DictClusterComment(z, x)
                dataFromAmazon = ColAmaz.ReturnOneDocFromAmazon(0)
                dataFromAliexpres = ColAliexp.ReturnOneDocFromAliExpres(0)
                dataFromEbay = ColEbay.ReturnOneDocFromEbay(0)

                return JsonResponse({
                    "searchpro": searchpro,
                    "dataFromAmazon" : dataFromAmazon,
                    "dataFromAliexpres" : dataFromAliexpres,
                    "dataFromEbay" : dataFromEbay,
                    "status": True,
                    "message": f"your product is {searchpro} are seved to database."
                    
                })
            else:
                return JsonResponse({
                    "searchpro": searchpro,
                    "message": f"your product is {searchpro} does not seved to database."
                })
        else :
            return JsonResponse({
                    # "searchpro": searchpro,
                    "message": f"re-send your product name"
                })

# class sendEmail(APIView):
#     def post(self, request):
#         if request.method == 'POST':
#             message = request.POST['message']
#             email = request.POST['email']
#             name = request.POST['name']

#             send_mail(
#                 'Contact Form',  # title
#                 message,  # message
#                 email,  # sender email
#                 ['elwafiyoussef82@gmail.com', 'youssefelwafi77@gmail.com'],  # recipients
#                 fail_silently=False
#             )
#         return JsonResponse({
#                     # "status": True,
#                     "message": f"Email sent successfully!"
#                 }) # Return some response after sending email

class SendEmail(APIView):
    def post(self, request):
        messagetext = request.data.get('message', '')
        email = request.data.get('email', '')
        subject = request.data.get('subject', '')
        username = request.data.get('username', '')
        message = f"Hello, this user : {username}\n sent from this email : {email},\n about subject : {subject},\n avec le message est : \n\n {messagetext}."

        # send_mail(
        #     subject,
        #     message,
        #     email,
        #     # settings.EMAIL_HOST_USER,
        #     ['elwafiyoussef82@gmail.com', 'youssefelwafi77@gmail.com'],
        #     # reply_to=email,
        #     fail_silently=False,
        # )

        # email=EmailMessage(
        #      subject,
        #      message,
        #      settings.EMAIL_HOST_USER,
        #      ['elwafiyoussef82@gmail.com', 'youssefelwafi77@gmail.com'],
        #      reply_to=[email],
        # )
        # email.send(fail_silently=False)

        # headers = {'Reply-To': reply_email}
        # msg = EmailMessage(subject, message, email, ['elwafiyoussef82@gmail.com', 'youssefelwafi77@gmail.com'], headers=headers)
        # msg.content_subtype = "html"
        # msg.send()

        # msg = EmailMessage(subject, message, settings.EMAIL_HOST_USER, ['elwafiyoussef82@gmail.com', 'youssefelwafi77@gmail.com'])
        # msg.reply_to = email  # Ajoutez l'adresse e-mail de l'expéditeur comme réponse à l'en-tête
        # msg.send()
        

        sendemail = EmailMessage(
            subject,
            message,
            email,
            # ['elwafiyoussef82@gmail.com', 'youssefelwafi77@gmail.com'],
            ['youssefelwafi77@gmail.com', 'ibizzikhalid19@gmail.com'],
            # ["bcc@example.com"],
            reply_to=[email],
            headers={"Message-ID": "foo"},
        )

        sendemail.send()

        if sendemail :
            return Response({"message": "Email sent successfully!"})
        else:
            return Response({"message": "erreur!"})


        
