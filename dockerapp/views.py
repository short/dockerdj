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

class CreateContainerView(LoginRequiredMixin, generic.CreateView):
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
        os.system("docker container stop " + str(container_id))
        os.system("docker container rm " + str(container_title))
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

        # get the container title
        container_title = container.title

        # stop and remove the container with the title and container id
        os.system("docker container stop " + str(container.container_id))

        try:
            container = models.Container.objects.filter(
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

class UpdateContainerId(LoginRequiredMixin, generic.RedirectView):
    model = models.Container

    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy("dockerapp:containers")

    def get(self, request, *args, **kwargs):
        # Get the object
        container = get_object_or_404(Container)

        # get the container title
        container_title = container.title

        try:
            container = models.Container.objects.filter(
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
