from django.urls import path, include
from users import views

app_name = "user"
urlpatterns = [
    # path("", views.profile, name = "profile"),
    path("logout/", views.logout_view, name = "logout"),
    path("login/", views.login_view, name = "login"),
    path("signup/", views.signup, name = "signup"),
]