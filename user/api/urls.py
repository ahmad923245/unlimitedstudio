from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'sign_up', Sign_up,basename='sign_up')#done ok

router.register(r'verification', Verification_by_Email,basename='verification')#done ok
router.register(r'resend_otp_email', resend_otp_email,basename='resend_otp_email')#done

router.register(r'login', LoginView,basename='login')#done
router.register(r'social_login', SocialSignupViewSet,basename='socialLogin') #done
router.register(r'logout', LogoutView,basename='logout')#done
#-------------------------------------------Forget_Password------------------------------
router.register(r'forgot_password', ForgotPasswordViewset,
                basename='forgot_password')# Done
router.register(r'verify_forgot_otp', VerifyForgotOtp,
                basename='verify_forgot_otp')# Done
router.register(r'reset_password', ResetPassword,
                basename='reset_password') #Done
#-----------------------------------------------------------------------------------------------
router.register(r'change_password', ChangePassword,
                basename='change_password')# Done
router.register(r'view_profile', view_profile,basename='view_profile') # Done
router.register(r'update_profile', update_profile,basename='update_profile') # Done
router.register(r'delete_account', DeleteAccountViewset,basename='delete_account') # Done
router.register(r'version_settings', AppSettingViewset,basename='version_settings') # Done
router.register(r'fcm_update', FCMDeviceViewset,basename='fcm_update') # Done




urlpatterns = router.urls

