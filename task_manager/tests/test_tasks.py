from django.test import TestCase
from django.urls import reverse

from task_manager.tasks.models import Task
from task_manager.users.models import User


class TaskTestCase(TestCase):
    fixtures = ["user_test", "task_test"]

    def login(self):
        user = User.objects.get(pk=1)
        self.client.force_login(user)

    def test_access(self):
        urls = [
            reverse('task_create'),
            reverse('tasks'),
            reverse('task_update', kwargs={'pk': 1}),
            reverse('task_delete', kwargs={'pk': 1}),
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)

        self.login()
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)

    def test_TaskCreate(self):
        self.login()
        url = reverse('task_create')

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'general/general_form.html')

        response = self.client.post(url, {
            'name': 'New Task',
            'description': 'New task description',
            'status': 1,
            'executor': 2,
            'labels': [],
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('tasks'))

        task = Task.objects.last()
        self.assertEqual(task.name, 'New Task')
        self.assertEqual(task.description, 'New task description')
        self.assertEqual(task.status.id, 1)
        self.assertEqual(task.executor.id, 2)
        self.assertEqual(task.author.id, 1)

    def test_ListTasks(self):
        self.login()
        response = self.client.get(reverse('tasks'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['tasks']), 2)

    def test_ViewTask(self):
        self.login()
        task = Task.objects.get(pk=1)
        response = self.client.get(reverse('task_view', kwargs={'pk': task.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task/task_detail.html')
        self.assertEqual(task.name, 'Fix login bug')

    def test_UpdateTask(self):
        self.login()
        task = Task.objects.get(pk=1)
        url = reverse('task_update', kwargs={'pk': task.pk})

        response = self.client.post(url, {
            'name': 'Updated Task',
            'description': 'Updated desc',
            'status': 1,
            'executor': 2,
            'labels': [],
        })
        self.assertEqual(response.status_code, 302)

        task.refresh_from_db()
        self.assertEqual(task.name, 'Updated Task')
        self.assertEqual(task.executor.id, 2)

    def test_DeleteTask(self):
        self.login()
        task = Task.objects.get(pk=1)
        url = reverse('task_delete', kwargs={'pk': task.pk})

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('tasks'))
        self.assertEqual(Task.objects.count(), 1)
