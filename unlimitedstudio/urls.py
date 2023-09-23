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
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.template.defaulttags import url
from django.urls import path, include
from django.contrib.auth import views as auth_views

# from app.views import verifyEmail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('myadmin/', include('myadmin.urls')),
    path('api/v1/',include('user.api.urls')),
    path('api/v1/studio/',include('studio.api.urls')),
    path('api/v1/booking/',include('booking.api.urls')),
    path('settings/',include('setting.api.urls')),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),

    # path('accounts', include('django.contrib.auth.urls')),
    # path('api/', include('api.urls')),

    # path('verify_email/<uidb64>/', verifyEmail, name='verify_email'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)





