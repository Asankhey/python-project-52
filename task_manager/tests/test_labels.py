from django.test import TestCase
from django.urls import reverse
from task_manager.labels.models import Label
from task_manager.users.models import User


class LabelTestCase(TestCase):
    fixtures = [
        'user_test.json',
        'label_test.json',
    ]

    def login(self):
        self.client.force_login(User.objects.get(pk=1))

    def test_ListLabels(self):
        self.login()
        resp = self.client.get(reverse('labels'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(
            resp,
            template_name='labels/index.html'
        )
        self.assertEqual(len(resp.context['labels']), 4)
        names = [label.name for label in resp.context['labels']]
        self.assertIn('bug', names)
        self.assertIn('urgent', names)

    def test_CreateLabel(self):
        self.login()
        resp = self.client.get(reverse('create_label'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(
            resp,
            template_name='general/general_form.html'
        )

        resp = self.client.post(reverse('create_label'), {
            'name': 'test-label',
        })
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(
            resp,
            reverse('labels')
        )

        label = Label.objects.last()
        self.assertEqual(label.name, 'test-label')

        resp = self.client.get(reverse('labels'))
        self.assertEqual(len(resp.context['labels']), 5)
        names = [label.name for label in resp.context['labels']]
        self.assertIn('test-label', names)

    def test_DeleteLabel(self):
        self.login()
        label = Label.objects.get(name="bug")
        resp = self.client.post(
            reverse('delete_label', args=[label.id])
        )
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(
            resp,
            reverse('labels')
        )
        self.assertFalse(Label.objects.filter(id=label.id).exists())
