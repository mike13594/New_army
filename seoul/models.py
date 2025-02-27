from django.db import models

# Create your models here.
class Place(models.Model):
    name= models.CharField(max_length=100, unique=True, )
    district = models.CharField(max_length=10)
    place_image = models.ImageField(upload_to='place_images/')
    address= models.TextField("주소")
    description = models.TextField(null=True)

    def __str__(self):
        return self.name