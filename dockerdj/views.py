from django.views.generic import TemplateView

class LoginRedPage(TemplateView):
    template_name = 'loggedin.html'

class LogoutRedPage(TemplateView):
    template_name = 'loggedout.html'

class HomePage(TemplateView):
    template_name = 'index.html'
