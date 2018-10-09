from django.shortcuts import render
from django.views.generic import TemplateView, ListView, CreateView
from dockerapp.models import Dockerfile, Container
from dockerapp.forms import DockerfileForm, ContainerForm
from django.contrib.auth.mixins import LoginRequiredMixin
import os

# Create your views here.

class DockerfileView(ListView):
    model = Dockerfile

class CreateDockerfileView(LoginRequiredMixin, CreateView):
    login_url = 'dockerapp/login/'
    redirect_field_name = 'dockerapp/containers.html'

    form_class = DockerfileForm

    model = Dockerfile

class ContainerView(ListView):
    model = Container

class CreateContainerView(LoginRequiredMixin, CreateView):
    login_url = 'dockerapp/login/'
    redirect_field_name = 'dockerapp/containers.html'

    form_class = ContainerForm

    model = Container

    # os.system("docker build -t " + Container.title + " " + Container.dockerfile)
    # os.system("docker run -d " + Container.title)
