from django.contrib import admin
from dockerapp.models import Dockerfile, ContainerByDockerFile, ContainerByImage, GitRepo, Swarm

# Register your models here.
admin.site.register(Dockerfile)
admin.site.register(ContainerByDockerFile)
admin.site.register(ContainerByImage)
admin.site.register(GitRepo)
admin.site.register(Swarm)
