from django.urls import path
from . import views
from review.views import add_comment


urlpatterns = [
    path('doctors/', views.doctor_list, name='doctor_list'),
    path('offices/', views.office_list, name='office_list'),
    path('doctor-search/', views.doctor_search, name='doctor_search'),
    path('timesheets/', views.timesheet_list, name='timesheet_list'),
    path('office/<int:office_id>/', views.office_detail, name='office_detail'),
    path('doctor/<int:doctor_id>/free-times/', views.doctor_free_times, name='doctor_free_times'),
    path('visit/<int:doctor_id>/reserve/', views.reserve_visit_time, name='reserve_visit_time'),
    path('visit/<int:visit_id>/cancel/', views.cancel_visit_time, name='cancel_visit_time'),
    path('add/', views.add_doctor, name='add_doctor'),
    path('office/<int:office_id>/edit/office', views.office_edit, name='office_edit'),
    path('office/<int:timesheet_id>/edit/timesheet', views.timesheet_edit, name='timesheet_edit'),
    path('doctor/<int:doctor_id>/add-comment/', add_comment, name='add_comment'),
    path('doctor/<int:doctor_id>/', views.doctor_detail, name='doctor_detail'),
    path('showtimesheet/<int:doctor_id>/' , views.available_times_for_doctor, name='show_timesheet'),
    path("near-doctor/", views.near_doctor, name="near_doctor"),
]