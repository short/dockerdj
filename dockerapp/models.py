from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.conf import settings
import os, os.path, subprocess

# Create your models here.
class Dockerfile(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    image_name = models.CharField(max_length=200)
    dockerfile = models.FileField(upload_to='dockerfiles/%Y/%m/%d/%H-%M-%S',blank=True)
    dockerfile_path = models.CharField(max_length=500)
    created_date = models.DateTimeField(default=timezone.now)

    def get_absolute_url(self):
        print(self.dockerfile.path.split('dockerdj', 1)[-1])
        self.dockerfile_path = self.dockerfile.path.split('dockerdj', 1)[-1]
        self.save()
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
    gitrepo = models.ForeignKey('dockerapp.GitRepo', on_delete=models.CASCADE, blank=True, null=True)

    def get_absolute_url(self):
        dockerfilepath = self.dockerfile.dockerfile_path.replace("\\", "/")
        basedirectory = settings.BASE_DIR.replace("\\", "/")
        fulldirectory = str(basedirectory + dockerfilepath)
        print(fulldirectory)

        # Start the container
        os.system("docker login")
        os.system("docker build --no-cache -t " + self.title + " -f " + fulldirectory + " .")
        os.system("docker run --name " + self.title + " -d -p " + self.port + " " + self.dockerfile.title)

        return reverse("dockerapp:containers_dockerfile")

    def __str__(self):
        return self.title

class GitRepo(models.Model):
    name = models.CharField(max_length=250)
    url = models.CharField(max_length=500)
    Description = models.TextField()
    last_commit_id = models.CharField(max_length=250)

    def get_absolute_url(self):
        #Get last id token to check if application is up to date
        self.last_commit_id = os.popen(str("git ls-remote " + self.url + " HEAD")).read()
        self.save()

        return reverse("dockerapp:gitrepos")

    def __str__(self):
        return self.name

class Swarm(models.Model):
    name = models.CharField(max_length=200)
    container_amount = models.PositiveIntegerField()

    def get_absolute_url(self):
        #swarm code here


        return reverse("index.html")    #change redirection path!

    def __str__(self):
        return self.name
