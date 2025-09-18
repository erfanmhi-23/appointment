from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
<<<<<<< HEAD
    path('doctors/', views.doctor_list, name='docto_list'),
=======
    path('doctors/', views.doctor_list, name='doctor_list'),
>>>>>>> origin/Erfan
    path('offices/', views.office_list, name='office_list'),
    path('doctor-search/', views.doctor_search, name='doctor_search'),
    path('timesheets/', views.timesheet_list, name='timesheet_list'),
    path('doctor/<int:doctor_id>/free-times/', views.doctor_free_times, name='doctor_free_times'),
    path('visit/<int:visit_id>/reserve/', views.reserve_visit_time, name='reserve_visit_time'),
    path('visit/<int:visit_id>/cancel/', views.cancel_visit_time, name='cancel_visit_time'),
    path('add/', views.add_doctor, name='add_doctor'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('doctor/<int:doctor_id>/', views.doctor_detail, name='doctor_detail'),


]