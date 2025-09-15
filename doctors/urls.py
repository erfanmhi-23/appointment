from django.urls import path
from . import views


urlpattern = [
    path('doctors/', views.doctor_list, name='docto_list'),
    path('offices/', views.office_list, name='office_list'),
    path('doctor-search/', views.doctor_search, name='doctor_search'),
    path('timesheets/', views.timesheet_list, name='timesheet_list'),
    path('doctor/<int:doctor_id>/free-times/', views.doctor_free_times, name='doctor_free_times'),
    path('visit/<int:visit_id>/reserve/', views.reserve_visit_time, name='reserve_visit_time'),
    path('visit/<int:visit_id>/cancel/', views.cancel_visit_time, name='cancel_visit_time'),
]