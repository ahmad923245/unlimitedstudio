from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, AbstractBaseUser ,PermissionsMixin


class Module(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    display_name = models.CharField(max_length=255, null=True, blank=True)
    status = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'modules'


class Method(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    display_name = models.CharField(max_length=255, null=True, blank=True)
    module = models.ForeignKey(Module, on_delete=models.CASCADE, blank=True, related_name='method')
    status = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'methods'


class Role(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    status = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    # permissions = models.ManyToManyField(Permission)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'roles'


class Permission(models.Model):
    method_id = models.IntegerField(null=True, blank=True)
    role_id = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'permissions'

# class Cms(models.Model):
#     en_title = models.CharField(max_length=255, null=True, blank=True)
#     en_description = models.TextField(null=True, blank=True)
#     status = models.BooleanField(default=True)
#     created_date = models.DateTimeField(auto_now_add=True)
#     modified_date = models.DateTimeField(auto_now=True)
#
#
#     class Meta:
#         db_table = 'cms'


# class UserManager(BaseUserManager):
#
#     def admin(self):
#         return self.get_queryset().filter(is_staff=True, is_superuser=True)
#
#     def customers(self):
#         return self.get_queryset().filter(is_staff=False, is_superuser=False)
#
#     def inactive(self):
#         return self.get_queryset().filter(is_active=False)
#
#     def active(self):
#         return self.get_queryset().filter(is_active=True)
#
#     def create_user(self,email, password):
#         """
#         Creates and saves a User with the given email and password.
#         """
#         if not email:
#             raise ValueError('Users must have an email address')
#
#         user = self.model(
#
#             email=self.normalize_email(email),
#
#         )
#
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
#
#     def create_superuser(self,email, password):
#         """
#         Creates and saves a superuser with the given email and password.
#         """
#         user = self.create_user(
#
#             email=email,
#             password=password
#
#         )
#         user.is_staff = True
#         user.is_superuser = True
#         user.is_active = True
#         user.save(using=self._db)
#         return user
#
#
#
# class User(AbstractBaseUser ,PermissionsMixin):
#     first_name = models.CharField(max_length=255, null=True, blank=True)
#     last_name = models.CharField(max_length=255, null=True, blank=True)
#     phone_code = models.CharField(max_length=255, null=True, blank=True)
#     mobile = models.CharField(max_length=255, null=True, blank=True)
#     gender = models.CharField(max_length=255, null=True, blank=True)
#     social_type = models.CharField(max_length=20, null=True, blank=True)
#     social_id = models.CharField(max_length=255, null=True, blank=True)
#     email = models.EmailField(max_length=255, null=True, unique=True)
#     email_verified = models.BooleanField(default=False, null=True, blank=True)
#     notification_permission = models.BooleanField(default=True, blank=True, null=True)
#     status = models.BooleanField(default=True, blank=True, null=True)
#     role = models.ForeignKey(Role, on_delete=models.CASCADE, blank=True, related_name='role', null=True)
#     image = models.FileField(max_length=255, null=True, blank=True, upload_to='users')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     objects = UserManager()
#     is_active = models.BooleanField(default=False)
#     is_staff = models.BooleanField(default=False)
#     is_superuser = models.BooleanField(default=False)
#     # class Meta:
#     #     db_table = 'users'
#
#     USERNAME_FIELD = 'email'
#
#     @property
#     def is_admin(self):
#         "Is the user a admin member?"
#         return self.is_staff or self.is_superuser



# class UserOtp(models.Model):
#     phone_code = models.CharField(max_length=10, null=True, blank=True)
#     phone_number = models.CharField(max_length=20, null=True, blank=True)
#     email = models.EmailField(max_length=255, null=True, blank=True)
#     user_id = models.IntegerField(null=True, blank=True)
#     otp_code = models.IntegerField(null=True, blank=True)
#     created_date = models.DateTimeField(auto_now_add=True)
#     modified_date = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         db_table = 'user_otps'


# class UserDevice(models.Model):
#     user_id = models.IntegerField(null=True, blank=True)
#     device_type = models.CharField(max_length=20, null=True, blank=True)
#     device_id = models.CharField(max_length=255, null=True, blank=True)
#
#     class Meta:
#         db_table = 'user_devices'





# class Faq(models.Model):
#     en_title = models.CharField(max_length=255, null=True, blank=True)
#     it_title = models.CharField(max_length=255, null=True, blank=True)
#     en_description = models.TextField(null=True, blank=True)
#     it_description = models.TextField(null=True, blank=True)
#     status = models.BooleanField(default=True)
#     created_date = models.DateTimeField(auto_now_add=True)
#     modified_date = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         db_table = 'faq'
#
#
# class Contact(models.Model):
#     name = models.CharField(max_length=100, null=True, blank=True)
#     email = models.EmailField(max_length=255, null=True, blank=True)
#     phone_number = models.CharField(max_length=30, null=True, blank=True)
#     message = models.TextField(null=True, blank=True)
#     created_date = models.DateTimeField(auto_now_add=True)
#     modified_date = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         db_table = 'contacts'
#
#









