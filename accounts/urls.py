from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.home, name='home'),
    path('user_regist', views.user_regist, name='user_regist'),
    path('user_login', views.user_login, name='user_login'),
    path('user_logout', views.user_logout, name='user_logout'),
    path('user/<int:id>', views.user, name='user'),
    path('user_update', views.user_update, name='user_update'),
    path('password_change', views.password_change, name='password_change'),
    path('user_delete/<int:id>', views.user_delete, name='user_delete'),
    path('is_staff_check', views.is_staff_check, name='is_staff_check'),
]