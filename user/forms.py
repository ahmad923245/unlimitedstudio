from django import forms
from myadmin.models import Role
from .models import *
from django.db.models import Q


class NotificationForm(forms.ModelForm):
    title = forms.CharField()
    user_type = forms.ModelChoiceField(queryset=Role.objects.filter(Q(id=2) | Q(id=3)),
                                  required=True,
                                  empty_label='Select Role',
                                  widget=forms.Select(attrs={'class': 'form-control', 'required': False}))

    class Meta:
        model = Notifications
        fields = ['title', 'message', 'user_type']

