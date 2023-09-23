from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.
class Cms(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    status = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cms'


class Faq(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    status = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'faq'


class Contact(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=30, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'contacts'

class AdminCharges(models.Model):
    admin_percentes = models.CharField(max_length=5, null=True,blank=True)

    class Meta:
        db_table = 'admin_charges'


StaticPage = [('privacy_policy', 'Privacy Policy for User'),
              ('terms_conditions', 'Terms Conditions for User'),
              ('service_provider_privacy_policy', 'Privacy Policy for Service Provider'),
              ('service_provider_terms_conditions', 'Terms Conditions for  Service Provide'),
              ('about_us', 'About us'),
              ('support', 'Support'),

              ]


class StaticPages(models.Model):
    page_type = models.CharField(max_length=255,unique=True,default='privacy_policy', choices=StaticPage)
    # content = models.TextField(null=True, blank=True)
    content = RichTextUploadingField(null=True, blank=True)

    def str(self):
        return self.page_type

    class Meta:
        verbose_name = 'Static Content'
        verbose_name_plural = 'Static Content'
        db_table = 'static content page'
