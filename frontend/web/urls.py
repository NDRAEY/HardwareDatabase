from django.urls import path
from . import views

urlpatterns = [
    path('', views.report),
    path('report', views.report),
    path('cmd', views.command),
]