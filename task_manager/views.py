from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import View


class HomePageView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'home.html')


class LoginUser(SuccessMessageMixin, LoginView):
    form_class = AuthenticationForm
    template_name = 'general/general_form.html'
    extra_context = {'title': _("Login"), 'button': _("Enter")}
    success_message = _('You were login')


class LogoutUser(View):

    def get(self, request, *args, **kwargs):
        logout(request)
        messages.info(request, _("You were logout"))
        return redirect(reverse_lazy('home'))
