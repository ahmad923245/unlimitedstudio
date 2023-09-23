from django import forms
from django.contrib.admin.views import autocomplete
from django.contrib.auth.forms import PasswordResetForm
from django.core.exceptions import ValidationError

from .models import *
from user.models import *

class ModuleForm(forms.ModelForm):
    name = forms.CharField(max_length=255, required=True)
    display_name = forms.CharField(max_length=255, required=True)

    class Meta:
        model = Module
        fields = ['name', 'display_name']


class MethodForm(forms.ModelForm):
    name = forms.CharField(max_length=255, required=True)
    display_name = forms.CharField(max_length=255, required=True)
    module = forms.ModelChoiceField(queryset=Module.objects.all(),
                                    required=True,
                                    empty_label='Select Module',
                                    widget=forms.Select(attrs={'class': 'form-control', 'required': False}))

    class Meta:
        model = Method
        fields = ['name', 'display_name', 'module']


class RoleForm(forms.ModelForm):
    title = forms.CharField(max_length=255, required=True)
    permission = forms.MultipleChoiceField(required=True,
                 choices=Method.objects.values_list('id', 'display_name'))

    # permission=forms.ModelMultipleChoiceField(widget=forms.SelectMultiple(),
    #                                queryset=Method.objects.all())

    class Meta:
        model = Role
        fields = ['title', 'permission']


class SubadminForm(forms.ModelForm):
    first_name = forms.CharField(max_length=255, required=True)
    # last_name = forms.CharField(max_length=255, required=True)
    password = forms.CharField(widget=forms.PasswordInput)
    # email = forms.EmailField(max_length=255)
    # username = forms.CharField(max_length=255, required=False)
    # phone_number = forms.CharField(max_length=20,required=True)
    gender = forms.CharField(max_length=25,required=True)
    role = forms.ModelChoiceField(queryset=Role.objects.all().exclude(id__in=[1,2,3]),
                                  required=True,
                                  empty_label='Select Role',
                                  widget=forms.Select(attrs={'class': 'form-control', 'required': False}))

    class Meta:
        model = User
        fields = ['first_name', 'email', 'role','gender','password']


class UserForm(forms.ModelForm):
    role = forms.ModelChoiceField(queryset=Role.objects.filter(id__in=[2, 3]),
                                  required=True,
                                  empty_label='Select Role',
                                  widget=forms.Select(attrs={'class': 'form-control', 'required': False}))
    first_name = forms.CharField(max_length=255, required=True)
    gender = forms.CharField(max_length=25,required=True)
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model=User
        fields = ['first_name', 'email', 'gender', 'password', 'role']

    # def clean_email(self):
    #     email = self.cleaned_data['email']
    #     if User.objects.filter(email=email).exists():
    #         raise ValidationError("Email already exists")
    #     return email


class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=255, required=True)
    last_name = forms.CharField(max_length=255, required=True)
    profile_image = models.FileField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'profile_image']


class ChangePasswordForm(forms.ModelForm):
    current_password = forms.CharField(max_length=255, required=True)
    new_password = forms.CharField(max_length=255, required=True, min_length=6)
    confirm_password = forms.CharField(max_length=255, required=True, min_length=6)

    class Meta:
        model = User
        fields = ['current_password', 'new_password', 'confirm_password']


class EmailValidationOnForgotPassword(PasswordResetForm):

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email__iexact=email, status=True).exists():
            msg = _("E-Mail id does not exist")
            self.add_error('email', msg)
        return email


