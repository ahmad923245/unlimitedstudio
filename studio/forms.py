from django import forms
from django.contrib.admin.views import autocomplete
from django.contrib.auth.forms import PasswordResetForm
from django.core.exceptions import ValidationError
from django.forms.models import inlineformset_factory, BaseInlineFormSet

from .models import *

# Create your forms here.
day = (
    ('Mon', 'Monday'),
    ('Tue', 'Tuesday'),
    ('Wed', 'Wednesday'),
    ('Thu', 'Thursday'),
    ('Fri', 'Friday'),
    ('Sat', 'Saturday'),
    ('Sun', 'Sunday'))


class StudioForm(forms.ModelForm):
    # image = forms.FileField(required=False)
    # availibility = forms.MultipleChoiceField(choices=day)
    # start_time = forms.TimeField()
    # end_time = forms.TimeField()

    # image = forms.FileField(required=False)
    studio_name = forms.CharField()
    category = forms.SelectMultiple(attrs={'required': True})
    subcategory = forms.SelectMultiple(attrs={'required': True})
    generic = forms.SelectMultiple(attrs={'required': True})
    # days = forms.MultipleChoiceField(choices=day)
    # start_time = forms.TimeField()
    # end_time = forms.TimeField()
    # ServiceName = forms.CharField(label='Service Name', required=True)
    # ServicePrice = forms.CharField(label='Service Price', required=True)
    # description = forms.CharField(widget=forms.Textarea)

    created_by = forms.ModelChoiceField(queryset=User.objects.filter(role_id=3),
                                  required=True,
                                  label='Studio Owner',
                                  empty_label='Select Service Provider',
                                  widget=forms.Select(attrs={'class': 'form-control', 'required': False}))
    class Meta:
        model = Studio
        fields = ['studio_name','category','subcategory','generic','created_by','price',
                  'instagram','twitter','facebook','description'

                  ]

    def __init__(self, *args, **kwargs):
        super(StudioForm, self).__init__(*args, **kwargs)
        # print(self.fields,'---------------------25')
        self.fields['generic'].widget.attrs['class'] = 'select2multiple'
        self.fields['category'].widget.attrs['class'] = 'select2multiple'
        self.fields['subcategory'].widget.attrs['class'] = 'select2multiple'
        # self.fields['days'].widget.attrs['class'] = 'select2multiple'



class StudioAvailabilityForm(forms.ModelForm):
    days = forms.MultipleChoiceField(choices=day)

    class Meta:
        model = StudioAvailability
        fields = ['days', 'start_time', 'end_time']

    # def __init__(self, *args, **kwargs):
    #     super(StudioAvailabilityForm, self).__init__(*args, **kwargs)
    #     self.fields['days'].widget.attrs['class'] = 'select2multiple'


# StudioFormSet = inlineformset_factory(
#     Studio,
#     StudioAvailability,
#     fields=('days',
#             'start_time',
#             'end_time',
#             ),
#     widgets={
#             'days': forms.MultipleChoiceField(choices=day),
#             'start_time': forms.TimeInput(attrs={
#                 'type': 'time'
#             }),
#             'end_time': forms.TimeInput(attrs={
#                 'type': 'time'
#             })},
#     extra=1,
#     can_order=True
# )

class GenericForm(forms.ModelForm):
    name = forms.CharField()

    class Meta:
        model = Generics
        fields = ['name', 'image']

class SubCategoryForm(forms.ModelForm):
    name = forms.CharField()
    class Meta:
        model = SubCategory
        fields = ['name', 'category']


class RaiseDisputeForm(forms.ModelForm):
    class Meta:
        model = RaiseDispute
        fields = ['comment']


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ['service_provider','name','description','image']

