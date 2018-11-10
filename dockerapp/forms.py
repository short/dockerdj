from django import forms
from dockerapp.models import Dockerfile, ContainerByDockerFile, GitRepo, ContainerByImage

class DockerfileForm(forms.ModelForm):

    class Meta():
        model = Dockerfile
        fields = ('author','title','image_name','dockerfile_content')

        widgets = {
            'title':forms.TextInput(attrs={'class':'textinputclass'}),
        }


class ContainerByDockerFileForm(forms.ModelForm):

    # dockerfile = forms.ChoiceField(required=False)

    class Meta():
        model = ContainerByDockerFile
        fields = ('dockerfile','title','port','container_public_port')

        widgets = {
            'title':forms.TextInput(attrs={'class':'textinputclass'}),
        }

class GitRepoForm(forms.ModelForm):

    class Meta():
        model = GitRepo
        fields = ('name','url','Description')

        widgets = {
            'title':forms.TextInput(attrs={'class':'textinputclass'}),
        }

class ContainerByImageForm(forms.ModelForm):

    # dockerfile = forms.ChoiceField(required=False)

    class Meta():
        model = ContainerByImage
        fields = ('name','port','container_public_port')

        widgets = {
            'title':forms.TextInput(attrs={'class':'textinputclass'}),
        }
