from django.urls import path
from . import views
from review.views import add_comment


urlpatterns = [
    path('doctors/', views.doctor_list, name='doctor_list'),
    path('offices/', views.office_list, name='office_list'),
    path('doctor-search/', views.doctor_search, name='doctor_search'),
    path('timesheets/', views.timesheet_list, name='timesheet_list'),
    path('doctor/<int:doctor_id>/free-times/', views.doctor_free_times, name='doctor_free_times'),
    path('visit/<int:visit_id>/reserve/', views.reserve_visit_time, name='reserve_visit_time'),
    path('visit/<int:visit_id>/cancel/', views.cancel_visit_time, name='cancel_visit_time'),
    path('add/', views.add_doctor, name='add_doctor'),
    path('doctor/<int:doctor_id>/add-comment/', add_comment, name='add_comment'),
    path('doctor/<int:doctor_id>/', views.doctor_detail, name='doctor_detail'),
    
]