from django.urls import path    
from . import views
from .views import add_comment

urlpatterns = [
    path('doctor/<int:doctor_id>/add-comment/', add_comment, name='add_comment'),
]