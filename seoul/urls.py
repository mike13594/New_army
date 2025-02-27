from django.urls import path, include
from seoul import views

app_name = "seoul"
urlpatterns = [
    path("", views.place_list, name="place_list"),
    path("<int:place_id>/", views.place_detail, name="place_detail"),
]