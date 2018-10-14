from django import forms
from dockerapp.models import Dockerfile, Container

class DockerfileForm(forms.ModelForm):

    class Meta():
        model = Dockerfile
        fields = ('author','title','image_name','dockerfile_content')

        widgets = {
            'title':forms.TextInput(attrs={'class':'textinputclass'}),
        }


class ContainerForm(forms.ModelForm):

    class Meta():
        model = Container
        fields = ('dockerfile','title','port','container_public_port')

        widgets = {
            'title':forms.TextInput(attrs={'class':'textinputclass'}),
        }
