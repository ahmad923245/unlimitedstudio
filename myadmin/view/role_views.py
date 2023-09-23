from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect

from unlimitedstudio.utils import *
from myadmin.forms import *
from myadmin.models import Role
from unlimitedstudio.settings import DATETIME_FORMAT, UPDATE_SUCCESS_MESSAGE, ADD_SUCCESS_MESSAGE


page_name = "Role"
page_url = "role"
    

@login_required
def list(request):
    checkRolePermission(request, page_url + "-list")
    show_add = checkRolePermission(request, page_url + "-add", 0)
    cont = {'page_name': page_name, 'page_url': page_url, 'show_add': show_add}
    return render(request, page_url+'/list.html', cont)


@login_required
def get_list(request):
    checkRolePermission(request, page_url + "-list")
    sortable_columns = ['id', 'title', 'created_date', 'status']
    start = int(request.GET.get('start', 1))
    length = int(request.GET.get('length', 1))
    page = (start/length) + 1
    order_dir = request.GET.get('order[0][dir]')
    order_column = int(request.GET.get('order[0][column]'))
    order_by = sortable_columns[order_column]
    keyword = request.GET.get('search[value]')
    if order_dir == "desc":
        order_by = '-{}'.format(order_by)

    data_list = Role.objects.all().filter(Q(title__icontains=keyword) & Q(
        id__gt=3)).order_by(order_by)
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
        if checkRolePermission(request, page_url + "-edit", 0) == True:
            actions += create_edit(record.id, page_url + '.edit')
        if checkRolePermission(request, page_url + "-view", 0) == True:
            actions += create_view(record.id, page_url + '.view')
        if checkRolePermission(request, page_url + "-delete", 0) == True:
            # actions += create_delete(record.id, page_url + '.delete')
            pass
        actions += '</div>'
        u = {
            'sno': start + i,
            'title': record.title,
            'created_at': record.created_date.strftime(DATETIME_FORMAT),
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


@login_required
def add(request):
    checkRolePermission(request, page_url + "-add")
    form = RoleForm()
    modules = Module.objects.all()
    if request.method == 'POST':
        # print(request.POST)
        # print(request.POST.get('permission'))
        form = RoleForm(request.POST)
        if form.is_valid():
            permissions = form.cleaned_data.get('permission')
            data = Role.objects.create()
            data.title = request.POST.get('title')
            data.status = True
            data.save()
            for permission in permissions:
                perm = Permission.objects.create()
                perm.method_id = permission
                perm.role_id = data.id
                perm.save()
            messages.add_message(request, messages.SUCCESS, ADD_SUCCESS_MESSAGE)
            return redirect(page_url)
        else:
            pass
    cont = {
        'page_name': page_name,
        'page_url': page_url,
        'form': form,
        'modules': modules
    }
    return render(request, page_url+'/add.html', cont)


@login_required
def update_status(request):
    checkRolePermission(request, page_url + "-edit")
    if request.method == 'GET':
        id = request.GET.get('id')
        status = request.GET.get('status')
        data = Role.objects.get(pk=id)
        data.status = status
        data.save()
        response = {
            'status': 'success'
        }
    else:
        response = {
            'status': 'failed'
        }
    return JsonResponse(response)


@login_required
def edit(request, id):
    checkRolePermission(request, page_url + "-edit")
    modules = Module.objects.all()
    if request.method == 'POST':
        print('yes','---------------------136')
        rolePermissions = []
        form = RoleForm(request.POST)
        if form.is_valid():
            data = Role.objects.get(pk=id)
            data.title = request.POST.get('title')
            data.save()
            permissions = form.cleaned_data.get('permission')
            Permission.objects.filter(role_id=id).exclude(method_id__in=permissions).delete()
            for permission in permissions:
                is_exist = Permission.objects.filter(role_id=id,method_id=permission).count()
                if is_exist == 0:
                    perm = Permission.objects.create()
                    perm.method_id = permission
                    perm.role_id = data.id
                    perm.save()
            messages.add_message(request, messages.SUCCESS, UPDATE_SUCCESS_MESSAGE)
            return redirect(page_url)
    else:
        rolePermissions = Permission.objects.filter(role_id=id).all().values_list('method_id', flat=True)
        obj = Role.objects.get(pk=id)
        form = RoleForm(instance=obj)
    cont = {
        'page_name': page_name,
        'page_url': page_url,
        'form': form,
        'modules': modules,
        'rolePermissions': rolePermissions,
        'id': id
    }
    return render(request, page_url+'/edit.html', cont)


@login_required
def view(request, id):
    checkRolePermission(request, page_url + "-view")
    data = Role.objects.get(pk=id)
    modules = Module.objects.all()
    rolePermissions = Permission.objects.filter(role_id=id).all().values_list('method_id', flat=True)
    cont = {
        'page_name': page_name,
        'page_url': page_url,
        'data': data,
        'modules': modules,
        'rolePermissions': rolePermissions
    }
    return render(request, page_url+'/view.html', cont)


@login_required
def delete(request, id):
    checkRolePermission(request, page_url + "-delete")
    if request.method == 'GET':
        data = Role.objects.get(pk=id)
        data.delete()
        Permission.objects.filter(role_id=id).delete()
        response = {
            'status': 'success'
        }
    else:
        response = {
            'status': 'failed'
        }
    return JsonResponse(response)

