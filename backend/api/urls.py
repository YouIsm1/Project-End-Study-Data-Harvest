from .views import FormView, SendEmail
from django.urls import path

urlpatterns = [
    path('sear', FormView.as_view(), name='hello_world'),
    path('SendEmail', SendEmail.as_view(), name='SendEmail'),
    # path('sear', form_view, name='hello_world'),
]