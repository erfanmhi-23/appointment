from django.urls import path    
from patient.views import *

urlpatterns = [
    path('shownobat/<int:Doc>', show_nobat ,name='show_nobat')




]