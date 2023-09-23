"""
all common function to use is all over the application
"""

from urllib.parse import urlencode
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlsafe_base64_encode
from myadmin.models import Permission, Method
from unlimitedstudio.settings import *
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from django.utils.encoding import force_bytes

def create_status(status, id, options, page_url):
    page_url = reverse(page_url)
    status = int(status)
    html = '<select class="form-control changeStatus" data-id="'+str(id)+'" data-path="'+page_url+'" style="width:100px;">'
    for key in options:
        selected = ''
        if status == int(key):
            selected = 'selected="selected"'
        html += '<option data-key="'+str(key)+'" data-status="'+str(status)+'" value="'+key+'" '+selected+'>'+options[key]+'</option>'
    html += '</select>'
    return html


def create_delete(id, page_url):
    page_url = reverse(page_url, kwargs={"id": id})
    html = '<a href="javascript:void(0)"'
    html += 'class="btn btn-xs btn-danger deleteRecord" title="Delete" data-msg="Do you really want to delete?"'
    html += 'data-route="'+page_url+'"><i class="fas fa-trash"></i></a>'
    return html


def create_edit(id, page_url, query_string=''):
    page_url = reverse(page_url, kwargs={"id": id})
    if query_string != '':
        query_string = urlencode(query_string)
        page_url = '{}?{}'.format(page_url, query_string)
    html = '<a href="'+page_url+'" class="btn btn-xs btn-primary" title="Edit"><i class="fas fa-edit"></i></a>'
    return html


def create_view(id, page_url, query_string=''):
    page_url = reverse(page_url, kwargs={"id": id})
    if query_string != '':
        query_string = urlencode(query_string)
        page_url = '{}?{}'.format(page_url, query_string)
    html = '<a href="'+page_url+'" class="btn btn-xs btn-warning" title="Edit"><i class="fas fa-eye"></i></a>'
    return html


def checkRolePermission(request, permission, screen=1):
    current_role_id = request.user.role_id
    if current_role_id == 1:
        return True
    else:
        method = Method.objects.filter(name=permission).first()
        if method is None:
            if screen == 1:
                raise PermissionDenied
                # messages.add_message(request, messages.ERROR, PERMISSION_DENIED_MESSAGE)
                # render(request,'./dashboard.html')
                return False
            else:
                return False
        else:
            is_allow = Permission.objects.filter(method_id=method.id, role_id=request.user.role_id).count()
            if is_allow == 0:
                if screen == 1:
                    raise PermissionDenied
                    # messages.add_message(request, messages.ERROR, PERMISSION_DENIED_MESSAGE)
                    # render(request,'./dashboard.html')
                    return False
                else:
                    return False
            else:
                return True



def getErrorMessage(messages):
    print('messages', messages)
    message = ''
    for i in messages:
        print('i is ', i)
        if message == '':
            message = messages[i][0].replace('This', i.capitalize().replace('_', ' '))
        else:
            break
    return message

def generateRandomOTP():
    return 123456
    # return randrange(999999)

def sendOTP(message, recipient):
    print('message',message)
    print('recipient',recipient)
    return True


def sendEmailOTP(otp_code, user):
    subject = "Password Reset OTP"
    email_template_name = "mails/password_reset_otp.html"
    data = {
        "otp_code": otp_code,
        "user": user,
        'site_name': APP_NAME,
    }
    email = render_to_string(email_template_name, data)
    html_content = format_html(email)
    send_mail(subject, html_content, DEFAULT_FROM_EMAIL, [user.email], html_message=html_content, fail_silently=False)


def sendVerificationEmail(user):
    subject = "Verify your Email"
    email_template_name = "mails/verify_email.html"
    data = {
        "email": user['email'],
        'domain': APP_DOMAIN,
        'site_name': APP_NAME,
        "uid": urlsafe_base64_encode(force_bytes(str(user['id']))),
        "user": user,
        'protocol': APP_PROTOCOL,
    }
    email = render_to_string(email_template_name, data)
    html_content = format_html(email)
    send_mail(subject, html_content, DEFAULT_FROM_EMAIL, [user['email']], html_message=html_content, fail_silently=False)

#
# def custom_exception_handler(exc, context):
#     if isinstance(exc, NotAuthenticated):
#         return Response({
#             'status': False,
#             'data': {},
#             'message': 'Invalid token'
#         }, status=401)
#
#     elif isinstance(exc, AuthenticationFailed):
#         return Response({
#             'status': False,
#             'data': {},
#             'message': 'Invalid token'
#         }, status=401)
#     # default case
#     return exception_handler(exc, context)

def thumbimage_resize(original_image):
    img_io = BytesIO()
    original_image = Image.open(original_image)
    original_image.thumbnail((50, 50))
    original_image.save(img_io, format='JPEG')
    img_content = ContentFile(img_io.getvalue(), 'thumbs.jpg')
    return img_content


def thumbmediumimage_resize(original_image):
    img_io = BytesIO()
    original_image = Image.open(original_image)
    original_image.thumbnail((512, 512))
    original_image.save(img_io, format='JPEG')
    img_content = ContentFile(img_io.getvalue(), 'thumbs_medium.jpg')
    return img_content


# from django.shortcuts import render
# from django.utils.http import urlsafe_base64_decode
# from user.models import User
#
# def verifyEmail(request, *args, **kwargs):
#     if 'uidb64' not in kwargs:
#         return render(request, '404.html')
#     try:
#         uidb64 = kwargs['uidb64']
#         uid = urlsafe_base64_decode(uidb64).decode()
#
#         data = User.objects.get(pk=uid)
#         data.email_verified = True
#         data.save()
#         return render(request, 'email_verify.html')
#     except:
#         return render(request, '404.html')
