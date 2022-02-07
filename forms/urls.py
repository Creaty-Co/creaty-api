from django.urls import path

from .views import *

urlpatterns = [
    path('', FormsView.as_view()),
    # TODO: #38
    path('<int:form_id>/applications/', FormApplicationsView.as_view())
]
