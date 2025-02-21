from django.urls import path, include
from seoul import views

urlpatterns = [
    path("", views.places),
]