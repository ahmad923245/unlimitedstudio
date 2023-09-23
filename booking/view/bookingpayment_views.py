from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

# from booking.forms import BookingForm
from booking.models import BookingPayment
from unlimitedstudio.settings import DATETIME_FORMAT, UPDATE_SUCCESS_MESSAGE, ADD_SUCCESS_MESSAGE
from unlimitedstudio.utils import *


page_name = "BookingsPayment"
page_url = "booking_payment"




@login_required
def list(request):
    print('safsadsd')
    checkRolePermission(request, page_url + "-list")
    show_add = checkRolePermission(request, page_url + "-add", 0)
    cont = {'page_name': page_name, 'page_url': page_url, 'show_add': show_add}
    return render(request, page_url+'/list.html', cont)


@login_required
def get_list(request):
    checkRolePermission(request, page_url + "-list")
    sortable_columns = ['id', 'studio', 'musician', 'transaction_id']
    start = int(request.GET.get('start', 1))
    length = int(request.GET.get('length', 1))
    page = (start/length) + 1
    order_dir = request.GET.get('order[0][dir]')
    order_column = int(request.GET.get('order[0][column]'))
    order_by = sortable_columns[order_column]
    keyword = request.GET.get('search[value]')
    if order_dir == "desc":
        order_by = '-{}'.format(order_by)
    data_list = BookingPayment.objects.all().filter(Q(studio__studio_name__icontains=keyword)).order_by(order_by)
    paginator = Paginator(data_list, length)

    try:
        records = paginator.page(page)
    except PageNotAnInteger:
        records = paginator.page(1)
    except EmptyPage:
        records = paginator.page(paginator.num_pages)
    i = 1
    datas = []
    # print(checkRolePermission(request, page_url + "-edit", 0))
    for record in records:
        actions = '<div class="btn-group" role="group" aria-label="User Actions">'
        if checkRolePermission(request, page_url + "-edit", 0) == True:
            pass
            #actions += create_edit(record.id, page_url + '.edit')
        if checkRolePermission(request, page_url + "-view", 0) == True:
            actions += create_view(record.id, page_url + '.view')
        if checkRolePermission(request, page_url + "-delete", 0) == True:
            pass
            #actions += create_delete(record.id, page_url+'.delete')
        actions += '</div>'
        u = {
            'sno': start + i,
            'name': record.studio.studio_name,
            'musician':record.musician.first_name,
            'transaction_id':record.transaction_id,
            'booking': record.booking.id,
            'cashout_status':record.cashout_status,
            'amount': record.amount,
            'admincommision': record.admincommision,
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
def view(request, id):
    # user_type = request.GET.get('type')
    checkRolePermission(request, page_url + "-view") 
    data = BookingPayment.objects.get(pk=id)
    cont = {
        'page_name': page_name,
        'page_url': page_url,
        'data': data,
    }
    return render(request, page_url+'/view.html', cont)








