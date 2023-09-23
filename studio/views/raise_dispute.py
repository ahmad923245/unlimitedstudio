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


page_name = "Raise Dispute"
page_url = "raise_dispute"




@login_required
def list(request):
    checkRolePermission(request, page_url + "-list")
    show_add = checkRolePermission(request, page_url + "-add", 0)
    cont = {'page_name': page_name, 'page_url': page_url, 'show_add': show_add}
    return render(request, page_url+'/list.html', cont)


@login_required
def get_list(request):
    checkRolePermission(request, page_url + "-list")
    sortable_columns = ['id', 'musician', 'status', 'created_at']
    start = int(request.GET.get('start', 1))
    length = int(request.GET.get('length', 1))
    page = (start/length) + 1
    order_dir = request.GET.get('order[0][dir]')
    order_column = int(request.GET.get('order[0][column]'))
    order_by = sortable_columns[order_column]
    keyword = request.GET.get('search[value]')
    if order_dir == "desc":
        order_by = '-{}'.format(order_by)
    print('==================================39')
    data_list = RaiseDispute.objects.filter(Q(musician__first_name__icontains=keyword)).order_by(order_by)
    print(data_list,'==============================41')
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
            'musician': record.musician.first_name,
            'studio' : record.studio.studio_name,
            'status': create_status(record.status, record.id, {"1": "Active", "0": "Inactive"}, page_url+'.updateStatus'),
            'created_at': record.created_at.strftime(DATETIME_FORMAT),
            'actions': actions
        }
        i = i+1
        datas.append(u)

        print(record.comment, "_______74")

    data = {
        # 'draw': request.draw,
        'recordsFiltered': paginator.count,
        'recordsTotal': paginator.count,
        'data': datas
    }
    return JsonResponse(data)


@login_required
def update_status(request):
    checkRolePermission(request, page_url + "-edit")
    if request.method == 'GET':
        id = request.GET.get('id')
        status = request.GET.get('status')
        data = RaiseDispute.objects.get(pk=id)
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
    obj = get_object_or_404(RaiseDispute, id=id)
    form = RaiseDisputeForm(request.POST or None, instance=obj)
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
    data = RaiseDispute.objects.get(pk=id)
    cont = {
        'page_name': page_name,
        'page_url': page_url,
        'data': data
    }
    return render(request, page_url+'/view.html', cont)
