from django.db import models
from django.utils import timezone
from django.urls import reverse
import os

# Create your models here.
class Dockerfile(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    image_name = models.CharField(max_length=200)
    dockerfile_content = models.TextField()
    dockerfile = models.FileField(upload_to='media/dockerfiles/',blank=True)
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
    port = models.CharField(max_length=20)
    container_id = models.CharField(max_length=250)

    def get_absolute_url(self):
        # file = open(self.dockerfile + ".yml", "r")

        # Start the container
        os.system("docker login")
        # os.system("docker build -t " + self.title + " " + str(self.dockerfile) + ".yml")
        os.system("docker run --name " + self.title + " -d -p 80:80 " + self.title)
        # print('container id is')
        # print(os.system(str("docker inspect --format="+"{"+"{"+".Id"+"}"+"} " + self.title)))
        return reverse("dockerapp:containers")

    def __str__(self):
        return self.title
