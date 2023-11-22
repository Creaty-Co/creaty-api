from django.urls import path

from app.cal.views.token import CalTokenView

urlpatterns = [path('token/', CalTokenView.as_view())]
