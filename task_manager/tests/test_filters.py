from django.test import TestCase, RequestFactory
from task_manager.tasks.filters import TaskFilter
from task_manager.users.models import User
from task_manager.tasks.models import Task


class FilterTestCase(TestCase):
    fixtures = ["user_test", "label_test", "status_test", "task_test"]

    def setUp(self):
        self.user = User.objects.get(id=1)
        self.factory = RequestFactory()

    def get_filter(self, data):
        request = self.factory.get('/fake-url', data)
        request.user = self.user
        return TaskFilter(
            data=data,
            queryset=Task.objects.all(),
            request=request
        )

    def test_status(self):
        task_filter = self.get_filter({'status': 1})
        self.assertEqual(task_filter.qs.count(), 2)

    def test_executor(self):
        task_filter = self.get_filter({'executor': 1})
        self.assertEqual(task_filter.qs.count(), 2)
        self.assertEqual(task_filter.qs.first().executor.username, 'admin')

    def test_author(self):
        task_filter = self.get_filter({'author': 1})
        self.assertEqual(task_filter.qs.count(), 2)
        self.assertEqual(task_filter.qs.first().author.username, 'admin')
