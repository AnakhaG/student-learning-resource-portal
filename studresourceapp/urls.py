from django.urls import path
from . import views

urlpatterns = [

    path('', views.login_view, name='index'),

    path('home/', views.home, name='home'),

    path('signup/', views.signup, name='signup'),

    path('login/', views.login_view, name='login'),

    path('logout/', views.logout_view, name='logout'),

    path('about/', views.about, name='about'),

    path('contact/', views.contact, name='contact'),

    path('profile/', views.profile, name='profile'),
    
    path('download/<int:id>/',views.download_resource,name='download_resource'),
    

]