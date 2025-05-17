from django.contrib import admin
from django.urls import path, include
from task_manager.tasks.views import trigger_error  # 👈 импорт вьюхи

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('task_manager.tasks.urls', namespace='tasks')),
    path('users/', include('users.urls', namespace='users')),
    path('statuses/', include('statuses.urls', namespace='statuses')),
    path('labels/', include('task_manager.labels.urls', namespace='labels')),
    path('rollbar-debug/', trigger_error),  # 👈 путь для проверки Rollbar
]
