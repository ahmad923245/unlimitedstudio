from rest_framework.routers import DefaultRouter
from .views import *
from django.urls import path, include

router = DefaultRouter()
router.register(r'manage_booking', BookingViewsets,basename='BookingAppointment')
router.register(r'booking_listing', BookingTypeListViewSet,basename='Booking Listing')
router.register(r'musician_booking_listing', BookingType_MusicianList_ViewSet,basename='Musician_Booking Listing')
router.register(r'recent_booking_listing', RecentBookingListViewSet,basename='Recent Booking Listing')
router.register(r'stripe_connect', stripe_connect, basename='stripe_connect')
router.register(r'paymentintent', PaymentIntentViewset, basename='paymentintent')
router.register(r'transaction_history', MyTransactionViewset,basename='transaction_history'),
router.register(r'stripe_booking_payment', StripeBookingPayment,basename='stripe_booking_payment'),
router.register(r'musician_cancle_booking', MusicianCancleBooking,basename='MusicianCancleBooking'),
router.register(r'serviceprovider_cancel_booking', Service_ProviderBookingCancel,basename='ServiceProviderCancalBooking'),
router.register(r'serviceprovider_payout_transaction', ServiceProviderPayoutTransaction,basename='serviceprovider_payout_transaction'),
router.register(r'user_notification', UserNotificationViewset,basename='user_notification'),
router.register(r'notification_count', CheckNotificationViewsets,basename='notification_count'),


urlpatterns = router.urls

urlpatterns = [
path('', include(router.urls)),
path('',include('booking.urls')),
path("cron/", today_bookings, name='cron'),



path("stripe/", stripe_view, name='stripe'),
path("stripe_successfully/", stripe_successfully,
     name='stripe_successfully'),


]






