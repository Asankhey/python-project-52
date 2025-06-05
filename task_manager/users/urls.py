from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.UserListView.as_view(), name='users_list'),
    path('create/', views.UserCreateView.as_view(), name='users_create'),
    path('<int:pk>/update/', views.UserUpdateView.as_view(), name='users_update'),
    path('<int:pk>/delete/', views.UserDeleteView.as_view(), name='users_delete'),
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
