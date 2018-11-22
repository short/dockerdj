from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views import generic
from dockerapp.models import Dockerfile, ContainerByDockerFile, GitRepo, ContainerByImage
from dockerapp.forms import DockerfileForm, ContainerByDockerFileForm, GitRepoForm, ContainerByImageForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.conf import settings
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

class UpdateContainerByDockerFileContainer(LoginRequiredMixin, generic.RedirectView):
    model = models.ContainerByDockerFile

    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy("dockerapp:containers_dockerfile")

    def get(self, request, *args, **kwargs):
        container = get_object_or_404(ContainerByDockerFile)

        container_title = container.title
        container_containerid = container.container_id

        # Check for update with gitrepo id and update container if id changed
        commit_id = os.popen(str("git ls-remote " + container.gitrepo.url + " HEAD")).read()
        print(commit_id)

        if commit_id != container.gitrepo.last_commit_id:
            print("Update")

            try:
                container = models.ContainerByDockerFile.objects.filter(
                    title = container_title
                ).get()

                os.system("docker container stop " + str(container.container_id))
                os.system("docker container rm " + str(container.title))

                gitrepo_name = container.gitrepo.name

                gitrepo = models.GitRepo.objects.filter(
                    name = gitrepo_name
                ).get()

                gitrepo.last_commit_id = commit_id
                gitrepo.save()

                new_container = ContainerByDockerFile(dockerfile=container.dockerfile, title=container.title, port=container.port, container_port=container.container_port, container_public_port=container.container_public_port, gitrepo=container.gitrepo)
                new_container.save()
                models.ContainerByDockerFile.objects.filter(
                    container_id = container_containerid
                ).delete()

                dockerfilepath = new_container.dockerfile.dockerfile_path.replace("\\", "/")
                basedirectory = settings.BASE_DIR.replace("\\", "/")
                fulldirectory = str(basedirectory + dockerfilepath)
                print(fulldirectory)

                # Start the container
                os.system("docker login")
                os.system("docker build --no-cache -t " + new_container.title + " -f " + fulldirectory + " .")
                os.system("docker run --name " + new_container.title + " -d -p " + new_container.port + " " + new_container.dockerfile.title)
            except:
                messages.warning(
                    self.request,
                    "Update did not work"
                )
            else:
                messages.success(
                    self.request,
                    "Container succesfully updated"
                )
        else:
            print("Container up to date")

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
