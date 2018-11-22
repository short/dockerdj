from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

app_name = 'dockerapp'

urlpatterns = [
    url(r'login/$', auth_views.LoginView.as_view(template_name='dockerapp/login.html'), name='login'),
    url(r'logout/$', auth_views.LogoutView.as_view(template_name='dockerapp/logout.html'), name='logout'),
    url(r'container/bydockerfile/$', views.ContainerByDockerFileView.as_view(), name='containers_dockerfile'),
    url(r'container/bydockerfile/new$', views.CreateContainerByDockerFileView.as_view(),name='container_dockerfile_new'),
    url(r"container/bydockerfile/(?P<pk>\d+)", views.ContainerByDockerFileDetail.as_view(),name="container_dockerfile_change"),
    url(r"container/bydockerfile/update/(?P<pk>\d+)",views.UpdateContainerByDockerFileId.as_view(),name="container_bydockerfile_update"),
    url(r"container/bydockerfile/delete/(?P<pk>\d+)",views.DeleteContainerByDockerFile.as_view(),name="container_bydockerfile_delete"),
    url(r"container/bydockerfile/stop/(?P<pk>\d+)",views.StopContainerByDockerFile.as_view(),name="container_bydockerfile_stop"),
    url(r"container/bydockerfile/updatecontainer/(?P<pk>\d+)",views.UpdateContainerByDockerFileContainer.as_view(),name="container_bydockerfile_update_container"),
    url(r'dockerfile/$',views.DockerfileView.as_view(),name='dockerfiles'),
    url(r'dockerfile/new$',views.CreateDockerfileView.as_view(),name='dockerfile_new'),
    url(r"dockerfile/(?P<pk>\d+)",views.DockerfileDetail.as_view(),name="dockerfile_change"),
    url(r"dockerfile/delete/(?P<pk>\d+)",views.DeleteDockerfile.as_view(),name="dockerfile_delete"),
    url(r"gitrepo/$",views.GitRepoView.as_view(),name='gitrepos'),
    url(r"gitrepo/new$",views.CreateGitRepoView.as_view(),name='gitrepo_new'),
    url(r"gitrepo/(?P<pk>\d+)",views.GitRepoDetail.as_view(),name="gitrepo_change"),
    url(r"gitrepo/delete/(?P<pk>\d+)",views.DeleteGitRepo.as_view(),name="gitrepo_delete"),
    url(r'container/byimage/$', views.ContainerByImageView.as_view(), name='containers_image'),
    url(r'container/byimage/new$', views.CreateContainerByImageView.as_view(),name='container_image_new'),
    url(r"container/byimage/(?P<pk>\d+)", views.ContainerByImageDetail.as_view(),name="container_image_change"),
    url(r"container/byimage/update/(?P<pk>\d+)",views.UpdateContainerByImageId.as_view(),name="container_image_update"),
    url(r"container/byimage/delete/(?P<pk>\d+)",views.DeleteContainerByImage.as_view(),name="container_image_delete"),
    url(r"container/byimage/stop/(?P<pk>\d+)",views.StopContainerByImage.as_view(),name="container_image_stop"),
]
