from django.urls import path
from . import views
urlpatterns = [
    path('', views.Index, name='index'),
    path('about/', views.About, name='about'),
    path('contact/', views.contact, name='contact'),
    path('program/', views.Programs, name='program'),



]
