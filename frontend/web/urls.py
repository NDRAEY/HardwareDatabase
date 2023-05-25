from django.urls import path
from . import views

urlpatterns = [
    path('', views.report),
    path('report', views.report),
    path('form_fill', views.form_fill)
]