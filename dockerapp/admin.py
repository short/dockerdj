from django.contrib import admin
from dockerapp.models import Dockerfile, Container

# Register your models here.
admin.site.register(Dockerfile)
admin.site.register(Container)
