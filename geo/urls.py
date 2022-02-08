from django.urls import path

from .views import *

urlpatterns = [
    path('languages/', GeoLanguagesView.as_view()),
    path('countries/', GeoCountriesView.as_view()),
]
