from django.db import models
from seoul.models import Place
from django.contrib.auth.models import User

class Post(models.Model):
    user = models.ForeignKey("users.User",
                             verbose_name = "작성자",
                             on_delete = models.CASCADE)#유저 외래키
    place = models.ManyToManyField(Place, related_name='posts')
    title = models.CharField("제목", max_length= 30)
    content = models.TextField("내용")
    created = models.DateTimeField("작성일시", auto_now_add = True)
    updated = models.DateTimeField("수정일시", auto_now=True)

    def __str__(self):
        return self.title


class PlaceComplete(models.Model):
    user = models.ForeignKey("users.User",
                              on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    place = models.ForeignKey("seoul.Place", on_delete=models.CASCADE)
    complete = models.BooleanField(default=False)
    class Meta:
        unique_together=("user","post","place")


    def __str__(self):
        return f"{self.user} - {self.place} 완료 여부: {self.complete}"


class PostImage(models.Model):
    post = models.ForeignKey(Post,
                             verbose_name = "포스트",
                             on_delete = models.CASCADE)
    photo = models.ImageField("사진", upload_to = "post_images")
 

class Comment(models.Model):
    user = models.ForeignKey("users.User",
                             verbose_name = "작성자",
                             on_delete = models.CASCADE)
    post = models.ForeignKey(Post,
                             verbose_name = "포스트",
                             on_delete = models.CASCADE)
    content = models.TextField("내용")
    created = models.DateTimeField("작성일시", auto_now_add = True)