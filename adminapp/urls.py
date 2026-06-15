from django.urls import path
from . import views

urlpatterns = [

    path('', views.dashboard, name='dashboard'),
    path('add/', views.add_resource, name='add_resource'),
    path('register/', views.admin_register, name='admin_register'),
    path('login/', views.admin_login, name='admin_login'),
    path('logout/', views.admin_logout, name='admin_logout'),
    path('edit/<int:id>/', views.edit_resource, name='edit_resource'),
    path('delete/<int:id>/', views.delete_resource, name='delete_resource'),
    path('student/delete/<int:id>/',views.delete_student,name='delete_student'),

]