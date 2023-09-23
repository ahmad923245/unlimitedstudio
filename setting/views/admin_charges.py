from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from ..forms import *
from ..models import *
from unlimitedstudio.settings import DATETIME_FORMAT, UPDATE_SUCCESS_MESSAGE, ADD_SUCCESS_MESSAGE
from unlimitedstudio.utils import *


page_name = "Admin Charges"
page_url = "admin_charges"




@login_required
def list(request):
    checkRolePermission(request, page_url + "-list")
    show_add = checkRolePermission(request, page_url + "-add", 0)
    cont = {'page_name': page_name, 'page_url': page_url, 'show_add': show_add}
    return render(request, page_url+'/list.html', cont)


@login_required
def get_list(request):
    checkRolePermission(request, page_url + "-list")
    sortable_columns = ['id', 'admin_percentes']
    start = int(request.GET.get('start', 1))
    length = int(request.GET.get('length', 1))
    page = (start/length) + 1
    order_dir = request.GET.get('order[0][dir]')
    order_column = int(request.GET.get('order[0][column]'))
    order_by = sortable_columns[order_column]
    keyword = request.GET.get('search[value]')
    if order_dir == "desc":
        order_by = '-{}'.format(order_by)
    data_list = AdminCharges.objects.all()
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
        actions += '</div>'
        u = {
            'sno': start + i,
            'admin_charges': record.admin_percentes,
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
    form = AdminChargesForm()
    if request.method == 'POST':
        form = AdminChargesForm(request.POST)
        if form.is_valid():
            data=form.save(commit=False)
            data.status = True
            data.save()
            messages.add_message(request, messages.SUCCESS, ADD_SUCCESS_MESSAGE)
            return redirect(page_url)
        else:
            pass
    cont = {
        'page_name': page_name,
        'page_url': page_url,
        'forms': form
    }
    return render(request, page_url+'/add.html', cont)


@login_required
def edit(request, id):
    checkRolePermission(request, page_url + "-edit")
    obj = get_object_or_404(AdminCharges, id=id)
    form = AdminChargesForm(request.POST or None, instance=obj)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, UPDATE_SUCCESS_MESSAGE)
            return redirect(page_url)
    cont = {
        'page_name': page_name,
        'page_url': page_url,
        'forms': form,
        'id': id
    }
    return render(request, page_url+'/edit.html', cont)


@login_required
def view(request, id):
    checkRolePermission(request, page_url + "-view")
    data = AdminCharges.objects.get(pk=id)
    cont = {
        'page_name': page_name,
        'page_url': page_url,
        'data': data
    }
    return render(request, page_url+'/view.html', cont)












