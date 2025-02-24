from django.db import models


class Post(models.Model):
    user = models.ForeignKey("users.User",
                             verbose_name = "작성자",
                             on_delete = models.CASCADE)#유저 외래키
    place = models.ManyToManyField("장소", related_name='related_posts')
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