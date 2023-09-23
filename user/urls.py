from django.contrib.auth import views as auth_views
from django.urls import path, re_path ,include

# from .forms import EmailValidationOnForgotPassword
from .views import *
from user.view import notification
from rest_framework.routers import DefaultRouter
router=DefaultRouter()
router.register('get_list',Get_list_api,basename='admin_get_user_list')

urlpatterns = [
    path('user/', list, name='user'),
    path('userlist/', get_list, name='user_list'),
    path('user/add/',add, name='user.add'),
    path('user/updatestatus/', update_status, name='user.updateStatus'),
    path('user/edit/<int:id>/', edit, name='user.edit'),
    path('user/view/<int:id>/', view, name='user.view'),
    path('user/delete/<int:id/', delete, name='user.delete'),
    path('notification/',notification.list, name='notification'),
    path('notificationlist/', notification.get_list, name='notification_list'),
    path('notification/add/',notification.add, name='notification.add'),
    path('notification/updatestatus/', notification.update_status, name='notification.updateStatus'),
    path('notification/view/<int:id>/', notification.view, name='notification.view'),
    path('notification/delete/<int:id>/', notification.delete, name='notification.delete'),
    path('api/',include(router.urls))
]
