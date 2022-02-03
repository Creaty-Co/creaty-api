from django.urls import path

from .views import *

urlpatterns = [
    path('', FormsView.as_view())
]
