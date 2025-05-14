from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from task_manager.models import Label

User = get_user_model()


class LabelCRUDTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.force_login(self.user)
        self.label = Label.objects.create(name='bug')

    def test_label_list_view(self):
        response = self.client.get(reverse('labels:labels_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.label.name)

    def test_label_create_view(self):
        response = self.client.post(
            reverse('labels:labels_create'),
            {'name': 'feature'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Label.objects.filter(name='feature').exists())

    def test_label_update_view(self):
        response = self.client.post(
            reverse('labels:labels_update', args=[self.label.id]),
            {'name': 'critical'}
        )
        self.assertEqual(response.status_code, 302)
        self.label.refresh_from_db()
        self.assertEqual(self.label.name, 'critical')

    def test_label_delete_view(self):
        response = self.client.post(reverse('labels:labels_delete', args=[self.label.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Label.objects.filter(id=self.label.id).exists())

    def test_login_required_for_labels(self):
        self.client.logout()
        urls = [
            reverse('labels:labels_list'),
            reverse('labels:labels_create'),
            reverse('labels:labels_update', args=[self.label.id]),
            reverse('labels:labels_delete', args=[self.label.id]),
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertRedirects(response, f'/users/login/?next={url}')
