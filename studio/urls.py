from django.urls import path, re_path,include
# from django.contrib.auth import views as auth_views
# from .forms import EmailValidationOnForgotPassword
from .views import studio,generic,sub_category,raise_dispute,category, rating,studioblock



urlpatterns = [
    #--------------------Studio-----------------------------------------
    path('studio', studio.list, name='studio'),
    path('studio/getlist', studio.get_list, name='studio_list'),
    path('studio/add', studio.add, name='studio.add'),
    path('studio/updatestatus', studio.update_status,
         name='studio.updateStatus'),
    path('studio/edit/<int:id>', studio.edit, name='studio.edit'),
    path('studio/view/<int:id>', studio.view, name='studio.view'),
    path('studio/delete/<int:id>', studio.delete, name='studio.delete'),
    path('studio/subcategoryoptions', studio.subcategory_options, name='subcategory_options'),

#-----------------------------generic----------------------------------------
    path('generic', generic.list, name='generic'),
    path('generic/getlist', generic.get_list, name='generic_list'),
    path('generic/add', generic.add, name='generic.add'),
    path('generic/updatestatus', generic.update_status,
         name='generic.updateStatus'),
    path('generic/edit/<int:id>', generic.edit, name='generic.edit'),
    path('generic/view/<int:id>', generic.view, name='generic.view'),
    path('generic/delete/<int:id>', generic.delete, name='generic.delete'),

#---------------------------------SubCategory---------------------------------
    path('subcategory', sub_category.list, name='sub_category'),
    path('subcategory/getlist', sub_category.get_list, name='sub_category_list'),
    path('subcategory/add', sub_category.add, name='sub_category.add'),
    path('subcategory/updatestatus', sub_category.update_status,
         name='sub_category.updateStatus'),
    path('subcategory/edit/<int:id>', sub_category.edit,
         name='sub_category.edit'),
    path('subcategory/view/<int:id>', sub_category.view,
         name='sub_category.view'),
    path('subcategory/delete/<int:id>', sub_category.delete,
         name='sub_category.delete'),

    path('raisedispute', raise_dispute.list, name='raise_dispute'),
    path('raisedispute/getlist', raise_dispute.get_list, name='raise_dispute_list'),
    path('raisedispute/updatestatus', raise_dispute.update_status,
         name='raise_dispute.updateStatus'),
    path('raisedispute/edit/<int:id>', raise_dispute.edit,
         name='raise_dispute.edit'),
    path('raisedispute/view/<int:id>', raise_dispute.view,
         name='raise_dispute.view'),

    path('category', category.list, name='category'),
    path('category/getlist', category.get_list, name='category_list'),
    path('category/add', category.add, name='category.add'),
    path('category/updatestatus', category.update_status,
         name='category.updateStatus'),
    path('category/edit/<int:id>', category.edit,
         name='category.edit'),
    path('category/view/<int:id>', category.view,
         name='category.view'),
    path('category/delete/<int:id>', category.delete,
         name='category.delete'),

path('rating', rating.list, name='rating'),
    path('rating/getlist', rating.get_list, name='rating_list'),
    path('rating/add', rating.add, name='rating.add'),
    path('rating/updatestatus', rating.update_status,
         name='rating.updateStatus'),
    path('rating/edit/<int:id>', rating.edit,
         name='rating.edit'),
    path('rating/view/<int:id>', rating.view,
         name='rating.view'),
    path('rating/delete/<int:id>', rating.delete,
         name='rating.delete'),
    path('studioblock', studioblock.list, name='studioblock'),
    path('studioblock/getlist', studioblock.get_list, name='studioblock_list'),
    path('studioblock/view/<int:id>', studioblock.view,
         name='studioblock.view'),
    path('studioblock/updatestatus', studioblock.update_status,
         name='studioblock.updateStatus'),
     path('studioblock/delete/<int:id>', studioblock.delete,
         name='studioblock.delete'),

]