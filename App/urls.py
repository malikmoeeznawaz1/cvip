from django.urls import path
from App import views

urlpatterns = [
    path("", views.home, name="home"), 
    path('upload/', views.upload, name='upload'),
    path('show_data/', views.show_data, name='show_data'),
]