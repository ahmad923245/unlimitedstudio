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


page_name = "Studio"
page_url = "studio"




@login_required
def list(request):
    checkRolePermission(request, page_url + "-list")
    show_add = checkRolePermission(request, page_url + "-add", 0)
    cont = {'page_name': page_name, 'page_url': page_url, 'show_add': show_add}
    return render(request, page_url+'/list.html', cont)


@login_required
def get_list(request):
    checkRolePermission(request, page_url + "-list")
    sortable_columns = ['id', 'studio_name', 'subcategory', 'price']
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
    data_list = Studio.objects.all().filter(Q(studio_name__icontains=keyword)).order_by(order_by)
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
        if checkRolePermission(request, page_url + "-delete", 0) == True:
            actions += create_delete(record.id, page_url+'.delete')
        actions += '</div>'
        category = []
        subcategory = []
        generic = []
        for x in record.category.all():
            category.append(x.name)
        for x in record.subcategory.all():
            subcategory.append(x.name)
        for x in record.generic.all():
            generic.append(x.name)
        try:
            u = {
                'sno': start + i,
                'category': category,
                'sub_category': subcategory,
                'generic': generic,
                'name': record.studio_name,
                'price': record.price,
                'user': record.created_by.first_name,
                'actions': actions
            }
            i = i+1
            datas.append(u)
        except Exception as e:
            print(str(e), '_____________86')
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
    form = StudioForm()
    if request.method == 'POST':
        form = StudioForm(request.POST)
        if form.is_valid():
            data=form.save(commit=False)
            data.status = True
            data.save()
            generic = request.POST.getlist('generic')
            category = request.POST.getlist('category')
            subcategory = request.POST.getlist('subcategory')
            data.generic.add(*generic)
            data.category.add(*category)
            data.subcategory.add(*subcategory)
            data.save()
            # availibility = request.POST.get('availibility')
            # start_time = request.POST.get('start_time')
            # end_time = request.POST.get('end_time')
            # StudioAvailability.objects.create(studio_id=data.id, days=availibility, start_time=start_time, end_time=end_time)
            messages.add_message(request, messages.SUCCESS, ADD_SUCCESS_MESSAGE)
            return redirect(page_url)

    cont = {
        'page_name': page_name,
        'page_url': page_url,
        'forms': form
    }
    return render(request, page_url+'/add.html', cont)


@login_required
def update_status(request):
    checkRolePermission(request, page_url + "-edit")
    if request.method == 'GET':
        id = request.GET.get('id')
        status = request.GET.get('status')
        data = Studio.objects.get(pk=id)
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
    obj = get_object_or_404(Studio, id=id)
    form = StudioForm(request.POST or None, instance=obj)
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
    data = Studio.objects.get(pk=id)
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
        data = Studio.objects.get(pk=id)
        data.delete()
        response = {
            'status': 'success'
        }
    else:
        response = {
            'status': 'failed'
        }
    return JsonResponse(response)


def subcategory_options(request):
    category = request.GET.getlist('country[]')
    x = SubCategory.objects.filter(category_id__in=category).order_by('name')
    return render(request, page_url+'/subcategory_dropdown_list_options.html', {'subcategory': x})


