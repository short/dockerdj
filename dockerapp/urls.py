from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

app_name = 'dockerapp'

urlpatterns = [
    url(r'login/$', auth_views.LoginView.as_view(template_name='dockerapp/login.html'), name='login'),
    url(r'logout/$', auth_views.LogoutView.as_view(template_name='dockerapp/logout.html'), name='logout'),
    url(r'container/$', views.ContainerView.as_view(), name='containers'),
    url(r'container/new$', views.CreateContainerView.as_view(),name='container_new'),
    url(r"container/(?P<pk>\d+)", views.ContainerDetail.as_view(),name="container_change"),
    url(r"container/delete/(?P<pk>\d+)",views.DeleteContainer.as_view(),name="container_delete"),
    url(r'dockerfile/$', views.DockerfileView.as_view(), name='dockerfiles'),
    url(r'dockerfile/new$', views.CreateDockerfileView.as_view(),name='dockerfile_new'),
    url(r"dockerfile/(?P<pk>\d+)", views.DockerfileDetail.as_view(),name="dockerfile_change"),
    url(r"dockerfile/delete/(?P<pk>\d+)",views.DeleteDockerfile.as_view(),name="dockerfile_delete"),
]
