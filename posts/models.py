from django.db import models


class Post(models.Model):
    user = models.ForeignKey("users.User",
                             verbose_name = "작성자",
                             on_delete = models.CASCADE)#유저 외래키
    title = models.CharField("제목", max_length= 30)
    complete = models.BooleanField("완료 여부", default=False)
    content = models.TextField("내용")
    created = models.DateTimeField("작성일시", auto_now_add = True)
    updated = models.DateTimeField("수정일시", auto_now=True)

    def __str__(self):
        return self.title

class PostImage(models.Model):
    post = models.ForeignKey(Post,
                             verbose_name = "포스트",
                             on_delete = models.CASCADE)
    photo = models.ImageField("사진", upload_to = "post")

class Comment(models.Model):
    user = models.ForeignKey("users.User",
                             verbose_name = "작성자",
                             on_delete = models.CASCADE)
    post = models.ForeignKey(Post,
                             verbose_name = "포스트",
                             on_delete = models.CASCADE)
    content = models.TextField("내용")
    created = models.DateTimeField("작성일시", auto_now_add = True)