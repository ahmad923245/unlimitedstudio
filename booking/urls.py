from django.urls import path, re_path,include

#from booking.models import Booking
# from django.contrib.auth import views as auth_views
# from .forms import EmailValidationOnForgotPassword
# from booking.view import booking_views

from .view import booking_views,bookingpayment_views

urlpatterns = [
path('booking',booking_views.list, name='booking'),
path('booking/getlist',booking_views.get_list, name='booking_list'),
# path('booking/add', booking_views.add, name='booking.add'),
# path('booking/update_status', booking_views.update_status,name='booking.updateStatus'),
# path('booking/edit/<int:id>', booking_views.edit, name='booking.edit'),
path('booking/view/<int:id>', booking_views.view, name='booking.view'),
# path('booking/delete/<int:id>', booking_views.delete, name='booking.delete'),


path('bookingpayment',bookingpayment_views.list, name='booking_payment'),
path('bookingpayment/getlist',bookingpayment_views.get_list, name='booking_payment_list'),
path('bookingpayment/view/<int:id>', bookingpayment_views.view, name='booking_payment.view'),

]