from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):

    def admin(self):
        return self.get_queryset().filter(is_staff=True, is_superuser=True)

    def customers(self):
        return self.get_queryset().filter(is_staff=False, is_superuser=False)

    def inactive(self):
        return self.get_queryset().filter(is_active=False)

    def active(self):
        return self.get_queryset().filter(is_active=True)

    def create_user(self,email, password):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(

            email=self.normalize_email(email),

        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email=email,
            password=password
        )
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user

# type = (
#         ("MUSICIAN", "MUSICIAN"),
#         ("SERVICE_PROVIDER", "SERVICE_PROVIDER")
# )

class User(AbstractBaseUser ,PermissionsMixin):
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    country_code = models.CharField(max_length=255, null=True, blank=True)
    mobile = models.CharField(max_length=255, null=True, blank=True)
    gender = models.CharField(max_length=255, null=True, blank=True)
    social_type = models.CharField(max_length=20, null=True, blank=True)
    social_id = models.CharField(max_length=255, null=True, blank=True)
    is_sociallogin = models.BooleanField(default=False)
    image_link=models.CharField(verbose_name=_('image_link'), max_length=1000,
                                null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, unique=True)
    is_email_verified = models.BooleanField(default=False, null=True,
                                            blank=True)
    is_mobile_vrified = models.BooleanField(default=True)
    otp=models.CharField(verbose_name=_('OTP'), max_length=10,default="1234")
    notification_status = models.BooleanField(default=True, blank=True,
                                              null=True)
    status = models.BooleanField(default=True, blank=True, null=True)
    role = models.ForeignKey('myadmin.Role',
                             on_delete=models.CASCADE,
                             blank=True, related_name='role', null=True)
    profile_image = models.FileField(max_length=255, null=True, blank=True,
                                     upload_to='users')
    strip_customer_id = models.CharField(max_length=200, null=True, blank=True)
    strip_Connect_id = models.CharField(max_length=200, null=True, blank=True)
    is_musician = models.BooleanField(default=False)
    is_service_provider = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    objects = UserManager()
    deleted_account = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_profile_setup = models.BooleanField(default=False)
    is_studio_setup = models.BooleanField(default=False)

    class Meta:
        db_table = 'users'

    USERNAME_FIELD = 'email'

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.is_staff or self.is_superuser

    def __str__(self):
        return self.email

class UserOtp(models.Model):
    phone_code = models.CharField(max_length=10, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    user_id = models.IntegerField(null=True, blank=True)
    otp_code = models.IntegerField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_otps'


from django.db import models

# Create your models here.


# class SocialLoginUser(models.Model):
#
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     uid = models.CharField(max_length=100, null=False, blank=False)
#     provider = models.CharField(max_length=50, null=False, blank=False)
#     created_date = models.DateTimeField(auto_now_add=True)
#     modified_date = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return str(self.user)





class Notifications(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    user_type = models.CharField(max_length=250, null=True, blank=True)
    title = models.CharField(max_length=250, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    status = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=250, null=True, blank=True)
    booking_id = models.CharField(max_length=250, null=True, blank=True)
    sender_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Sender_id', null=True, blank=True)

# from celery import current_app
# from .serializers import NotificationListSerializer
# from .task import *
# @receiver(post_save, sender=Notifications)
# def save_profile(sender, instance, **kwargs):
#     print(NotificationListSerializer(instance).data, "____________________________152")
#     custom_notification_func.delay(NotificationListSerializer(instance).data)


class UserSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True,blank=True)
    session_id = models.CharField(max_length=100)
    is_online = models.BooleanField(default=False)

    class Meta:
        db_table = 'user_session'


class SoketImageUpload(models.Model):
    image = models.ImageField(upload_to='image_document', blank=True, null=True)
    image_thumbnail = models.ImageField(upload_to='image_document', blank=True, null=True)

    class Meta:
        db_table = 'socket_image_upload'


Message_Type = (
    ('TEXT', 'TEXT'),
    ('IMAGE', 'IMAGE'),)

class Conversation(models.Model):
    sender = models.ForeignKey(User, null=True, blank=True,on_delete=models.CASCADE,related_name='conversation_sender')
    receiver = models.ForeignKey(User, null=True, blank=True,on_delete=models.CASCADE, related_name="conversation_receiver")
    #event = models.ForeignKey('event.Event',  null=True, blank=True, on_delete=models.CASCADE,related_name='event_conversation')
    #conversation_number = models.CharField(verbose_name='Conversation Number',max_length=20, default='Conversation_number)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_check =models.BooleanField(default=True)
    conversation_delete = models.CharField(verbose_name=('Conversation Delete'), max_length=10000, default='0')
    class Meta:
        verbose_name_plural = 'Chat Conversation'


class ChatMessage(models.Model):
    conversation_id = models.ForeignKey(Conversation, null=True, blank=True, on_delete=models.CASCADE,
                                     related_name='Conversation')
    sender = models.ForeignKey(User, on_delete=models.CASCADE,related_name='send_message_user', null=True, blank=True)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE,related_name='receive_message_user',null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    message_type = models.CharField(choices=Message_Type, default='TEXT', max_length=50, null=True, blank=True)
    thumbnail_image = models.CharField(verbose_name=('Socket Thumb Image'), max_length=100, null=True, blank=True)
    image = models.CharField(verbose_name=('Socket Image'), max_length=100, null=True, blank=True)
    message_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'chat_messages'


class BlockUser(models.Model):
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE,
                                   related_name='block_created_by')
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name='users')
    block = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    block_user_id = models.CharField(verbose_name=('Which Block User'),
                                    max_length=10000, default='0')


    class Meta:
        db_table = 'block_user'


class VersionControl(models.Model):
    class Meta:
        verbose_name =("Settings")
        verbose_name_plural = ("Settings")
    ios_version =models.CharField(max_length=100,verbose_name=('Ios Version'),blank=True, null=True)
    android_version =models.CharField(max_length=100,verbose_name=('Android  Version'),blank=True, null=True)
    ios_app_message =models.CharField(max_length=250,verbose_name=('Ios App Message'),blank=True, null=True)
    android_app_message =models.CharField(max_length=250,verbose_name=('Android App Message'),blank=True, null=True)
    ios_force_stop=models.BooleanField(default=False, verbose_name=('Ios Force Stop'))
    android_force_stop=models.BooleanField(default=False, verbose_name=('Android Force Stop'))
    ios_maintenance=models.BooleanField(default=False, verbose_name=('Ios Maintenance'))
    android_maintenance=models.BooleanField(default=False, verbose_name=('Android Maintenance'))
    android_app_link=models.CharField(max_length=250,verbose_name=('Android App Link'),blank=True, null=True)
    ios_app_link=models.CharField(max_length=250,verbose_name=('Ios App Link'),blank=True, null=True)
