from django.urls import path, include
from users import views

app_name = "user"
urlpatterns = [
    path("login/", views.login_view, name = "login"),
    path("logout/", views.logout_view, name = "logout"),        
    path("profile/", views.profile, name = "profile"),
    path("signup/", views.signup, name = "signup"),
    path("profile/<int:user_id>/edit/", views.profile_edit, name = "edit"),
    path("profile/<int:user_id>/delete/", views.profile_delete, name = "delete"),
]