from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from setting.forms import *
from setting.models import *
from unlimitedstudio.settings import DATETIME_FORMAT, UPDATE_SUCCESS_MESSAGE, ADD_SUCCESS_MESSAGE
from unlimitedstudio.utils import *
page_name = "FAQ"
page_url = "faq"


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

    data_list = Faq.objects.filter(Q(title__icontains=keyword) | Q(description__icontains=keyword)).order_by(order_by)
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
            actions += create_delete(record.id, page_url + '.delete')
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
    form = FaqForm()
    if request.method == 'POST':
        form = FaqForm(request.POST)
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
def update_status(request):
    checkRolePermission(request, page_url + "-edit")
    if request.method == 'GET':
        id = request.GET.get('id')
        status = request.GET.get('status')
        data = Faq.objects.get(pk=id)
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
    obj = get_object_or_404(Faq, id=id)
    form = FaqForm(request.POST or None, instance=obj)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            # data = Faq.objects.get(pk=id)
            # data.en_title = request.POST.get('title')
            # data.it_title = request.POST.get('title')
            # data.en_description = request.POST.get('description')
            # data.it_description = request.POST.get('description')
            # data.save()
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
    data = Faq.objects.get(pk=id)
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
        data = Faq.objects.get(pk=id)
        data.delete()
        response = {
            'status': 'success'
        }
    else:
        response = {
            'status': 'failed'
        }
    return JsonResponse(response)

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.forms import widgets
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, View
from django.views.generic.edit import CreateView, DeleteView


# class StudentListView(LoginRequiredMixin, ListView):
#     model = Faq
#     template_name = "faq/list.html"
#
#
#
# class FaqDetailView(LoginRequiredMixin, DetailView):
#     model = Faq
#     template_name = "faq/view.html"
#
#     def get_context_data(self, **kwargs):
#         context = super(FaqDetailView, self).get_context_data(**kwargs)
#         context['page_name']=page_name
#         context['page_url']= page_url
#         return context


# class FaqCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
#     model = Faq
#     fields = "__all__"
#     success_message = "New student successfully added."
#
#     def get_form(self):
#         """add date picker in forms"""
#         form = super(StudentCreateView, self).get_form()
#         form.fields["date_of_birth"].widget = widgets.DateInput(attrs={"type": "date"})
#         form.fields["address"].widget = widgets.Textarea(attrs={"rows": 2})
#         form.fields["others"].widget = widgets.Textarea(attrs={"rows": 2})
#         return form