from django.urls import path    
from . import views

urlpatterns = [
        path('doctor/<int:doctor_id>/add-comment/', views.add_comment, name='add_comment'),
]