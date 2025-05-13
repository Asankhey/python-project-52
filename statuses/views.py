from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .models import Status


class StatusListView(LoginRequiredMixin, ListView):
    model = Status
    template_name = 'statuses/status_list.html'
    context_object_name = 'statuses'


class StatusCreateView(LoginRequiredMixin, CreateView):
    model = Status
    fields = ['name']
    template_name = 'form.html'
    success_url = reverse_lazy('statuses:statuses_list')

    def form_valid(self, form):
        messages.success(self.request, 'Статус успешно создан')
        return super().form_valid(form)


class StatusUpdateView(LoginRequiredMixin, UpdateView):
    model = Status
    fields = ['name']
    template_name = 'form.html'
    success_url = reverse_lazy('statuses:statuses_list')

    def form_valid(self, form):
        messages.success(self.request, 'Статус успешно изменён')
        return super().form_valid(form)


class StatusDeleteView(LoginRequiredMixin, DeleteView):
    model = Status
    template_name = 'delete.html'
    success_url = reverse_lazy('statuses:statuses_list')

    def form_valid(self, form):
        messages.success(self.request, 'Статус успешно удалён')
        return super().form_valid(form)
