import stripe
from firebase_admin import messaging
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from unlimitedstudio.apiutils import *
from unlimitedstudio.utils import *
from unlimitedstudio.settings import DEFAULT_FROM_EMAIL, STRIPE_SECRET_KEY
from .serializers import *
from user.models import *
from django.utils.translation import gettext_lazy as _
from myadmin.models import Role

# from unlimitedstudio.utils import serialiser_errors

# def serialiser_errors(serializer):
#     for k, error in serializer.errors.items():
#         print(k, error[0])
#     error_message = " & ".join([f"{k}:-{str(v[0])}" for k, v in serializer.errors.items()])
#     return error_message

import random
def getotp():
    # return 123456
    return random.randint(111111, 999999)


class Sign_up(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def create(self, request):
        stripe.api_key = STRIPE_SECRET_KEY
        serializer = CheckUserSerializers(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email', '')
            # first_name = serializer.validated_data.get('first_name', '')
            # last_name = serializer.validated_data.get('last_name', '')
            # password = serializer.data['password']
            # cpassword = serializer.data['confirm_password']
            # fcm_token = serializer.validated_data.get('fcm_token', '')
            # device_type = serializer.validated_data.get('device_type', '')
            # device_token = serializer.validated_data.get('device_token', '')
            user_type = request.data['user_type']
            print('user_type ', user_type)

            try:
                user_type=Role.objects.get(id=int(user_type)).title
            except:
                user_type='Wrong User type'



            try:
                user = User.objects.get(email=email)
                if user.deleted_account == True:
                    eml = email

                else:
                    m = "Email already exists"
                    s = False
                    d = {}
                    return response_handler(message=m, status=s, data=d)
            except:
                eml = email


            sub = "Hi {},".format('')
            otp = random.randint(111111, 999999)
            # otp = 123456
            user_otp, x = UserOtp.objects.get_or_create(otp_code=otp,
                                                        email=eml)


            msg = "Your OTP For Unlimited Studio Account Verification {}".format(
                otp)
            print(msg)

            m = "Verification OTP send to Email on {}".format(email)
            s = True
            try:
                send_mail(message=msg, from_email=DEFAULT_FROM_EMAIL, subject=sub,
                      recipient_list=[email, ],
                      fail_silently=False, )
            except:
                pass

            return response_handler(message=m, status=s, data={'OTP': otp,'user_type':user_type})
        else:
            m = serialiser_errors(serializer)  # "Error"
            s = False
            d = {}
            return response_handler(message=m, status=s, data=d)


        #     if password == cpassword:
        #         pass
        #     else:
        #         m = "password and confirm_password doesn't match "
        #         s = False
        #         d = {}
        #         return response_handler(message=m, status=s, data=d)

        #     user = User.objects.create(email=eml,
        #                                first_name=first_name,
        #                                last_name=last_name,
        #                                is_active=True,
        #                                is_email_verified=True,
        #                                role_id=user_type)

        #     user.is_superuser = False
        #     user.is_staff = False
        #     user.set_password(password)

        #     user.save()
        #     device_update(user=user, registration_id=fcm_token,
        #                   device_type=device_type, device_id=device_token)
        #     token = Token.objects.create(user=user)

        #     user = User_serializers1(user).data
        #     user['token'] = str(token)

        #     m = "Sign_up Successfull"
        #     s = True
        #     return response_handler(message=m, status=s, data=user)
        # else:
        #     m = serialiser_errors(serializer)  # "Error"
        #     s = False
        #     d = {}
        #     return response_handler(message=m, status=s, data=d)


class Verification_by_Email(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def create(self, request):
        serializer = verify_email_serializers(data=request.data)
        if serializer.is_valid():
            enter_otp = serializer.validated_data.get('enter_otp', None)
            email = serializer.validated_data.get('email', None)
            try:
                first_name = serializer.data['first_name']
            except:
                first_name=''
            last_name = serializer.validated_data.get('last_name', '')
            password = serializer.data['password']
            cpassword = serializer.data['confirm_password']
            fcm_token = serializer.validated_data.get('fcm_token', '')
            device_type = serializer.validated_data.get('device_type', '')
            device_token = serializer.validated_data.get('device_token', '')
            user_type = serializer.validated_data.get('user_type', None)

            # try:
            #     usr = User.objects.get(email=email)
            # except:
            #     m = "Invalid Email Address or Record not Found"
            #     s = False
            #     d = {}
            #     return response_handler(message=m, status=s, data=d)

            user_otp = UserOtp.objects.filter(email=email).last()

            if user_otp == None:
                m = "User OTP doesn't exist Or Expired"
                s = False
                d = {}
                return response_handler(message=m, status=s, data=d)

            if user_otp != None:
                user_email = User.objects.filter(email=email).exclude(
                    is_superuser=True).last()
                if not user_email:
                    if user_otp.otp_code == int(enter_otp):
                        if password == cpassword:
                            pass
                        else:
                            m = "password and confirm_password doesn't match"
                            s = False
                            d = {}
                            return response_handler(message=m, status=s, data=d)
                        usr = User()
                        usr.is_active = True
                        print(usr.is_email_verified, '----------------------132')
                        usr.email=email
                        usr.is_email_verified = True
                        usr.first_name=first_name,
                        usr.last_name=last_name,
                        usr.role_id=user_type
                        usr.is_superuser = False
                        usr.is_staff = False
                        usr.set_password(password)
                        usr.save()
                        stripe.api_key = STRIPE_SECRET_KEY
                        fname = usr.first_name
                        fname = str(fname).strip("()',")
                        print("usr.first_name", usr.first_name)
                        print(fname, '=================================fameafsafsaf')

                        if fname == None:
                            fname = ''
                        usr.first_name = fname
                        usr.save()

                        lname = usr.last_name
                        lname = str(lname).strip("()',")

                        print('lname', lname)
                        if lname == None:
                            lname = ''
                        usr.last_name = lname

                        usr.save()
                        print('user first', usr.first_name)
                        try:
                            name = usr.first_name
                        except:
                            name = " "
                        try:
                            strip_customer = stripe.Customer.create(
                                description=name,
                                email=usr.email
                            )
                            usr.strip_customer_id = strip_customer.id
                            usr.save()
                        except Exception as e:
                            strip_customer = e


                        device_update(user=usr, registration_id=fcm_token,
                                    device_type=device_type, device_id=device_token)
                        try:
                            token = Token.objects.get(user=usr)
                        except:
                            token = Token.objects.create(user=usr)
                        detail = User_serializers1(usr).data
                        detail['token']=str(token)
                        #user_data = {"User": detail.data, "Token": str(token)}
                        user_otp.delete()
                        m = "You've successfully verified your email!"
                        s = True
                        d = {}
                        return response_handler(message=m, status=s, data=detail)
                    else:
                        m = "Invalid OTP"
                        s = False
                        d = {}
                        return response_handler(message=m, status=s, data=d)
                elif user_email and user_email.deleted_account == True:
                    user_email.deleted_account = False
                    user_email.is_active = True
                    user_email.save()
                    d = {}
                    s = False
                    m = "Your account activated Successfully"
                    return response_handler(message=m,
                                            status=s,
                                            data=d)
                d = {}
                s = False
                m = "email already exists!"
                return response_handler(message=m,
                                        status=s,
                                        data=d)
        else:
            m = serialiser_errors(serializer)  # "Error"
            s = False
            d = {}
            return response_handler(message=m, status=s, data=d)


class resend_otp_email(viewsets.ViewSet):  # RESEND OTP EMAIL VERIFICATION
    permission_classes = [AllowAny]

    def create(self, request):
        serializer = resend_email_verification_link_serializers(
            data=request.data)
        if serializer.is_valid():
            #email = serializer.validated_data.get('email', None)
            email = request.data['email']
            user_type = request.data['user_type']
            print('user_type ', user_type)

            try:
                user_type=Role.objects.get(id=int(user_type)).title
            except:
                user_type='Wrong User type'

            try:
                #usr = User.objects.get(email=email)
                otp = getotp()

                # otp = random.randint(1111, 9999)
                uo, create = UserOtp.objects.get_or_create(email=email)
                uo.otp_code = otp
                uo.save()
                print(uo, '------------------210')
                m = "Verification OTP send to Email on {}".format(
                    email)
                s = True
                
                sub = "Hi {}".format(email)
                msg = 'Your OTP For unlimited studio account  verification ' \
                      'is {}'.format(
                    uo.otp_code)
                try:
                    y = send_mail(message=msg, from_email=DEFAULT_FROM_EMAIL,
                                  subject=sub, recipient_list=[email, ],
                                  fail_silently=False, )
                except:
                    pass


                return response_handler(message=m, status=s, data={'OTP': otp,'user_type':user_type})

            except Exception as e:
                m = str(e)
                s = False
                d = {}
                return response_handler(message=m, status=s, data=d)
        else:
            m = serialiser_errors(serializer)
            s = False
            d = {}
            return response_handler(message=m, status=s, data=d)


class LogoutView(viewsets.ViewSet):
    def create(self, request):
        usr = request.user
        try:
            Token.objects.get(user=usr).delete()
            m = " Logout successful"
            s = True
            d = {}
            return response_handler(message=m, status=s, data=d)

        except Exception as e:
            m = str(e)
            s = False
            d = {}
            return response_handler(message=m, status=s, data=d)

from firebase_admin import *
from firebase_admin.messaging import Message
from firebase_admin.messaging import Notification as fNotification


class LoginView(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def create(self, request):
        serializer = login_serializers(data=request.data)

        if serializer.is_valid():
            user_type = serializer.validated_data.get('user_type')
            try:
                email = serializer.validated_data.get('email')
                user = User.objects.get(email=email, role=user_type)
            except:
                email = None
                pass

            # try:
            #     email = serializer.data['user_name']
            #     user = User.objects.get(user_name=email)
            # except:
            #     user_name = None

            device_type = serializer.data['device_type']
            device_token = serializer.validated_data.get('device_token', '')
            fcm_token = serializer.validated_data.get('fcm_token', '')
            password = serializer.data['password']
            try:
                if user:
                    valid_password = user.check_password(password)
                    if valid_password == False:
                        m = "incorrect password"
                        s = False
                        d = {}  # serializer.errors
                        return response_handler(message=m, status=s, data=d)

                    if user.is_email_verified == False:
                        detail = User_serializers1(user)
                        m = "Your Account is Not verified"
                        s = True
                        d = {"User": detail.data, }
                        return response_handler(message=m, status=s, data=d)

                    if user.is_active == False:
                        m = "Your account is deactivated by admin"
                        s = False
                        d = {}
                        return response_handler(message=m, status=s, data=d)

                    if valid_password == False:
                        m = "incorrect password"
                        s = False
                        d = {}  # serializer.errors
                        return response_handler(message=m, status=s, data=d)
                    try:
                        token = Token.objects.get(user=user)
                    except (Exception,):

                        token = Token.objects.create(user=user)
                    device_update(user=user, registration_id=fcm_token,
                                  device_type=device_type,
                                  device_id=device_token)


                    # try:
                    #     if user.strip_customer_id == None or user.strip_customer_id == "":
                    #         stripe.api_key = STRIPE_SECRET_KEY
                    #         strip_customer = stripe.Customer.create(description=user.name, email=user.email)
                    #         print(strip_customer, '=======================122')
                    #         user.strip_customer_id = strip_customer.id
                    #         print('=============125')
                    #         user.save()
                    # except:
                    #     pass

                    detail = User_serializers1(user,context={'user_type': user_type}).data
                    detail['token'] = str(token)
                    try:

                        fcmdevice = FCMDevice.objects.get(
                            user=user)
                        print(fcmdevice,'============169')
                        k = Message(notification=fNotification(
                            title="WTM Now",
                            body="{}...".format("hwllo")))
                        x = fcmdevice.send_message(k)
                    except Exception as e:
                        print(str(e),"429999999999999999999999")
                        print("wdqwdwqdqwdqwdqwdwq")
                    # try:
                    #     device = FCMDevice.objects.get(user=user)
                    #     notification = messaging.Notification(
                    #         title="offline Booking Update",
                    #         body="You receive new booking request",
                    #         image=''
                    #     )
                    #     print("________________________425")
                    #     if device.type == 'ios':
                    #         message = messaging.Message(
                    #             notification=notification,
                    #             data={
                    #                 # 'id': str(booking_id),
                    #                 'title': "Booking Update.",
                    #                 'message': "You receive new booking request.",
                    #                 'type': 'offline Booking',
                    #                 # 'body': str(data_obj.data),
                    #             },
                    #             token=str(device.registration_id))
                    #     else:
                    #         message = messaging.Message(
                    #             # notification=notification,
                    #             data={
                    #                 # 'id': str(booking_id),
                    #                 'title': "Booking Update.",
                    #                 'message': "You receive new booking request.",
                    #                 'type': 'offline Booking',
                    #                 # 'body': str(data_obj.data),
                    #             },
                    #             token=str(device.registration_id))
                    #     device.send_message(message)
                    #     print(device.send_message(message), "________________________449")
                    #     # print('okkkkkkkkkkkkkkkkkkkkkkkkkkk fcm device ', device.registration_id)
                    #     # msg = "ok ----------------------tested {}".format(user.first_name)
                    #     # print('userrrrrrrrrrrrrrrrr id ', user.id)
                    #     # # print(/'msg')
                    #     # xd = device.send_message("signup successfully " ,
                    #     #                          data={"Type": "REQUESTED", "REQUEST_ID": user.id})
                    #     # print("242 ========== ", xd)
                    #     # # user_data = {"User": detail.data, "Token": str(token)}
                    # except Exception as e:
                    #     print(e, "____________________________________________________________________427")
                    #     pass
                    return response_handler(message="Login Successfull",
                                            status=True,
                                            data=detail)  # Response(x.data)
            except Exception as e:
                print(e)
                m = "Invalid email or User name "
                s = False
                d = {}
                return response_handler(message=m, status=s, data=d)
        else:
            m = serialiser_errors(serializer)  # "Error"
            s = False
            d = {}
            return response_handler(message=m, status=s, data=d)


from django.core.mail import send_mail


class ForgotPasswordViewset(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def create(self, request):
        serializer = Forgot_password(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            try:
                user = User.objects.get(email=email)
            except:
                m = "Enter a valid email address"
                s = False
                d = {}
                return response_handler(message=m, status=s, data=d)

            sub = "Hi {},".format('')
            # otp = random.randint(1111, 9999)
            otp = getotp()
            m = "You Will get An OTP verification Email on {}".format(user)
            s = True
            user_otp, created = UserOtp.objects.get_or_create(user_id=user.id,
                                                              email=user.email)
            user_otp.otp_code = otp
            user_otp.save()
            msg = 'Your OTP For ' \
                  'Unlimited Studio account verification is {}'.format(
                user_otp.otp_code)
            try:
                send_mail(message=msg, from_email=DEFAULT_FROM_EMAIL, subject=sub,
                          recipient_list=[email, ],
                          fail_silently=False, )
            except:
                pass

            m = "Otp send successful"
            s = True
            d = {}
            return response_handler(message=m, status=s, data=d)

        # --------------------------------For Email Link------------------------

        '''
           
            subject = "Password Reset Requested"
            email_template_name = "registration/password_reset_email.html"
            c = {
                "email": user.email,
                'domain': email_url,
                'site_name': 'Website',
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "user": user,
                'token': default_token_generator.make_token(user),
                'protocol': 'https',
            }
            email = render_to_string(email_template_name, c)
            try:
                send_mail(subject, email, DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)
                send_mail(message=msg, from_email=DEFAULT_FROM_EMAIL, subject=sub, recipient_list=[email, ],
                          fail_silently=False, )
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            
            '''

        # return Response("hiii ")
        # except:
        #     m = "Invalid email "  # or may be your Account is Not verifyed  "
        #     s = False
        #     d = serializer.errors
        #     return response_handler(message=m, status=s, data=d)

        m = serialiser_errors(serializer)
        s = False
        d = serialiser_errors(serializer)
        return response_handler(message=m, status=s, data=d)


class VerifyForgotOtp(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def create(self, request):
        serializer = verify_email_serializers(data=request.data)
        if serializer.is_valid():
            enter_otp = serializer.validated_data.get('enter_otp', None)
            email = serializer.validated_data.get('email', None)
            try:
                usr = User.objects.get(email=email)
            except:
                m = "Invalid Email Address or Record not Found"
                s = False
                d = {}
                return response_handler(message=m, status=s, data=d)

            user_otp = UserOtp.objects.filter(user_id=usr.id).last()
            print(user_otp)
            if user_otp == None:
                m = "User OTP doesn't exist Or Expired"
                s = False
                d = {}
                return response_handler(message=m, status=s, data=d)

            print(user_otp.otp_code, enter_otp, '-------------------435')
            if user_otp.otp_code == int(enter_otp):
                print(user_otp)
                detail = User_serializers1(usr)
                user_data = detail.data
                user_otp.delete()
                m = "You've successfully verified your OTP"
                s = True
                d = {}
                return response_handler(message=m, status=s, data=user_data)
            else:
                m = "Invalid OTP"
                s = False
                d = {}
                return response_handler(message=m, status=s, data=d)
        else:
            m = serialiser_errors(serializer)  # "Error"
            s = False
            d = {}
            return response_handler(message=m, status=s, data=d)


class ResetPassword(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def create(self, request):
        serializer = SetNewPasswordSerializers(data=request.data)
        if serializer.is_valid():

            user_id = serializer.validated_data.get('user_id', None)
            new_password = serializer.validated_data.get('new_password', None)
            confirm_passsword = serializer.validated_data.get(
                'confirm_passsword', None)

            if new_password != confirm_passsword:
                m = "New password and confirm password not match "
                s = False
                d = {}
                return response_handler(message=m, status=s, data=d)
            try:
                user = User.objects.get(id=user_id)
                user.set_password(new_password)
                user.save()
                m = "Password Set successfully"
                s = True
                d = {}
            except:
                m = "User id Wrong"
                s = False
                d = {}
            return response_handler(message=m, status=s, data=d)
        else:
            m = serialiser_errors(serializer)  # "Error"
            s = False
            d = {}
            return response_handler(message=m, status=s, data=d)


class ChangePassword(viewsets.ViewSet):
    def create(self, request):
        serializer = reset_password_serializers(data=request.data)
        if serializer.is_valid():
            usr = request.user
            old_password = serializer.data['old_password']
            old = usr.check_password(old_password)
            if old == False:
                m = "Incorrect old password"
                s = False
                d = {}
                return response_handler(message=m, status=s, data=d)
            else:
                new_password = serializer.data['new_password']
                confirm_password = serializer.data['confirm_password']
                if new_password == confirm_password:
                    x = User.objects.get(id=usr.id)
                    x.set_password(new_password)
                    x.save()
                    m = "your password has been updated successfully"
                    s = True
                    d = {}
                    return response_handler(message=m, status=s, data=d)
                else:
                    m = "New  password and confirm password are not same"
                    s = False
                    d = {}
                    return response_handler(message=m, status=s, data=d)
        m = "Error "
        s = False
        d = serialiser_errors(serializer)
        return response_handler(message=m, status=s, data=d)


# class SocialLogin(viewsets.ViewSet):
#     permission_classes = [AllowAny]
#     def create(self, request):
#         serializer = social_login(data=request.data)
#         if serializer.is_valid():
#             uid = serializer.validated_data.get('uid')
#             first_name = serializer.validated_data.get('first_name', '')
#             login_type = serializer.validated_data.get('login_type', '')
#             device_type = serializer.validated_data.get('device_type', '')
#             device_token = serializer.validated_data.get('device_token', '')
#             email = serializer.validated_data.get('email', None)
#             image_link = serializer.validated_data.get('image_link', None)
#             user_type = serializer.validated_data.get('user_type')
#
#             if email == None:
#                 email = serializer.data['uid'] + "@social.id"
#
#             try:
#                 usr = SocialLoginUser.objects.get(uid=uid)
#                 print(" social login user found")
#                 x = User_serializers1(usr.user)
#                 token, created = Token.objects.get_or_create(user=usr.user)
#                 x = {"User": x.data, "Token": str(token)}
#                 return response_handler(message="successful", status=True,
#                                         data=x)  # Response(x.data)
#             except:
#                 mobile = serializer.validated_data.get('mobile', uid)
#                 try:
#                     user = User.objects.create(email=email,
#                                                is_active=True, mobile=mobile,
#                                                is_sociallogin=True,
#                                                image_link=image_link,
#                                                first_name=first_name,
#                                                user_type=user_type
#                                                )
#
#                 except Exception as e:
#                     try:
#                         user = User.objects.get(email=email)
#                         slu = SocialLoginUser.objects.get(user=user)
#                         m = "You are already with us with your {} account  ".format(
#                             slu.provider)
#                         return response_handler(message=m, status=False,
#                                                 data={})
#                     except:
#                         pass
#
#                 try:
#                     profile_image = request.FILES.get('profile_image')
#                     user.profile_image = profile_image
#                     user.save()
#                 except:
#                     pass
#                 SocialLoginUser.objects.create(user=user, uid=uid,
#                                                provider=login_type)
#                 token, x = Token.objects.get_or_create(user=user)
#                 x = User_serializers1(user)
#                 x = {"User": x.data, "Token": str(token)}
#                 return response_handler(message="successful", status=True,
#                                         data=x)  # Response(x.data)
#         else:
#             m = serialiser_errors(serializer)  # "Error"
#             s = False
#             d = {}
#             return response_handler(message=m, status=s, data=d)


class view_profile(viewsets.ViewSet):

    def list(self, request):
        usr = request.user
        try:
            user_data = User.objects.get(id=usr.id)
            user_details = User_serializers1(user_data)
            m = "successful"
            s = True
            d = user_details.data
            return response_handler(message=m, status=s, data=d)
        except:
            m = "Invalid Token or token may be Expired either deleted "
            s = False
            d = {}
            return response_handler(message=m, status=s, data=d)


class update_profile(viewsets.ViewSet):

    def create(self, request):
        usr = request.user
        serializer = update_profile_serializer(usr, data=request.data,
                                               partial=True)
        if serializer.is_valid():
            x = serializer.save()
            token, created = Token.objects.get_or_create(user=x)
            detail = User_serializers1(x).data
            detail['token'] = str(token)

            m = "Profile updated successfully"
            s = True
            d = detail
            return response_handler(message=m, status=s, data=d)

        else:
            m = serialiser_errors(serializer)  # "Error"
            s = False
            d = {}
            return response_handler(message=m, status=s, data=d)


class SocialSignupViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]

    def create(self, request):
        serializer = SocialSignupSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user_type = serializer.validated_data.get('user_type')

                social_type = serializer.validated_data.get('social_type')
                social_id = serializer.validated_data.get('social_id')
                user = User.objects.filter(social_type=social_type,
                                           social_id=social_id).first()


                if user is None:
                    email = serializer.validated_data.get('email',
                                                          social_id + "@social.id")

                    country_code = serializer.validated_data.get(
                        'country_code', '')

                    mobile = serializer.validated_data.get('mobile', '')

                    if email != "":
                        user = User.objects.filter(email=email).first()
                        if user is None:
                            pass
                        else:
                            user.social_type = social_type
                            user.social_id = social_id
                            user.save()
                    elif country_code != "" and mobile != "":
                        user = User.objects.filter(country_code=country_code,
                                                   mobile=mobile).first()
                        if user is None:
                            pass
                        else:
                            user.social_type = social_type
                            user.social_id = social_id
                            user.save()
                    if user is None:
                        first_name = serializer.validated_data.get(
                            'first_name', '')
                        last_name = serializer.validated_data.get('last_name',
                                                                  '')

                        try:
                            profile_image = request.FILES.get('profile_image')
                        except:
                            profile_image = ''

                        user = User.objects.create(role_id=user_type,
                                                   first_name=first_name,
                                                   last_name=last_name,
                                                   email=email,
                                                   country_code=country_code,
                                                   mobile=mobile,
                                                   social_type=social_type,
                                                   social_id=social_id,
                                                   status=True,
                                                   )
                        user.is_active = True
                        user.is_sociallogin = True
                        user.is_email_verified = True
                        user.profile_image=profile_image
                        user.save()

                        stripe.api_key = STRIPE_SECRET_KEY
                        print(" stripe.api_key ",  stripe.api_key )
                        try:
                            name = user.name
                        except:
                            name = " "
                        try:
                            strip_customer = stripe.Customer.create(
                                description=name,
                                email=user.email
                            )
                        except Exception as e:
                            strip_customer = e
                        acc = None
                        try:
                            u = User.objects.get(id=user.id)
                            u.strip_customer_id = strip_customer.id
                            u.save()
                        except:
                            pass

                # user_device = UserDevice.objects.create()
                # user_device.device_type = serializer.data['device_type']
                # user_device.device_id = serializer.data['device_id']
                # user_device.user_id = user.id
                # user_device.save()

                if user.role.id != int(user_type):
                    return Response({
                        'status': False,
                        'data': {},
                        'message': 'Already Registered with Musician/Service'
                    })

                token, create = Token.objects.get_or_create(user=user)
                print(token, '---------------------660')
                try:
                    fcm_token = request.data['device_token']
                    device_id = request.data['device_id']
                    device_type = request.data['device_type']
                    device_update(user=user, registration_id=fcm_token,
                                  device_type=device_type, device_id=device_id)
                except Exception as e:
                    print(str(e))

                print(user.strip_customer_id, "______________strip_customer_id")
                user=User.objects.get(id=user.id)
                user = User_serializers1(user)
                user = dict(user.data)

                user['token'] = str(token)
                print(user, "______________________USER")

                return Response({
                    'status': True,
                    'data': user,
                    'message': 'Signed in successfully'
                })
            except Exception as e:
                print(e)
                return Response({
                    'status': False,
                    'data': [],
                    'message': _('something_wrong')
                })
        else:
            return Response({
                'status': False,
                'data': [],
                'message': getErrorMessage(serializer.errors)
            })


class DeleteAccountViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            user = request.user
            user = User.objects.get(id=user.id)
            user.delete()
            # user.is_active = False
            # user.deleted_account = True
            # user.save()
            m = "Account Deleted successfully"
            s = True
            d = []
            return response_handler(message=m, status=s, data=d)

        except:
            m = "Something went wrong"
            s = False
            d = {}
            return response_handler(message=m, status=s, data=d)


class AppSettingViewset(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = SettingSerializer
    def list(self,request):
        admin_obj = VersionControl.objects.all()
        data= self.serializer_class(admin_obj,many=True)
        try:
            data=data.data[0]
        except:
            data = {}

        message = "List fetched successfully"
        return Response({'status': True, 'message': message,'data':data })


from fcm_django.models import FCMDevice

class FCMDeviceViewset(viewsets.ViewSet):
    def create(self, request, *args, **kwargs):
        serializer = FCMSerializer(data=request.data)
        try:
            print("___________2222222222222")
            if serializer.is_valid():
                print("____________________!!!!111111")
                usr = request.user
                print(usr, "______________99999")
                registration_id = request.data['registration_id']
                device_id = request.data['device_id']
                device_type = request.data['device_type']
                device = FCMDevice.objects.get(user=usr)
                device.registration_id = registration_id
                device.type = device_type
                print('hiiiiiiiiiiiiiiiiiiiiiiiiiii', device.type)
                device.device_id = device_id
                print('ggggggggggggggggggggggggggg', device.device_id)
                device.active = True
                device.save()
                m ="successfully updated"
                s = True
                d = request.data
                # d = {'registration_id':registration_id,'device_id':device_id}
                # d = FCMSerializer(device).data

                return response_handler(message=m, status=s, data=d)
        except Exception as e:
            print(str(e))
            return  response_handler(message=str(e), status=False, data={})
