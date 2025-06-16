from django.test import TestCase
from django.urls import reverse

from task_manager.statuses.models import Status
from task_manager.users.models import User


class StatusTestCase(TestCase):
    fixtures = [
        'user_test.json',
        'status_test.json',
    ]

    def login(self):
        self.client.force_login(User.objects.get(pk=1))

    def test_ListStatuses(self):
        self.login()
        resp = self.client.get(reverse('statuses'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(
            resp,
            template_name='statuses/status_list.html'
        )
        self.assertTrue(len(resp.context['statuses']) == 4)

    def test_create_status(self):
        self.login()
        resp = self.client.get(reverse('create_status'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(
            resp,
            template_name='general/general_form.html'
        )

        resp = self.client.post(reverse('create_status'), {
            'name': 'test',
        })
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse('statuses'))

        status = Status.objects.last()
        self.assertEqual(status.name, 'test')

        resp = self.client.get(reverse('statuses'))
        self.assertTrue(len(resp.context['statuses']) == 5)

    def test_DeleteStatus(self):
        self.login()
        status = Status.objects.get(name='new')
        resp = self.client.post(
            reverse('delete_status', args=[status.id])
        )
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse('statuses'))
        self.assertFalse(
            Status.objects.filter(id=status.id).exists()
        )
