from django.urls import path, re_path,include
# from django.contrib.auth import views as auth_views
# from .forms import EmailValidationOnForgotPassword
from .views import cms ,faq, static_pages, admin_charges



urlpatterns = [
    #--------------------cms-----------------------------------------
    path('cms', cms.list, name='cms'),
    path('cms/getlist', cms.get_list, name='cms_list'),
    path('cms/add', cms.add, name='cms.add'),
    path('cms/updatestatus', cms.update_status, name='cms.updateStatus'),
    path('cms/edit/<int:id>', cms.edit, name='cms.edit'),
    path('cms/view/<int:id>', cms.view, name='cms.view'),
    path('cms/delete/<int:id>', cms.delete, name='cms.delete'),

#--------------------------faq-------------------------------------

    path('faq/', faq.list, name='faq'),
    path('faq/getlist', faq.get_list, name='faq_list'),
    path('faq/add', faq.add, name='faq.add'),
    path('faq/updatestatus', faq.update_status, name='faq.updateStatus'),
    path('faq/edit/<int:id>', faq.edit, name='faq.edit'),
    path('faq/view/<int:id>', faq.view, name='faq.view'),
    path('faq/delete/<int:id>', faq.delete, name='faq.delete'),

    path('staticpages/', static_pages.list, name='static_pages'),
    path('staticpages/getlist', static_pages.get_list, name='static_pages_list'),
    path('staticpages/add', static_pages.add, name='static_pages.add'),
    path('staticpages/edit/<int:id>', static_pages.edit, name='static_pages.edit'),
    path('ckeditor/', include('ckeditor_uploader.urls')),


    path('admincharges/', admin_charges.list, name='admin_charges'),
    path('admincharges/getlist', admin_charges.get_list, name='admin_charges_list'),
    path('admincharges/add', admin_charges.add, name='admin_charges.add'),
    path('admincharges/edit/<int:id>', admin_charges.edit, name='admin_charges.edit'),
    path('admincharges/view/<int:id>', admin_charges.view, name='admin_charges.view'),

]