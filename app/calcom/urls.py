from django.urls import path

from app.calcom.views.token import CalcomTokenView

urlpatterns = [path('token/', CalcomTokenView.as_view())]
