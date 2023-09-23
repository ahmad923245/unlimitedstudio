from django.shortcuts import render

# Create your views here.
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
from unlimitedstudio.utils import *
from unlimitedstudio.apiutils import *
from myadmin.forms import UserForm, UserProfileForm, ChangePasswordForm, SubadminForm
from user.models import *
from unlimitedstudio.settings import DATETIME_FORMAT, ADD_SUCCESS_MESSAGE, UPDATE_SUCCESS_MESSAGE, DEFAULT_FROM_EMAIL, APP_NAME, APP_DOMAIN, APP_PROTOCOL
from django.utils.encoding import force_bytes

page_name = "User"
page_url = "user"




@login_required
def list(request):
    user_type = request.GET.get('type')
    if user_type==None:
        return redirect('dashboard')
    checkRolePermission(request, page_url+"-list")
    show_add = checkRolePermission(request, page_url+"-add", 0)
    cont = {'page_name': page_name, 'page_url': page_url, 'show_add': show_add, 'user_type': user_type}
    return render(request, page_url+'/list.html', cont)


from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response

from .serializers import *
from rest_framework.pagination import PageNumberPagination

#-----------------------------------------------------------
from rest_framework_datatables import pagination as dt_pagination
from rest_framework_datatables.django_filters.filters import GlobalFilter
from rest_framework_datatables.django_filters.filterset import DatatablesFilterSet
from rest_framework_datatables.django_filters.backends import DatatablesFilterBackend

# class StandardResultsSetPagination(PageNumberPagination):
#     page_size_query_param = 'limit'

#
def getaction():
    return ""

class Get_list_api(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = User_serializers1
    queryset = User.objects.all().order_by('id')
    #filter_backends = (DatatablesFilterBackend,)


    # ordering_title = 'order'
    # filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    # filterset_fields = {
    #     'first_name': ['iexact'],
    #     'last_name': ['iexact', ],
    # }
    # ordering_fields = ['id', 'first_name', 'last_name', 'email','mobile', 'created_date', 'status']
    # pagination_class = StandardResultsSetPagination
    pagination_class = dt_pagination.DatatablesLimitOffsetPagination
    #search_fields = ['first_name', 'last_name']

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_options(self):
        return 'yes', {}

    class Meta:
        datatables_extra_json = ('get_options',)


@login_required
def get_list(request):
    checkRolePermission(request, page_url + "-list")
    user_type = request.GET.get('type')
    sortable_columns = ['id', 'first_name', 'email', 'role', 'created_date', 'status']
    start = int(request.GET.get('start', 1))
    length = int(request.GET.get('length', 1))
    page = (start/length) + 1
    order_dir = request.GET.get('order[0][dir]')
    order_column = int(request.GET.get('order[0][column]'))
    order_by = sortable_columns[order_column]
    keyword = request.GET.get('search[value]')

    if order_dir == "desc":
        order_by = '-{}'.format(order_by)

    data_list = User.objects.filter(Q(first_name__icontains=keyword)).order_by(order_by).exclude(id=1)



    if user_type == "subadmin":
        data_list = data_list.filter(role_id__gt=3)
    elif user_type == "MUSICIAN":
        data_list = data_list.filter(role_id=2)
    elif user_type == "SERVICE_PROVIDER":
        data_list = data_list.filter(role_id=3)
    else:
        data_list = data_list.filter(Q(role_id=2) | Q(role_id=3))
    paginator = Paginator(data_list, length)

    try:
        records = paginator.page(page)
    except PageNotAnInteger:
        records = paginator.page(1)
    except EmptyPage:
        records = paginator.page(paginator.num_pages)
    i = 1
    datas = []
    for record in records:
        actions = '<div class="btn-group" role="group" aria-label="User Actions">'
        if checkRolePermission(request, page_url + "-edit",0) == True:
            actions += create_edit(record.id, page_url+'.edit', {'type': user_type})
        if checkRolePermission(request, page_url + "-view",0) == True:
            actions += create_view(record.id, page_url+'.view', {'type': user_type})
        if checkRolePermission(request, page_url + "-delete", 0) == True:
            # actions += create_delete(record.id, page_url+'.delete')
            pass
        actions += '</div>'

        if '@social.id' in record.email:
               email=""
        else:
            email=record.email

        u = {
            'sno': start + i,
            'user_name': record.first_name,
            'user_type': str.title(record.role.title).replace("_", " "),
            'email': email,
            'created_date': record.created_date.strftime("%m-%d-%Y"),
            'status': create_status(record.status, record.id, {"1": "Active", "0": "Inactive"}, page_url+'.updateStatus'),
            'actions': actions
        }
        i = i+1
        datas.append(u)
    data = {
        # 'draw': request.draw,
        'recordsFiltered': paginator.count,
        'recordsTotal': paginator.count,
        'data': datas
    }
    return JsonResponse(data)

import stripe
from unlimitedstudio.settings import DEFAULT_FROM_EMAIL, STRIPE_SECRET_KEY

@login_required
def add(request):
    print('hnnhjbhj')
    checkRolePermission(request, page_url + "-add")
    form = SubadminForm()
    user_type = request.GET.get('type')
    if user_type == "user":
        form = UserForm()
    if request.method == 'POST':
        if user_type == "subadmin":
            form = SubadminForm(request.POST, request.FILES)
        else:
            form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            print("OOOOOO")
            data = User.objects.create(role_id=True)
            data.first_name = request.POST.get('first_name')
            data.last_name = ''
            data.email = request.POST.get('email')
            data.mobile=''
            data.gender=request.POST.get('gender')
            # data.profile_image = request.FILES['profile_image']
            data.country_code = ''
            # password = User.objects.make_random_password()
            # print('password', password)
            data.profile_image = ''
            data.strip_Connect_id = ''
            data.set_password(request.POST.get('password'))
            data.role_id = request.POST.get('role')
            data.is_email_verified = True
            data.is_active = True
            data.status = True
            data.save()

            try:
                stripe.api_key = STRIPE_SECRET_KEY

                strip_customer = stripe.Customer.create(
                    description=data.first_name,
                    email=data.email
                )
                data.strip_customer_id = strip_customer.id
                data.save()
                print("MMMMMMMMM")
            except Exception as e:
                strip_customer = str(e)
                print("PPPPP")
                data.strip_customer_id = strip_customer
                data.save()
            messages.add_message(request, messages.SUCCESS, ADD_SUCCESS_MESSAGE)
            base_url = reverse(page_url)
            query_string = urlencode({'type': user_type})
            url = '{}?{}'.format(base_url, query_string)
            return redirect(url)
        else:
            pass
    cont = {
        'page_name': page_name,
        'page_url': page_url,
        'form': form,
        'user_type': user_type,
    }
    return render(request, page_url+'/add.html', cont)


@login_required
def update_status(request):
    checkRolePermission(request, page_url + "-edit")
    if request.method == 'GET':
        id = request.GET.get('id')
        status = request.GET.get('status')
        data = User.objects.get(pk=id)
        data.status = status
        data.is_active = status
        data.save()
        response = {
            'status': 'success'
        }
    else:
        response = {
            'status': 'failed'
        }
    return JsonResponse(response)


from django.http import HttpResponseRedirect
@login_required
def edit(request, id):
    checkRolePermission(request, page_url + "-edit")
    user_type = request.GET.get('type')
    print(user_type, "___________")
    if request.method == 'POST':
        u = User.objects.get(pk=id)
        if user_type == 'subadmin':
            form = SubadminForm(request.POST, request.FILES, instance=u)
        else:
            form = UserForm(request.POST, request.FILES, instance=u)
        if form.is_valid():
            data = User.objects.get(pk=id)
            data.first_name = request.POST.get('first_name')
            # data.last_name = request.POST.get('last_name')
            data.email = request.POST.get('email')
            data.mobile=request.POST.get('phone_number')
            data.gender=request.POST.get('gender')
            data.set_password(request.POST.get('password'))
            data.role_id = request.POST.get('role')

            data.profile_image = ''
            data.strip_Connect_id = ''
            # if user_type == 'subadmin':
            #     data.role_id = request.POST.get('role')
            data.save()
            messages.add_message(request, messages.SUCCESS, UPDATE_SUCCESS_MESSAGE)
            base_url = reverse(page_url)
            query_string = urlencode({'type': user_type})
            url = '{}?{}'.format(base_url, query_string)
            return redirect(url)
    else:
        obj = User.objects.get(pk=id)
        form = UserForm(instance=obj)
    cont = {
        'page_name': page_name,
        'page_url': page_url,
        'form': form,
        'id': id,
        'user_type': user_type,
    }
    return render(request, page_url+'/edit.html', cont)


@login_required
def view(request, id):
    user_type = request.GET.get('type')
    checkRolePermission(request, page_url + "-view")
    data = User.objects.get(pk=id)
    cont = {
        'page_name': page_name,
        'page_url': page_url,
        'data': data,
        'user_type': user_type,
    }
    return render(request, page_url+'/view.html', cont)


@login_required
def delete(request, id):
    checkRolePermission(request, page_url + "-delete")
    if request.method == 'GET':
        data = User.objects.get(pk=id)
        data.delete()
        response = {
            'status': 'success'
        }
    else:
        response = {
            'status': 'failed'
        }
    return JsonResponse(response)
