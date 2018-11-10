from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views import generic
from dockerapp.models import Dockerfile, ContainerByDockerFile, GitRepo, ContainerByImage
from dockerapp.forms import DockerfileForm, ContainerByDockerFileForm, GitRepoForm, ContainerByImageForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
import os

from braces.views import SelectRelatedMixin
from . import models

# Create your views here.
class DockerfileView(generic.ListView):
    model = Dockerfile

class CreateDockerfileView(LoginRequiredMixin, generic.CreateView):
    login_url = 'dockerapp/login/'
    redirect_field_name = 'dockerapp/containerbydockerfile_list.html'

    form_class = DockerfileForm

    model = Dockerfile

class DockerfileDetail(SelectRelatedMixin, generic.DetailView):
    model = models.Dockerfile
    select_related = ("author",)

class DeleteDockerfile(LoginRequiredMixin, SelectRelatedMixin, generic.DeleteView):
    model = models.Dockerfile
    select_related = ("author",)
    success_url = reverse_lazy("dockerapp:dockerfiles")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def delete(self, *args, **kwargs):
        messages.success(self.request, "Dockerfile Deleted")
        return super().delete(*args, **kwargs)

class ContainerByDockerFileView(generic.ListView):
    model = ContainerByDockerFile

class CreateContainerByDockerFileView(LoginRequiredMixin, generic.CreateView):
    login_url = 'dockerapp/login/'
    redirect_field_name = 'dockerapp/containerbydockerfile_list.html'

    form_class = ContainerByDockerFileForm

    model = ContainerByDockerFile

class ContainerByDockerFileDetail(SelectRelatedMixin, generic.DetailView):
    model = models.ContainerByDockerFile
    select_related = ("dockerfile",)

class DeleteContainerByDockerFile(LoginRequiredMixin, SelectRelatedMixin, generic.DeleteView):
    model = models.ContainerByDockerFile
    select_related = ("dockerfile",)
    success_url = reverse_lazy("dockerapp:containers_dockerfile")

    def get_queryset(self):
        # Get the object
        queryset = super().get_queryset()

        # get the specifik title and container id
        container_title = queryset.get().title
        container_id = queryset.get().container_id
        container_stopped = queryset.get().container_stopped

        print(container_title)
        print(container_id)

        # stop and remove the container with the title and container id
        if container_stopped != '1':
            os.system("docker container stop " + str(container_id))

        os.system("docker container rm " + str(container_title))
        return queryset

    def delete(self, *args, **kwargs):
        messages.success(self.request, "Container Deleted")
        return super().delete(*args, **kwargs)

class StopContainerByDockerFile(LoginRequiredMixin, generic.RedirectView):
    model = models.ContainerByDockerFile

    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy("home")

    def get(self, request, *args, **kwargs):
        # Get the object
        container = get_object_or_404(ContainerByDockerFile)

        # get the container title
        container_title = container.title

        # stop and remove the container with the title and container id
        os.system("docker container stop " + str(container.container_id))

        try:
            container = models.ContainerByDockerFile.objects.filter(
                title = container_title
            ).get()

            container.container_stopped = 1
            container.save()
        except:
            messages.warning(
                self.request,
                "Container did not stop"
            )
        else:
            messages.success(
                self.request,
                "Container stopped"
            )

        return super().get(request, *args, **kwargs)

class UpdateContainerByDockerFileId(LoginRequiredMixin, generic.RedirectView):
    model = models.ContainerByDockerFile

    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy("dockerapp:containers_dockerfile")

    def get(self, request, *args, **kwargs):
        # Get the object
        container = get_object_or_404(ContainerByDockerFile)

        # get the container title
        container_title = container.title

        try:
            container = models.ContainerByDockerFile.objects.filter(
                title = container_title
            ).get()

            container_id = os.popen(str("docker inspect --format="+"{"+"{"+".Id"+"}"+"} " + container.title)).read()
            container_port_command = os.popen(str("docker port " + container_id)).read()

            # get the ip address
            number = 0
            for word in container_port_command.split():
                number += 1
                if number == 3:
                    container_port = word

            container.container_id = container_id
            container.container_port = container_port
            container.save()
        except:
            messages.warning(
                self.request,
                "Update did not work"
            )
        else:
            messages.success(
                self.request,
                "Container id succesfully updated"
            )
        return super().get(request, *args, **kwargs)

class GitRepoView(generic.ListView):
    model = GitRepo

class CreateGitRepoView(LoginRequiredMixin, generic.CreateView):
    login_url = 'dockerapp/login/'
    redirect_field_name = 'dockerapp/gitrepo_list.html'

    form_class = GitRepoForm

    model = GitRepo


class GitRepoDetail(SelectRelatedMixin, generic.DetailView):
    model = models.GitRepo
    select_related = ()

class DeleteGitRepo(LoginRequiredMixin, SelectRelatedMixin, generic.DeleteView):
    model = models.GitRepo
    select_related = ()
    success_url = reverse_lazy("dockerapp:gitrepos")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def delete(self, *args, **kwargs):
        messages.success(self.request, "Gitrepo Deleted")
        return super().delete(*args, **kwargs)

class ContainerByImageView(generic.ListView):
    model = ContainerByImage

class CreateContainerByImageView(LoginRequiredMixin, generic.CreateView):
    login_url = 'dockerapp/login/'
    # redirect_field_name = 'dockerapp/containerbyimage_list.html'

    form_class = ContainerByImageForm

    model = ContainerByImage

class ContainerByImageDetail(SelectRelatedMixin, generic.DetailView):
    model = models.ContainerByImage
    select_related = ()

class UpdateContainerByImageId(LoginRequiredMixin, generic.RedirectView):
    model = models.ContainerByImage

    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy("dockerapp:containers_image")

    def get(self, request, *args, **kwargs):
        # Get the object
        container = get_object_or_404(ContainerByImage)

        # get the container title
        container_name = container.name

        try:
            container = models.ContainerByImage.objects.filter(
                name = container_name
            ).get()

            container_id = os.popen(str("docker inspect --format="+"{"+"{"+".Id"+"}"+"} " + container.name)).read()
            container_port_command = os.popen(str("docker port " + container_id)).read()

            # get the ip address
            number = 0
            for word in container_port_command.split():
                number += 1
                if number == 3:
                    container_port = word

            container.container_id = container_id
            container.container_port = container_port
            container.save()
        except:
            messages.warning(
                self.request,
                "Update did not work"
            )
        else:
            messages.success(
                self.request,
                "Container id succesfully updated"
            )
        return super().get(request, *args, **kwargs)

class DeleteContainerByImage(LoginRequiredMixin, SelectRelatedMixin, generic.DeleteView):
    model = models.ContainerByImage
    select_related = ()
    success_url = reverse_lazy("dockerapp:containers_image")

    def get_queryset(self):
        # Get the object
        queryset = super().get_queryset()

        # get the specifik title and container id
        container_name = queryset.get().name
        container_id = queryset.get().container_id
        container_stopped = queryset.get().container_stopped

        # print(container_title)
        # print(container_id)

        # stop and remove the container with the title and container id
        if container_stopped != '1':
            os.system("docker container stop " + str(container_id))

        os.system("docker container rm " + str(container_name))
        return queryset

    def delete(self, *args, **kwargs):
        messages.success(self.request, "Container Deleted")
        return super().delete(*args, **kwargs)

class StopContainerByImage(LoginRequiredMixin, generic.RedirectView):
    model = models.ContainerByImage

    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy("home")

    def get(self, request, *args, **kwargs):
        # Get the object
        container = get_object_or_404(ContainerByImage)

        # get the container title
        container_name = container.name

        # stop and remove the container with the title and container id
        os.system("docker container stop " + str(container.container_id))

        try:
            container = models.ContainerByImage.objects.filter(
                name = container_name
            ).get()

            container.container_stopped = 1
            container.save()
        except:
            messages.warning(
                self.request,
                "Container did not stop"
            )
        else:
            messages.success(
                self.request,
                "Container stopped"
            )

        return super().get(request, *args, **kwargs)
