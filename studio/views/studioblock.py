from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from unlimitedstudio.utils import *
from unlimitedstudio.apiutils import *
from ..forms import *
from ..models import *
from unlimitedstudio.settings import DATETIME_FORMAT, UPDATE_SUCCESS_MESSAGE, ADD_SUCCESS_MESSAGE
from unlimitedstudio.utils import *


page_name = "Report"
page_url = "studioblock"




@login_required
def list(request):
    checkRolePermission(request, page_url + "-list")
    show_add = checkRolePermission(request, page_url + "-add", 0)
    print('==================24')
    cont = {'page_name': page_name, 'page_url': page_url, 'show_add': show_add}
    print(cont,'================26')
    return render(request, page_url+'/list.html', cont)


@login_required
def get_list(request):
    print('========================31')
    checkRolePermission(request, page_url + "-list")
    sortable_columns = ['id','studio','user','status','created_date']
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
    data_list = StudioBlock.objects.all().order_by(order_by)#.filter(Q(rating_for__studio_name__icontains=keyword) | Q(rating_from__first_name__icontains=keyword) | Q(rating__icontains=keyword))
    print(data_list,'========================dsfsfdsfsdf======41')
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
        # if checkRolePermission(request, page_url + "-edit", 0) == True:
        #     actions += create_edit(record.id, page_url + '.edit')
        if checkRolePermission(request, page_url + "-view", 0) == True:
            actions += create_view(record.id, page_url + '.view')
        if checkRolePermission(request, page_url + "-delete", 0) == True:
            actions += create_delete(record.id, page_url+'.delete')
        actions += '</div>'
        # rating_for_list = []
        # rating_for_list.append(record.rating_for.studio_name)
        # rating_from_list = []
        # rating_from_list.append(record.rating_from.first_name)
        u = {
            'sno': start + i,
            'studio': record.studio.studio_name,
            'reported_by': record.user.first_name,
            'status': create_status(record.status, record.id, {"1": "Active", "0": "Inactive"}, page_url+'.updateStatus'),
            'date': record.created_date.strftime("%m-%d-%Y"),
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
#     form = RatingForm()
#     if request.method == 'POST':
#         print(request.POST,"POST")
#         form = RatingForm(request.POST)
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


@login_required
def update_status(request):
    checkRolePermission(request, page_url + "-edit")
    if request.method == 'GET':
        id = request.GET.get('id')
        status = request.GET.get('status')
        print(status,'==================120')
        data = StudioBlock.objects.get(pk=id)

        if status == '0':
            studio_obj = data.studio
            studio_obj.status=False
            data.status = status
            data.save()
            studio_obj.save()
        else:
            studio_obj = data.studio
            studio_obj.status = True
            data.status = status
            data.save()
            studio_obj.save()
        #print(studio_obj.status,'===============54644======')

        response = {
            'status': 'success'
        }
    else:
        response = {
            'status': 'failed'
        }
    return JsonResponse(response)


# @login_required
# def edit(request, id):
#     checkRolePermission(request, page_url + "-edit")
#     obj = get_object_or_404(Rating, id=id)
#     form = RatingForm(instance=obj)
#     if request.method == 'POST':
#         form = RatingForm(request.POST, instance=obj)
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


@login_required
def view(request, id):
    checkRolePermission(request, page_url + "-view")
    data = StudioBlock.objects.get(pk=id)
    cont = {
        'page_name': page_name,
        'page_url': page_url,
        'data': data
    }
    return render(request, page_url+'/view.html', cont)


@login_required
def delete(request, id):
    checkRolePermission(request, page_url + "-delete")
    if request.method == 'GET':
        data = StudioBlock.objects.get(pk=id)
        data.delete()
        response = {
            'status': 'success'
        }
    else:
        response = {
            'status': 'failed'
        }


    return JsonResponse(response)











