from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from statuses.models import Status

User = get_user_model()


class StatusesTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.force_login(self.user)
        self.status = Status.objects.create(name='тестовый статус')

    def test_status_list_view(self):
        response = self.client.get(reverse('statuses:statuses_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.status.name)

    def test_status_create_view(self):
        response = self.client.post(
            reverse('statuses:status_create'),
            {'name': 'на тестировании'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Status.objects.filter(name='на тестировании').exists())

    def test_status_update_view(self):
        response = self.client.post(
            reverse('statuses:status_update', args=[self.status.id]),
            {'name': 'обновленный'}
        )
        self.assertEqual(response.status_code, 302)
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, 'обновленный')

    def test_status_delete_view(self):
        response = self.client.post(reverse('statuses:status_delete', args=[self.status.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Status.objects.filter(id=self.status.id).exists())

    def test_login_required_views(self):
        self.client.logout()
        urls = [
            reverse('statuses:statuses_list'),
            reverse('statuses:status_create'),
            reverse('statuses:status_update', args=[self.status.id]),
            reverse('statuses:status_delete', args=[self.status.id]),
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertRedirects(response, f'/users/login/?next={url}')
