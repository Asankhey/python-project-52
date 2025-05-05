from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class UserCRUDTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.force_login(self.user)
        self.other_user = User.objects.create_user(username='otheruser')

    def test_create_user(self):
        response = self.client.post(reverse('users:users_create'), {
            'username': 'newuser',
            'password1': 'complexpass123',
            'password2': 'complexpass123',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_update_user(self):
        response = self.client.post(
            reverse('users:users_update', args=[self.other_user.id]),
            {'username': 'updatedname'}
        )
        self.assertEqual(response.status_code, 302)
        self.other_user.refresh_from_db()
        self.assertEqual(self.other_user.username, 'updatedname')
        self.assertRedirects(response, reverse('users:users_list'))

    def test_delete_user(self):
        response = self.client.post(reverse('users:users_delete', args=[self.other_user.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(User.objects.filter(id=self.other_user.id).exists())
        self.assertRedirects(response, reverse('users:users_list'))