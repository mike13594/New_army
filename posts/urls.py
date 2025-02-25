from django.urls import path
from posts import views


# edit,delete, complete는 detail 로 보내고 한 템플릿에서 하면 될듯함
urlpatterns = [
    path("", views.main, name= "main"),
    path("<int:post_id>/comment_add/", views.comment_add, name="comment_add"),
    path("<int:comment_id>/comment_delete/", views.comment_delete, name="comment_delete"),
    path("post_create/", views.post_create, name="post_create"),
    path("<int:post_id>/", views.post_detail, name = "post_detail"),
    path("<int:post_id>/edit/", views.post_edit, name = "post_edit"),
    path("<int:post_id>/delete/", views.post_delete, name = "post_delete"),
    path("<int:post_id>/<int:place_id>/complete/", views.place_complete, name="place_complete"),
    path("<int:post_id>/<int:place_id>/uncomplete/", views.place_uncomplete, name="place_uncomplete"), 
]
