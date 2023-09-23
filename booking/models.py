from django.db import models
from studio.models import *
from user.models import *
from django.db import models


class Booking(models.Model):
    studio = models.ForeignKey(Studio, on_delete=models.CASCADE, blank=True,
        null=True, related_name='users_category', verbose_name="User Category",)
    musician = models.ForeignKey(User, on_delete=models.CASCADE, blank=True,
        	null=True, related_name='booking_musician', verbose_name="musician",)
    appointment_date = models.DateField(auto_now_add=False, null=True, blank=True)
    appointment_time = models.TimeField(auto_now_add=False, null=True, blank=True)
    end_time = models.TimeField(auto_now_add=False, null=True, blank=True)
    service_id=models.CharField(max_length=500, blank=True, null=True)
    cost = models.FloatField(null=True, blank=True, default=0, verbose_name='Service Cost($)')
    payment_type = models.CharField(max_length=200, blank=True, null=True)
    accepted = models.BooleanField(default=False)
    sent_date = models.DateField(auto_now_add=True)
    accepted_date = models.DateField(auto_now_add=False, null=True, blank=True)
    decline_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True,
            null=True, related_name='decline_by_user', verbose_name="DeclineByUser",)
    decline = models.BooleanField(default=False)

    cancelled = models.BooleanField(default=False)
    payment_status=models.CharField(max_length=200, blank=True, null=True)
    payment_method_nonce = models.CharField(verbose_name=('Payment_method_nonce'),
        max_length=100, null=True, blank=True)
    paid_amount = models.FloatField(null=True, blank=True, default=0.0, verbose_name='paid amount($)')
    payment_type = models.CharField(max_length=200, blank=True, null=True)
    paid_date = models.DateField(auto_now_add=False, null=True, blank=True)
    cashout_status=models.BooleanField(default=False)
    cashout_date = models.DateField(auto_now_add=False, null=True, blank=True)
    card_number = models.CharField(max_length=20, blank=True, null=True)
    transaction_id = models.CharField(verbose_name=('Trans_id'), max_length=100,null=True, blank=True)
    commision_amount = models.CharField(verbose_name=('Commision Amount($)'),max_length=100, null=True, blank=True)
    #created_time = models.DateField(auto_now_add=False)
    time_slot = models.TextField(null=True, blank=True)



class PaymentIntent(models.Model):
    paymentintentid = models.CharField(max_length=500, null=True, blank=True)
    status = models.CharField(max_length=100, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True,
        blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = ("PaymentIntent")
        verbose_name_plural = ("PaymentIntents")
        db_table = 'PaymentIntents'



class BookingPayment(models.Model):
    class Meta:
        verbose_name = ("Transaction History")
        verbose_name_plural = ("Transaction History")

    studio = models.ForeignKey(Studio, on_delete=models.CASCADE, blank=True,
        null=True, related_name='service_provider_category', verbose_name="Service Provider",)
    musician=models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    customer_id=models.CharField(verbose_name=('Customer_id'), max_length=100, null=True, blank=True)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    payment_method_nonce= models.CharField(verbose_name=('Payment_method_nonce'), max_length=100, null=True, blank=True)
    transaction_id=models.CharField(verbose_name=('Transaction_id'), max_length=100, null=True, blank=True)
    amount =models.CharField(verbose_name=('Amount'), max_length=100, null=True, blank=True)
    status=models.CharField( max_length=100, null=True, blank=True)
    admincommision=models.CharField(max_length=250,null=True, blank=True)
    cashout_status = models.BooleanField(default=False)
    cashout_date = models.DateField(auto_now_add=False, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)
  