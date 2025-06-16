from django.contrib import admin
from django.urls import include, path

from .views import HomePageView, LoginUser, LogoutUser

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('i18n/', include('django.conf.urls.i18n')),
    path('tasks/', include('task_manager.tasks.urls')),
    path('statuses/', include('task_manager.statuses.urls')),
    path('users/', include('task_manager.users.urls')),
    path('labels/', include('task_manager.labels.urls')),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', LogoutUser.as_view(), name='logout'),
    path('admin/', admin.site.urls),

]
