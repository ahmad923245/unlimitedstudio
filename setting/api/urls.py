from .views import *
from django.urls import path

urlpatterns = [

    path('<str:page_type>/', StaticPageHtml, name='pages'),
]