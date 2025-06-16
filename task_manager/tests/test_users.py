from django.test import TestCase
from django.urls import reverse

from task_manager.users.models import User


class UserTestCase(TestCase):
    fixtures = ["user_test"]

    def test_signUp(self):
        response = self.client.get(reverse('user_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'general/general_form.html')

        response = self.client.post(reverse('user_create'), {
            'first_name': 'Nail',
            'last_name': 'Ivanovich',
            'username': 'fatty',
            'password1': 'Test123@#',
            'password2': 'Test123@#',
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

        user = User.objects.last()
        self.assertEqual(user.first_name, 'Nail')
        self.assertEqual(user.last_name, 'Ivanovich')
        self.assertEqual(user.username, 'fatty')

    def test_ListUsers(self):
        response = self.client.get(reverse('users'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['users']), 3)

    def test_UpdateUser(self):
        user = User.objects.get(pk=2)
        url = reverse('user_update', kwargs={'pk': user.pk})

        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

        self.client.force_login(user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'general/general_form.html')

        response = self.client.post(url, {
            'first_name': 'IvanUpdated',
            'last_name': 'NewLast',
            'username': 'IvanNew',
            'password1': 'Newpass123@',
            'password2': 'Newpass123@',
        })
        self.assertEqual(response.status_code, 302)

        user.refresh_from_db()
        self.assertEqual(user.first_name, 'IvanUpdated')
        self.assertEqual(user.username, 'IvanNew')

    def test_DeleteUser(self):
        user = User.objects.get(pk=2)
        url = reverse('user_delete', kwargs={'pk': user.pk})

        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

        self.client.force_login(user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(url)
        self.assertRedirects(response, reverse('users'))
        self.assertEqual(User.objects.count(), 2)
