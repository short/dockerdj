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

    def __str__(self):
        return self.title

class ContainerByImage(models.Model):
    name = models.CharField(max_length=200)
    port = models.CharField(max_length=20)
    container_id = models.CharField(max_length=250)
    container_stopped = models.CharField(max_length=1)
    container_port = models.CharField(max_length=250)
    container_public_port = models.CharField(max_length=20)

    def get_absolute_url(self):
        os.system("docker login")
        os.system("docker run --name " + self.name + " -d -p " + self.port + " " + self.name)
        return reverse("dockerapp:containers_image")

    def __str__(self):
        return self.name

class ContainerByDockerFile(models.Model):
    dockerfile = models.ForeignKey('dockerapp.Dockerfile', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    port = models.CharField(max_length=20)
    container_id = models.CharField(max_length=250)
    container_stopped = models.CharField(max_length=1)
    container_port = models.CharField(max_length=250)
    container_public_port = models.CharField(max_length=20)

    def get_absolute_url(self):
        # file = open(self.dockerfile + ".yml", "r")

        # Start the container
        os.system("docker login")
        os.system("docker build -t " + self.title + " " + self.title + ".yml")
        os.system("docker run --name " + self.title + " -d -p " + self.port + " " + self.title)
        return reverse("dockerapp:containers_dockerfile")

    def __str__(self):
        return self.title

class GitRepo(models.Model):
    name = models.CharField(max_length=250)
    url = models.CharField(max_length=500)
    Description = models.TextField()
    last_commit_id = models.CharField(max_length=250)

    def get_absolute_url(self):
        return reverse("dockerapp:gitrepos")

    #Get last id token to check if application is up to date

    def __str__(self):
        return self.name

class Swarm(models.Model):
    name = models.CharField(max_length=200)
    container_amount = models.PositiveIntegerField()

    def get_absolute_url(self):
        #swarm code here
        return reverse("index.html")

    def __str__(self):
        return self.name
