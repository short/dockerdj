from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views import generic
from dockerapp.models import Dockerfile, Container
from dockerapp.forms import DockerfileForm, ContainerForm
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
    redirect_field_name = 'dockerapp/containers.html'

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

class ContainerView(generic.ListView):
    model = Container

class CreateContainerView(LoginRequiredMixin, generic.edit.CreateView):
    login_url = 'dockerapp/login/'
    redirect_field_name = 'dockerapp/containers.html'

    form_class = ContainerForm

    model = Container

class ContainerDetail(SelectRelatedMixin, generic.DetailView):
    model = models.Container
    select_related = ("dockerfile",)

class DeleteContainer(LoginRequiredMixin, SelectRelatedMixin, generic.DeleteView):
    model = models.Container
    select_related = ("dockerfile",)
    success_url = reverse_lazy("dockerapp:containers")

    def get_queryset(self):
        # Get the object
        queryset = super().get_queryset()

        # get the specifik title and container id
        container_title = queryset.get().title
        container_id = queryset.get().container_id

        # stop and remove the container with the title and container id
        # os.system("docker container stop " + str(model.container_id))
        # os.system("docker container rm " + str(model.title))
        return queryset

    def delete(self, *args, **kwargs):
        messages.success(self.request, "Container Deleted")
        return super().delete(*args, **kwargs)

class StopContainer(LoginRequiredMixin, generic.RedirectView):
    model = models.Container

    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy("dockerapp:containers")

    def get(self, request, *args, **kwargs):
        # Get the object
        container = get_object_or_404(Container)

        # get the specifik title and container id
        container_id = container.container_id

        # stop and remove the container with the title and container id
        # os.system("docker container stop " + str(model.container_id))
        return super().get(request, *args, **kwargs)
