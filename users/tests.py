from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class UserCRUDTest(TestCase):
    def setUp(self):
        self.password = 'pass12345'
        self.user = User.objects.create_user(
            username='testuser',
            first_name='Test',
            last_name='User',
            password=self.password
        )
        self.client.login(username='testuser', password=self.password)

    def test_create_user(self):
        self.client.logout()
        response = self.client.post(reverse('users:create'), {
            'username': 'newuser',
            'password1': 'strongpass123',
            'password2': 'strongpass123',
            'first_name': 'New',
            'last_name': 'User'
        })
        self.assertRedirects(response, reverse('users:login'))
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_update_user(self):
        response = self.client.post(reverse('users:update', args=[self.user.pk]), {
            'username': 'updateduser',
            'first_name': 'Updated',
            'last_name': 'User'
        })
        self.assertRedirects(response, reverse('users:index'))
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updateduser')

    def test_delete_user(self):
        response = self.client.post(reverse('users:delete', args=[self.user.pk]))
        self.assertRedirects(response, reverse('users:index'))
        self.assertFalse(User.objects.filter(pk=self.user.pk).exists())
