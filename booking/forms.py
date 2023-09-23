from django import forms
from django.contrib.admin.views import autocomplete
from django.contrib.auth.forms import PasswordResetForm
from django.core.exceptions import ValidationError

from .models import *



class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['studio','musician','appointment_date','appointment_time',
                  'service_id','cost','payment_type','accepted',
                  'accepted_date','decline_by','decline','cancelled','payment_status',
                  'payment_method_nonce','paid_amount','payment_type','paid_date','cashout_status',
                  'cashout_date','card_number','transaction_id','commision_amount',
                  ]






# class DishForm(forms.ModelForm):
    # en_title = forms.CharField(max_length=255, required=False)
    # it_title = forms.CharField(max_length=255, required=True)
    # en_history = forms.CharField(widget=forms.Textarea, required=True)
    # it_history = forms.CharField(widget=forms.Textarea, required=True)
    # en_notes = forms.CharField(widget=forms.Textarea, required=False)
    # it_notes = forms.CharField(widget=forms.Textarea, required=False)
    # en_bibliography = forms.CharField(widget=forms.Textarea, required=True)
    # it_bibliography = forms.CharField(widget=forms.Textarea, required=True)
    # minor_ingredients = forms.CharField(widget=forms.Textarea, required=False)
    # keywords = forms.CharField(widget=forms.Textarea, required=False)
    # aliases = forms.CharField(widget=forms.Textarea, required=False)
    # address = forms.CharField(required=True)
    # city = forms.CharField(max_length=255, required=True)
    # state = forms.CharField(max_length=255, required=True)
    # country = forms.CharField(max_length=255, required=True)
    # latitude = forms.CharField(max_length=25, required=True)
    # longitude = forms.CharField(max_length=25, required=True)
    # origin_address = forms.CharField(required=True)
    # origin_city = forms.CharField(max_length=255, required=True)
    # origin_state = forms.CharField(max_length=255, required=True)
    # origin_country = forms.CharField(max_length=255, required=True)
    # origin_latitude = forms.CharField(max_length=25, required=True)
    # origin_longitude = forms.CharField(max_length=25, required=True)
    # ingredients = forms.MultipleChoiceField(required= True , choices=Ingredients.objects.values_list('id','en_title'))
    # eat_months = forms.MultipleChoiceField(required=True , choices=MonthList.objects.values_list('id','month_name'))
    # image = forms.FileField(required=False)
    # dish_type = forms.ModelChoiceField(queryset=DishType.objects.all(),
    #                                       required=True,
    #                                       empty_label='Select Dish Type',
    #                                       widget=forms.Select(attrs={'class': 'form-control', 'required': False}))
    # dish_category = forms.ModelChoiceField(queryset=DishCategory.objects.all(),
    #                                       required=True,
    #                                       empty_label='Select Dish Catagory',
    #                                       widget=forms.Select(attrs={'class': 'form-control', 'required': False}))
    # scope_type = forms.ModelChoiceField(queryset=ScopeType.objects.all(),
    #                                        required=True,
    #                                        empty_label='Select Scope Type',
    #                                        widget=forms.Select(attrs={'class': 'form-control', 'required': False}))
    # cooking_type = forms.ModelChoiceField(queryset=CookingType.objects.all(),
    #                                        required=True,
    #                                        empty_label='Select Cooking Type',
    #                                        widget=forms.Select(attrs={'class': 'form-control', 'required': False}))
    # serve_type = forms.ModelChoiceField(queryset=ServeType.objects.all(),
    #                                        required=True,
    #                                        empty_label='Select Serve Type',
    #                                        widget=forms.Select(attrs={'class': 'form-control', 'required': False}))
    # class Meta:
    #     model = Dish
    #     fields = ''