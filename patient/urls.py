from django.urls import path    
from patient.views import *
from doctors.views import reserve_visit_time , cancel_visit_time
urlpatterns = [
    path('shownobat/<int:Doc>', show_nobat ,name= 'show_nobat'),
    path('reserve_nobat/<int:Doc>' , reserve_nobat , name= 'reserve_nobat'),
    path('visit/<int:visit_id>/reserve/', reserve_visit_time, name='reserve_visit_time'),
    path('visit/<int:visit_id>/cancel/', cancel_visit_time, name='cancel_visit_time'),



]