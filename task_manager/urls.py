from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('task_manager.tasks.urls', namespace='tasks')),
    path('users/', include('users.urls', namespace='users')),
    path('statuses/', include('statuses.urls', namespace='statuses')),
    path('labels/', include('task_manager.labels.urls', namespace='labels')),
]
