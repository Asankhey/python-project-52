from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from task_manager.statuses.models import Status
from task_manager.models import Task

User = get_user_model()


class TaskCRUDTest(TestCase):
    def setUp(self):
        self.author = User.objects.create_user(username='author', password='pass123')
        self.executor = User.objects.create_user(username='executor', password='pass123')
        self.client.force_login(self.author)

        self.status = Status.objects.create(name='New')
        self.task = Task.objects.create(
            name='Test Task',
            description='Description',
            status=self.status,
            author=self.author,
            executor=self.executor,
        )

    def test_create_task(self):
        response = self.client.post(reverse('tasks:tasks_create'), {
            'name': 'Created Task',
            'description': 'Created desc',
            'status': self.status.pk,
            'executor': self.executor.pk,
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(name='Created Task').exists())

    def test_task_detail_view(self):
        response = self.client.get(reverse('tasks:tasks_detail', args=[self.task.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.task.name)

    def test_update_task(self):
        response = self.client.post(reverse('tasks:tasks_update', args=[self.task.pk]), {
            'name': 'Updated Task',
            'description': 'Updated desc',
            'status': self.status.pk,
            'executor': self.executor.pk,
        })
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, 'Updated Task')

    def test_delete_task_by_author(self):
        response = self.client.post(reverse('tasks:tasks_delete', args=[self.task.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())

    def test_delete_task_by_non_author(self):
        self.client.logout()
        self.client.force_login(self.executor)
        response = self.client.post(reverse('tasks:tasks_delete', args=[self.task.pk]))
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Task.objects.filter(pk=self.task.pk).exists())

    def test_login_required_for_views(self):
        self.client.logout()
        urls = [
            reverse('tasks:tasks_list'),
            reverse('tasks:tasks_create'),
            reverse('tasks:tasks_detail', args=[self.task.pk]),
            reverse('tasks:tasks_update', args=[self.task.pk]),
            reverse('tasks:tasks_delete', args=[self.task.pk]),
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertRedirects(response, f'/users/login/?next={url}')
