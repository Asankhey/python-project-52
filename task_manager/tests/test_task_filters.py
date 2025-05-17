from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from task_manager.models import Task, Status, Label

User = get_user_model()


class TaskFilterTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='author', password='pass')
        self.executor = User.objects.create_user(username='executor', password='pass')
        self.status = Status.objects.create(name='В работе')
        self.label = Label.objects.create(name='bug')
        self.task = Task.objects.create(
            name='Test task',
            description='Test description',
            status=self.status,
            author=self.user,
            executor=self.executor,
        )
        self.task.labels.add(self.label)
        self.client.force_login(self.user)

    def test_filter_by_status(self):
        response = self.client.get(reverse('tasks:tasks_list'), {'status': self.status.id})
        self.assertContains(response, self.task.name)

    def test_filter_by_executor(self):
        response = self.client.get(reverse('tasks:tasks_list'), {'executor': self.executor.id})
        self.assertContains(response, self.task.name)

    def test_filter_by_label(self):
        response = self.client.get(reverse('tasks:tasks_list'), {'labels': self.label.id})
        self.assertContains(response, self.task.name)

    def test_filter_by_self_tasks(self):
        response = self.client.get(reverse('tasks:tasks_list'), {'self_tasks': 'on'})
        self.assertContains(response, self.task.name)
