from django.contrib import messages
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.tokens import default_token_generator
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail, EmailMultiAlternatives
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.html import format_html

from django.utils.http import urlsafe_base64_encode, urlencode
from myadmin.forms import UserForm, UserProfileForm, ChangePasswordForm, SubadminForm
from user.models import *
from booking.models import *
from unlimitedstudio.settings import DATETIME_FORMAT, ADD_SUCCESS_MESSAGE, UPDATE_SUCCESS_MESSAGE, DEFAULT_FROM_EMAIL, APP_NAME, \
    APP_DOMAIN, APP_PROTOCOL
from django.utils.encoding import force_bytes

page_name = "User"
page_url = "user"



from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.hashers import check_password


# class Login(View):
#     def get(self, request):
#
#         return render(request, 'auth/login.html')
#
#     def post(self, request):
#
#         error_message = None
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         user = authenticate(email=email, password=password)
#         if user:
#             if user.role_id == 2:
#                 messages.add_message(request, messages.ERROR, "Invalid credentials")
#             elif user.status:
#                 login(request, user)
#                 return redirect('dashboard')
#             else:
#                 messages.add_message(request, messages.ERROR, "Your account is inactive, please contact to admin!")
#         else:
#             user = User.objects.filter(email=email).first()
#             if not user:
#                 messages.add_message(request, messages.ERROR, "User does not exist")
#             elif not user.is_active:
#                 messages.add_message(request, messages.ERROR,
#                                      "Your account has been deactivated, please contact to admin")
#             else:
#                 messages.add_message(request, messages.ERROR, "Invalid credentials")
#
#         return render(request, 'auth/login.html', {'error': error_message})

def showLogin(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        return render(request, 'auth/login.html')

def checkLogin(request):
    if request.method == 'POST':

        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if user:
            if user.role_id == 2:
                messages.add_message(request, messages.ERROR, "Invalid credentials")
            elif user.status:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.add_message(request, messages.ERROR, "Your account is inactive, please contact to admin!")
        else:
            user = User.objects.filter(email=email).first()
            if not user:
                messages.add_message(request, messages.ERROR, "User does not exist")
            elif not user.is_active:
                messages.add_message(request, messages.ERROR, "Your account has been deactivated, please contact to admin")
            else:
                messages.add_message(request, messages.ERROR, "Invalid credentials")

        return redirect('login')

    return HttpResponse('check user credentials')


@login_required
def dashboard(request):
    musician = User.objects.filter(role_id=2).count()
    service_provider = User.objects.filter(role_id=3).count()
    user_count = musician + service_provider
    booking = Booking.objects.all().count()
    cont = {
        'user_count': user_count,
        'musician': musician,
        'service_provider': service_provider,
        'booking': booking,
        'page_name': 'Dashboard',
        'page_url': 'dashboard'
    }
    return render(request, 'dashboard.html',cont)


@login_required
def profile(request):
    if request.method == 'POST':

        u = User.objects.get(pk=request.user.id)
        form = UserProfileForm(request.POST, instance=u)
        if form.is_valid():

            data = User.objects.get(pk=request.user.id)
            data.first_name = request.POST.get('first_name')
            data.last_name = request.POST.get('last_name')

            if len(request.FILES) != 0:
                image = request.FILES['image']
                print('image',image)
                # print('image',image)
                # fs = FileSystemStorage()
                # filename = fs.save(image.name, image)
                # uploaded_file_url = fs.url(filename)
                # print('uploaded_file_url', uploaded_file_url)
                data.profile_image = image
                print(data.profile_image,'-----------------')
            data.save()
            # print(data.profile_image, '-----------------')
            messages.add_message(request, messages.SUCCESS, UPDATE_SUCCESS_MESSAGE)
            return redirect('profile')
    else:
        obj = User.objects.get(pk=request.user.id)
        form = UserProfileForm(instance=obj)
    cont = {'page_name': 'Profile',
            'page_url': 'profile',
            'form': form
            }
    return render(request, 'profile.html', cont)


@login_required
def change_password(request):
    if request.method == 'POST':
        u = User.objects.get(pk=request.user.id)
        form = ChangePasswordForm(request.POST, instance=u)

        if form.is_valid():
            current_password = request.POST.get('current_password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            if new_password != confirm_password:
                messages.add_message(request, messages.ERROR, 'New Password and Confirm Password does not match')
            elif not u.check_password(current_password):
                messages.add_message(request, messages.ERROR, 'Current Password is not valid')
            else:
                data = User.objects.get(pk=request.user.id)
                data.set_password(new_password)
                data.save()
                messages.add_message(request, messages.SUCCESS, 'Password changed successfully')
            return redirect('change_password')
    else:
        obj = User.objects.get(pk=request.user.id)
        form = ChangePasswordForm(instance=obj)
    cont = {'page_name': 'Change Password',
            'page_url': 'dashboard',
            'form': form
            }
    return render(request, 'change_password.html', cont)


@login_required
def Logout(request):
    logout(request)
    return redirect('login')


def forgotPassword(request):
    x=0
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            subject = "Password Reset Requested"
            email_template_name = "mails/password_reset_email.html"
            data = {
                "email": user.email,
                'domain': APP_DOMAIN,
                'site_name': APP_NAME,
                "uid": urlsafe_base64_encode(force_bytes(user.id)),
                "user": user,
                'token': default_token_generator.make_token(user),
                'protocol': APP_PROTOCOL,
            }
            email = render_to_string(email_template_name, data)

            html_content = format_html(email)
            send_mail(subject, html_content, DEFAULT_FROM_EMAIL, [user.email], html_message=html_content, fail_silently=False)
            # print('email',email)
            messages.add_message(request, messages.SUCCESS, "We've emailed you instructions for setting your password.")
        else:
            messages.add_message(request, messages.ERROR, "Invalid email")
        return redirect('forgotPassword')
    return render(request, 'auth/forgot_password.html')
