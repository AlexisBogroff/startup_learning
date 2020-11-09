from django.urls import path
from . import views
from .models import *

urlpatterns = [
    path('',views.new_question ),
    path('test', views.test),
]
