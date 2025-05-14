from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect
from django.contrib import messages

from task_manager.models import Label


class LabelListView(LoginRequiredMixin, ListView):
    model = Label
    template_name = 'labels/label_list.html'
    context_object_name = 'labels'


class LabelCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Label
    template_name = 'form.html'
    fields = ['name']
    success_url = reverse_lazy('labels:labels_list')
    success_message = 'Метка успешно создана'


class LabelUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Label
    template_name = 'form.html'
    fields = ['name']
    success_url = reverse_lazy('labels:labels_list')
    success_message = 'Метка успешно изменена'


class LabelDeleteView(LoginRequiredMixin, DeleteView):
    model = Label
    template_name = 'delete.html'
    success_url = reverse_lazy('labels:labels_list')
    success_message = 'Метка успешно удалена'

    def form_valid(self, form):
        if self.get_object().task_set.exists():
            messages.error(self.request, 'Невозможно удалить метку, связанную с задачами')
            return redirect('labels:labels_list')
        messages.success(self.request, self.success_message)
        return super().form_valid(form)
