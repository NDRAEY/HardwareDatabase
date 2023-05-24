from django.urls import path
from . import views

urlpatterns = [
    path('report', views.report),
    path('form_fill', views.form_fill)
]