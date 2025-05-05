from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

User = get_user_model()


class UserListView(ListView):
    model = User
    template_name = 'users/user_list.html'
    context_object_name = 'users'


class UserCreateView(CreateView):
    model = User
    template_name = 'users/user_form.html'
    fields = ['username', 'first_name', 'last_name', 'password']
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        return super().form_valid(form)


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    template_name = 'users/user_form.html'
    fields = ['username', 'first_name', 'last_name']
    success_url = reverse_lazy('users:index')

    def test_func(self):
        return self.request.user.pk == self.get_object().pk


class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('users:index')

    def test_func(self):
        return self.request.user.pk == self.get_object().pk
    