from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django_filters.views import FilterView

from task_manager.models import Task
from task_manager.forms import TaskForm
from task_manager.tasks.filters import TaskFilter


class TaskListView(LoginRequiredMixin, FilterView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'
    filterset_class = TaskFilter


class TaskCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'form.html'
    success_url = reverse_lazy('tasks:tasks_list')
    success_message = 'Задача успешно создана'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'
    context_object_name = 'task'


class TaskUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'form.html'
    success_url = reverse_lazy('tasks:tasks_list')
    success_message = 'Задача успешно изменена'


class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = Task
    template_name = 'delete.html'
    success_url = reverse_lazy('tasks:tasks_list')
    success_message = 'Задача успешно удалена'

    def test_func(self):
        return self.request.user.pk == self.get_object().author.pk

from django.http import HttpResponse


def trigger_error(request):
    a = None
    a.method()  # Искусственная ошибка
    return HttpResponse("This will never be reached")
