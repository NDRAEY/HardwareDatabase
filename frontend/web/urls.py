from django.urls import path
from . import views

urlpatterns = [
    path('', views.report),
    path('print', views.print_version),
    path('cmd', views.command),
    path('employees', views.employees),
]