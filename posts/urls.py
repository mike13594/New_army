from django.urls import path
from posts import views

# 주소 comment_add, comment_delete, post_add, post_detail 맞춰봐야함
# edit,delete, complete는 detail 로 보내고 한 템플릿에서 하면 될듯함
urlpatterns = [
    path("", views.main),
    path("comment_add/", views.comment_add),
    path("comment_delete/<int:comment_id>/", views.comment_delete),
    path("post_list/", views.post_list),
    path("post_add/", views.post_add),
    path("<int:post_id>/", views.post_detail, name = "post_detail"),
    path("<int:post_id>/edit", views.post_edit, name = "post_edit"),
    path("<int:post_id>/delete", views.post_delete, name = "post_delete"),
    path("<int:post_id>/complete", views.post_complete, name = "post_complete"),
]