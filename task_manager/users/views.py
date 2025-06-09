from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .forms import CustomUserCreationForm

User = get_user_model()


class UserListView(ListView):
    model = User
    template_name = 'users/user_list.html'
    context_object_name = 'users'


class UserCreateView(SuccessMessageMixin, CreateView):
    form_class = CustomUserCreationForm
    template_name = 'form.html'
    success_url = reverse_lazy('users:users_list')
    success_message = 'Пользователь успешно зарегистрирован'


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    template_name = 'form.html'
    fields = ['username', 'first_name', 'last_name']
    success_url = reverse_lazy('users:users_list')

    def test_func(self):
        return self.request.user.pk == self.get_object().pk


class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    template_name = 'delete.html'
    success_url = reverse_lazy('users:users_list')

    def test_func(self):
        return self.request.user.pk == self.get_object().pk