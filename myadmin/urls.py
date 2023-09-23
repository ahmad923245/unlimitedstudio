"""unlimitedstudio URL Configuration

The `urlpatterns` list routes URLs to view. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function view
    1. Add an import:  from my_app import view
    2. Add a URL to urlpatterns:  path('', view.home, name='home')
Class-based view
    1. Add an import:  from other_app.view import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URL conf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include

# from .forms import EmailValidationOnForgotPassword
from .view import user, role_views, module_views, method_views

urlpatterns = [
    path('', user.showLogin, name='login'),
    # path('',user.Login.as_view(),name='login'),
    path('checkLogin', user.checkLogin, name='checkLogin'),
    path('forgot-password', user.forgotPassword, name='forgotPassword'),
    # path('forgot-password/', auth_views.PasswordResetView.as_view(form_class=EmailValidationOnForgotPassword, success_url='',email_template_name='',html_email_template_name='auth/forgot_password.html'), name='forgotPassword'),
    path('dashboard/', user.dashboard, name='dashboard'),
    path('profile/', user.profile, name='profile'),
    path('changepassword/', user.change_password, name='change_password'),
    path('logout', user.Logout, name='logout'),
    path('',include('user.urls')),
    path('',include('setting.urls')),
    path('',include('studio.urls')),
    path('module', module_views.list, name='module'),
    path('module/getlist', module_views.get_list, name='module_list'),
    path('module/add', module_views.add, name='module.add'),
    path('module/updatestatus', module_views.update_status, name='module.updateStatus'),
    path('module/edit/<int:id>', module_views.edit, name='module.edit'),
    path('module/view/<int:id>', module_views.view, name='module.view'),
    path('module/delete/<int:id>', module_views.delete, name='module.delete'),

    path('method', method_views.list, name='method'),
    path('method/getlist', method_views.get_list, name='method_list'),
    path('method/add', method_views.add, name='method.add'),
    path('method/updatestatus', method_views.update_status, name='method.updateStatus'),
    path('method/edit/<int:id>', method_views.edit, name='method.edit'),
    path('method/view/<int:id>', method_views.view, name='method.view'),
    path('method/delete/<int:id>', method_views.delete, name='method.delete'),

    path('role', role_views.list, name='role'),
    path('rolelist', role_views.get_list, name='role_list'),
    path('role/add', role_views.add, name='role.add'),
    path('role/updatestatus', role_views.update_status, name='role.updateStatus'),
    path('role/edit/<int:id>', role_views.edit, name='role.edit'),
    path('role/view/<int:id>', role_views.view, name='role.view'),
    path('role/delete/<int:id>', role_views.delete, name='role.delete'),

]
