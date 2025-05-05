from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _

from .models import Status


class StatusListView(LoginRequiredMixin, ListView):
    model = Status
    template_name = 'statuses/status_list.html'
    context_object_name = 'statuses'


class StatusCreateView(LoginRequiredMixin, CreateView):
    model = Status
    fields = ['name']
    template_name = 'statuses/status_form.html'
    success_url = reverse_lazy('statuses_list')

    def form_valid(self, form):
        messages.success(self.request, _('Status created successfully'))
        return super().form_valid(form)


class StatusUpdateView(LoginRequiredMixin, UpdateView):
    model = Status
    fields = ['name']
    template_name = 'statuses/status_form.html'
    success_url = reverse_lazy('statuses_list')

    def form_valid(self, form):
        messages.success(self.request, _('Status updated successfully'))
        return super().form_valid(form)


class StatusDeleteView(LoginRequiredMixin, DeleteView):
    model = Status
    template_name = 'statuses/status_confirm_delete.html'
    success_url = reverse_lazy('statuses_list')

    def form_valid(self, form):
        # Пока не реализована проверка на связь с задачей
        messages.success(self.request, _('Status deleted successfully'))
        return super().form_valid(form)