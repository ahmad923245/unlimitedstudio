from django import forms
from .models import *

# Create your forms here.


class CmsForm(forms.ModelForm):
    title = forms.CharField(max_length=255, required=True)
    description = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Cms
        fields = ['title', 'description']

class FaqForm(forms.ModelForm):
    title = forms.CharField(max_length=255, required=True)
    description = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Faq
        fields = ['title', 'description']

class StaticPagesForm(forms.ModelForm):
    class Meta:
        model = StaticPages
        fields = ['page_type', 'content']

class AdminChargesForm(forms.ModelForm):
    class Meta:
        model = AdminCharges
        fields = ['admin_percentes']
