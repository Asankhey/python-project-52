from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from task_manager.statuses.models import Status

User = get_user_model()


class TestStatusesCRUD(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.client.force_login(self.user)
        self.status = Status.objects.create(name='Old name')

    def test_list(self):
        response = self.client.get(reverse('statuses:statuses_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Old name')

    def test_create(self):
        response = self.client.post(reverse('statuses:status_create'), {
            'name': 'New Status'
        })
        self.assertRedirects(response, reverse('statuses:statuses_list'))
        self.assertTrue(Status.objects.filter(name='New Status').exists())

    def test_update(self):
        response = self.client.post(reverse('statuses:status_update', args=[self.status.id]), {
            'name': 'Updated Name'
        })
        self.assertRedirects(response, reverse('statuses:statuses_list'))
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, 'Updated Name')

    def test_delete(self):
        response = self.client.post(reverse('statuses:status_delete', args=[self.status.id]))
        self.assertRedirects(response, reverse('statuses:statuses_list'))
        self.assertFalse(Status.objects.filter(id=self.status.id).exists())

    def test_login_required(self):
        self.client.logout()
        urls = [
            reverse('statuses:statuses_list'),
            reverse('statuses:status_create'),
            reverse('statuses:status_update', args=[self.status.id]),
            reverse('statuses:status_delete', args=[self.status.id]),
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)
            self.assertTrue(response.url.startswith('/users/login/'))
