from django.db import models
from django.utils import timezone
from django.urls import reverse

# Create your models here.
class Dockerfile(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    image_name = models.CharField(max_length=200)
    dockerfile_content = models.TextField()
    dockerfile = models.FileField(upload_to='dockerfiles/',blank=True)
    created_date = models.DateTimeField(default=timezone.now)

    def get_absolute_url(self):
        f = open(self.title + ".yml", "w+")
        f.write("FROM " + self.image_name + "\n")
        f.write(self.dockerfile_content)
        f.close()
        return reverse("dockerapp:dockerfiles")
        # return reverse("",kwargs={'pk':self.pk})

    def __str__(self):
        return self.title

class Container(models.Model):
    dockerfile = models.ForeignKey('dockerapp.Dockerfile', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    container_id = models.CharField(max_length=250, unique=True)

    def get_absolute_url(self):
        return reverse("dockerapp:containers")

    def __str__(self):
        return self.title
