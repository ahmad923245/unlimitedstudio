from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from booking.forms import BookingForm
from booking.models import Booking
from unlimitedstudio.settings import DATE_FORMAT, UPDATE_SUCCESS_MESSAGE, ADD_SUCCESS_MESSAGE
from unlimitedstudio.utils import *


page_name = "Bookings"
page_url = "booking"




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
    sortable_columns = ['id', 'studio', 'musician', 'paid_amount', 'appointment_date', 'cashout_status', 'payment_status', 'accepted', 'cancelled', 'decline']
    start = int(request.GET.get('start', 1))
    length = int(request.GET.get('length', 1))
    page = (start/length) + 1
    order_dir = request.GET.get('order[0][dir]')
    order_column = int(request.GET.get('order[0][column]'))
    order_by = sortable_columns[order_column]
    keyword = request.GET.get('search[value]')
    if order_dir == "desc":
        order_by = '-{}'.format(order_by)
    data_list = Booking.objects.filter(Q(studio__studio_name__icontains=keyword) | Q(musician__first_name__icontains=keyword) | Q(paid_amount__icontains=keyword) | Q(appointment_date__icontains=keyword) | Q(cashout_status__icontains=keyword) | Q(payment_status__icontains=keyword) | Q(accepted__icontains=keyword) | Q(cancelled__icontains=keyword) | Q(decline__icontains=keyword)).order_by(order_by)

    print(data_list, "___________44")
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
            'booking': record.id,
            'name': record.studio.studio_name,
            'musician': record.musician.first_name,
            'cost': record.paid_amount,
            'appointment_date': record.appointment_date.strftime(DATE_FORMAT),
            'cashout_status': record.cashout_status,
            'payment_status': record.payment_status.replace('succeeded', 'Paid'),
            'accepted': record.accepted,
            'cancelled': record.cancelled,
            'decline': record.decline,
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


# @login_required
# def add(request):
#     checkRolePermission(request, page_url + "-add")
#     form = BookingForm()
#     if request.method == 'POST':
#         form = BookingForm(request.POST)
#         if form.is_valid():
#             print('------------------89')
#             form.save()
#             # data.status = True
#             # data.save()
#             messages.add_message(request, messages.SUCCESS, ADD_SUCCESS_MESSAGE)
#             return redirect(page_url)
#         else:
#             pass
#     cont = {
#         'page_name': page_name,
#         'page_url': page_url,
#         'forms': form
#     }
#     return render(request, page_url+'/add.html', cont)


# @login_required
# def update_status(request):
#     checkRolePermission(request, page_url + "-edit")
#     if request.method == 'GET':
#         id = request.GET.get('id')
#         status = request.GET.get('status')
#         data = Booking.objects.get(pk=id)
#         data.status = status
#         data.save()
#         response = {
#             'status': 'success'
#         }
#     else:
#         response = {
#             'status': 'failed'
#         }
#     return JsonResponse(response)


# @login_required
# def edit(request, id):
#     print('============129')
#     checkRolePermission(request, page_url + "-edit")
#     obj = get_object_or_404(Booking, id=id)
#     form = BookingForm(request.POST or None, instance=obj)
#     if request.method == 'POST':
#         if form.is_valid():
#             form.save()
#             messages.add_message(request, messages.SUCCESS, UPDATE_SUCCESS_MESSAGE)
#             return redirect(page_url)
#     cont = {
#         'page_name': page_name,
#         'page_url': page_url,
#         'forms': form,
#         'id': id
#     }
#     return render(request, page_url+'/edit.html', cont)


# @login_required
# def view(request, id):
#     checkRolePermission(request, page_url + "-view")
#     data = Booking.objects.get(pk=id)
#     cont = {
#         'page_name': page_name,
#         'page_url': page_url,
#         'data': data
#     }
#     return render(request, page_url+'/view.html', cont)
@login_required
def view(request, id):
    # user_type = request.GET.get('type')
    checkRolePermission(request, page_url + "-view") 
    data = Booking.objects.get(pk=id)
    cont = {
        'page_name': page_name,
        'page_url': page_url,
        'data': data,
    }
    return render(request, page_url+'/view.html', cont)

# @login_required
# def delete(request, id):
#     checkRolePermission(request, page_url + "-delete")
#     if request.method == 'GET':
#         data = Booking.objects.get(pk=id)
#         data.delete()
#         response = {
#             'status': 'success'
#         }
#     else:
#         response = {
#             'status': 'failed'
#         }
#     return JsonResponse(response)






