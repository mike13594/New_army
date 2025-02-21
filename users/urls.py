from django.urls import path, include
from users import views

urlpatterns = [
    path("", views.profile, name = "profile"),
    path("login/", views.login_view, name = "login"),
    path("logout/", views.logout_view),
    path("signup/", views.signup, name = "signup"),
]