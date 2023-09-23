from rest_framework import serializers
from ..models import *
from unlimitedstudio.settings import base_url
from django.db.models import Avg

class GenericsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Generics
        fields = "__all__"


class CategorySerializers(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = "__all__"

    def get_image(self, obj):
        # base_url = 'http://127.0.0.1:8000'
        try:
            x = obj.image.url
        except:
            x = ""
        return x


class SubCategorySerializers(serializers.ModelSerializer):
    
    class Meta:
        model = SubCategory
        fields = "__all__"


class SubCategoryListSerializers(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id','name']

class StudioAvailabilitySerializers(serializers.ModelSerializer):
    class Meta:
        model = StudioAvailability
        fields = "__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)
        x = StudioAvailability.objects.filter(studio=instance.studio_id)
        start_t = int(instance.start_time.split(":")[0])
        s = int(instance.start_time.split(":")[1])
        #print(type(start_t))
        #print(start_t, "BBBBBBBBBBBBBBBBBBBBBBBBB")
        end_t = int(instance.end_time.split(":")[0])
        # e = int(instance.end_time.split(":")[1])
        list1 = []
        for j in range(start_t, end_t):
            c = str(j) + ':' + str(s) + '-' + str(j + 1) + ':' + str(s)
            list1.append(c)
            j += 1
        #print(list1)
        response['slots'] = list1

        return response


class StudioImageSerializers(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    class Meta:
        model = StudioImage
        fields = "__all__"

    def get_image(self, obj):
        # base_url = 'http://127.0.0.1:8000'
        try:
            x = obj.image.url
        except:
            x=""
        return x

class ServiceSerializers(serializers.ModelSerializer):
    class Meta:
        model = Services
        fields = "__all__"

class StudioAddSerializers(serializers.ModelSerializer):
    studio_images = serializers.ListField(required=False)
    category=CategorySerializers(many=True,required=False)



    class Meta:
        model = Studio
        fields = ['studio_images','studio_name','description','remote_service_status',
                  'instagram', 'twitter', 'facebook','category','location','cover_photo' ]

    def create(self, validated_data):
        user = self.context['request'].user
        user = User.objects.get(id=user.id)
        print(user,'===================user')
        user.is_profile_setup = True
        user.save()
        category_ids=validated_data.get('category')
        print('category_ids',category_ids)

        category_ids=self.context['request'].data['category']
        print('categories-------',type(category_ids))
        cat_ids=json.loads(category_ids)
        print('catttttttttttttttttt',cat_ids,type(cat_ids))
        latitude= self.context['request'].data['latitude']
        longitude=self.context['request'].data['longitude']

        # for cat in cat_ids:
        #     print(cat)
        #     .category.add(cat)
        #for cat in
        studio_images = validated_data.pop('studio_images',None)
        cover_photo = validated_data.pop('cover_photo',None)
        studio = Studio.objects.create(**validated_data,created_by=user)

        for cat in cat_ids:
             print('cattttttt',cat)   
             cat_obj=Category.objects.get(id=cat)
             studio.category.add(cat_obj)

        if studio_images:
            for image in studio_images:
                StudioImage.objects.create(studio_img=studio, image=image)
        try:
            image_obj=StudioImage.objects.filter(studio_img=studio).last().image
            user.profile_image=image_obj
            user.first_name=self.context['request'].data['studio_name']
            user.save()
        except Exception as e:
            print('studio image for chat',str(e))
            pass


        studio.latitude=latitude
        studio.longitude=longitude
        studio.cover_photo = cover_photo
        studio.price ='0'
        studio.save()
        return studio

import json
class StudioUpdateSerializers(serializers.ModelSerializer):
    studio_id=serializers.CharField(required=False)
    studio_images = serializers.ListField(required=False)
    generic = serializers.ListField(required=False)
    #generic=GenericsSerializers(many=True)
    availablity = serializers.ListField(required=False)
    start_time = serializers.TimeField(required=False)
    end_time = serializers.TimeField(required=False)
    category=CategorySerializers(many=True,required=False)
    subcategory=serializers.ListField(required=False)
    #services=serializers.ListField(required=False)

    class Meta:
        model = Studio
        fields = '__all__'


# class StudioUpdateSerializers2(serializers.ModelSerializer):
#     studio_images = serializers.ListField(required=False)
#     generic = serializers.ListField(required=False)
#     availablity = serializers.ListField(required=False)
#     start_time = serializers.TimeField(required=True)
#     end_time = serializers.TimeField(required=True)
#     category=CategorySerializers(many=True,required=False)
#     subcategory=serializers.ListField(required=False)
#     services=serializers.ListField(required=False)

#     class Meta:
#         model = Studio
#         fields = '__all__'

#     def update(self, instance, validated_data):
#         print('sssssssssssss',instance.category.all())

#         generic = validated_data.pop('generic', None)

#         print(generic)
#         if generic:
#             generic = json.loads(generic[0])
#             instance.generic.set(generic)
#         subcategory = validated_data.pop('subcategory', None)
#         if subcategory:
#             subcategory = json.loads(subcategory[0])
#             #for i in subcategory:
#             instance.subcategory.set(subcategory)
#         services = validated_data.pop('services', None)
#         #print('servicessss---------->',services)
#         #print(type(services[0]))
#         if services:
#             services = json.loads(services[0])
#             print('services',type(services))
#             for service in services:
#                 print(service['service_name'],service['price'])
#                 service_obj=Services.objects.create(ServiceId=instance,ServiceName=service['service_name'],
#                     ServicePrice=service['price'])
#                 service_obj.save()

#         availablity = validated_data.pop('availablity', None)
#         print('availablity----------------',availablity)
#         if availablity:
#             availablity = json.loads(availablity[0])
#             for av in availablity:
#                 print("131-------------",av)
#                 day=av['day']
#                 start_time=av['start_time']
#                 end_time=av['end_time']
#                 print('day',day,'start_time',start_time,'end_time',end_time)
                
#                 sa, create = StudioAvailability.objects.get_or_create(
#                     studio=instance, days=day)
#                 sa.start_time = start_time
#                 sa.end_time = end_time
#                 sa.save()
#         instance.save()
#         return instance

#         #instance.location = validated_data.get('location', instance.location)
#         #instance.studio_name=validated_data.get('studio_name', instance.studio_name)
#         #instance.remote_service_status = validated_data.get('remote_service_status',
#                                                   #instance.description)
#         #instance.description = validated_data.get('description',
#         #                                          instance.description)
#         #instance.subcategory = validated_data.get('subcategory',
#                                                   #instance.subcategory)
#         # instance.latitude = validated_data.get('latitude',
#         #                                        instance.latitude)
#         # #instance.longitude = validated_data.get('longitude',
#         #                                         instance.longitude)
#         #instance.price = validated_data.get('price', instance.price)
#         #instance.instagram = validated_data.get('instagram',
#         #                                        instance.instagram)
#         #instance.twitter = validated_data.get('twitter', instance.twitter)
#         #instance.facebook = validated_data.get('facebook', instance.facebook)
#         #studio_images = validated_data.pop('studio_images', None)

#         #start_time = validated_data.pop('start_time', None)
#         # end_time = validated_data.pop('end_time', None)

#         # days = validated_data.pop('days', None)
#         # if days:
#         #     days = days[0].replace("[", '').replace("]", '').split(',')
#         #     for day in days:
#         #         sa, create = StudioAvailability.objects.get_or_create(
#         #             studio=instance, days=day)
#         #         sa.start_time = start_time
#         #         sa.end_time = end_time
#         #         sa.save()

#             #instance.subcategory.set(subcategory)

#         # subcategory = validated_data.pop('subcategory', None)
#         # print('subcategory_idssubcategory_idssubcategory_ids',subcategory)
#         # if subcategory:
#         #     subcategory_ids = json.loads(subcategory[0])
#         #     print('subcategory_ids',subcategory_ids)
#         # if studio_images:
#         #     StudioImage.objects.filter(studio_img=instance).delete()
#         #     for x in studio_images:
#         #         img = StudioImage.objects.create(studio_img=instance, image=x)
#         #         img.save()


class EditStudioSerializer(serializers.ModelSerializer):
    generic = GenericsSerializers(many=True, required=False)
    category = CategorySerializers(many=True, required=False)
    # services = ServiceSerializers(many=True, required=False)
    subcategory = SubCategorySerializers(many=True, required=False)
    cover_photo = serializers.SerializerMethodField()


    class Meta:
        model = Studio
        fields = "__all__"

    def get_cover_photo(self, obj):
        x = None
        if obj.cover_photo:
            x =  obj.cover_photo.url
        return x

    def to_representation(self, instance):
        response = super().to_representation(instance)
        service_obj = Services.objects.filter(ServiceId=instance)
        _available_obj = StudioAvailability.objects.filter(studio=instance)
        response['services'] = ServiceSerializers(service_obj, many=True).data
        response['studioavailability'] = StudioAvailabilitySerializers(_available_obj, many=True).data
        return response

from user.serializers import *
class users_serializers(serializers.ModelSerializer):
    user_type = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id','first_name', 'last_name', 'email','mobile' , 'user_type']

    def get_user_type(self, obj):
        try:
            x = obj.role.title
        except:
            x = ""
        return x

class StudioSerializers(serializers.ModelSerializer):
    studio_owner_id=serializers.SerializerMethodField()
    generic = GenericsSerializers(many=True)
    user_type = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    is_profile_setup = serializers.SerializerMethodField()
    is_studio_setup = serializers.SerializerMethodField()
    strip_Connect_id=serializers.SerializerMethodField()
    notification_status =serializers.SerializerMethodField()
    #category=CategorySerializers(required=False)
    #services=serializers.ListField(required=False)


    class Meta:
        model = Studio
        exclude=('first_name','last_name')
        #fields = "__all__"

    def get_user_type(self, obj):
        user_type = obj.created_by.role.title
        return user_type

    def get_strip_Connect_id(self, obj):
        strip_Connect = obj.created_by.strip_Connect_id
        return strip_Connect
    
    def get_notification_status(self, obj):
        notification_status = obj.created_by.notification_status
        return notification_status
    
    def get_email(self, obj):
        email = obj.created_by.email
        return email
    def get_is_profile_setup(self, obj):
        is_profile_setup = obj.created_by.is_profile_setup
        return is_profile_setup

    def get_studio_owner_id(self, obj):
        studio_owner_id = obj.created_by.id
        return studio_owner_id

    def get_is_studio_setup(self, obj):
        is_studio_setup = obj.created_by.is_studio_setup
        return is_studio_setup

    def to_representation(self, instance):
        response = super().to_representation(instance)
        category=instance.category.all()
        subcategory=instance.subcategory.all()
        user = instance.created_by
        user = users_serializers(user).data
        category=CategorySerializers(category,many=True).data
        s = StudioImage.objects.filter(studio_img=instance.id)

        _available_obj=StudioAvailability.objects.filter(studio=instance)
        available_obj=StudioAvailabilitySerializers(_available_obj,many=True)
        service_obj=Services.objects.filter(ServiceId=instance)

        image = StudioImageSerializers(s, many=True)
        response['created_by'] = user
        response['category']=category
        response['subcategory']=SubCategorySerializers(subcategory,many=True).data
        response['studioavailability']=available_obj.data
        response['studio_all_image'] = image.data
        response['services']=ServiceSerializers(service_obj,many=True).data
        return response




from user.models import *

class ProfileSetupSerializers(serializers.ModelSerializer):
    #generic = GenericsSerializers(many=True)
    category=CategorySerializers(many=True,required=False)
    user_type = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    cover_photo = serializers.SerializerMethodField()
    is_profile_setup = serializers.SerializerMethodField()
    is_studio_setup = serializers.SerializerMethodField()


    class Meta:
        model = Studio
        exclude=('first_name','last_name','generic','subcategory',)
        #fields = "__all__"

    def get_user_type(self, obj):
        user_type = obj.created_by.role.title
        return user_type

    def get_email(self, obj):
        email = obj.created_by.email
        return email

    def get_cover_photo(self, obj):
        x = None
        if obj.cover_photo:
            x =  obj.cover_photo.url
        return x

    def get_is_profile_setup(self, obj):
        is_profile_setup = obj.created_by.is_profile_setup
        return is_profile_setup

    def get_is_studio_setup(self, obj):
        is_studio_setup = obj.created_by.is_studio_setup
        return is_studio_setup

    def to_representation(self, instance):
        response = super().to_representation(instance)
        s = StudioImage.objects.filter(studio_img=instance.id)

        _available_obj=StudioAvailability.objects.filter(studio=instance)
        available_obj=StudioAvailabilitySerializers(_available_obj,many=True)
        user_data=User.objects.get(id=instance.created_by.id)
        created_by=users_serializers(user_data).data
        image = StudioImageSerializers(s, many=True)
        response['created_by']=created_by
        response['studio_all_image'] = image.data
        return response


class StudioDistanceSerializers(serializers.ModelSerializer):
    distance = serializers.CharField(required=False)
    category_image = serializers.SerializerMethodField()

    #rating = serializers.SerializerMethodField(required=False)
    class Meta:
        model = Studio
        fields = ['id','studio_name','distance', 'latitude','longitude','category_image', 'price']

    def get_category_image(self, obj):
        category = self.context.get('category')
        try:
            category = Category.objects.get(id=category)
            x =  category.image.url
        except:
            x = ""
        return x

    def to_representation(self, instance):
        response = super().to_representation(instance)
        s = StudioImage.objects.filter(studio_img=instance.id)
        image = StudioImageSerializers(s, many=True)
        try:
            query_obj = Rating.objects.filter(rating_for=instance)
            print('average rating obj',query_obj)
            avarage_rating = query_obj.aggregate(rating=Avg('rating'))
            print('average rating---------288',avarage_rating)
            avarage_rating=int(avarage_rating['rating'])
            print(avarage_rating)
        except Exception as e:
            print('rating in nearby-----290',str(e))
            avarage_rating=0
        response['rating'] = avarage_rating
        response['studio_all_image'] = image.data

        
        return response



class RatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rating
        fields = "__all__"

class StudioRatingSerializers(serializers.ModelSerializer):
    class Meta:
        model = Studio
        fields = ['id', 'studio_name', 'price']
from user.api.serializers import *
class RatingSerializer1(serializers.ModelSerializer):
    #from user.api.serializers import *
    rating_for = StudioRatingSerializers()
    rating_from = User_serializers1()

    class Meta:
        model = Rating
        fields = "__all__"


class FavouriteStudioSerializer(serializers.ModelSerializer):
    studio = StudioRatingSerializers()
    musician_user = users_serializers()
    is_favourite = serializers.BooleanField(required=True)
    studio_image = serializers.SerializerMethodField()

    class Meta:
        model = Favourite
        fields = "__all__"

    def get_studio_image(self, obj):
        try:
            studio_image = StudioImage.objects.filter(studio_img=obj.studio.id).first()
            image =  studio_image.image.url
        except:
            image = ""
        return image


class RaiseDisputeSerializer(serializers.Serializer):
    studio_id = serializers.CharField(required=True)

class RatingSerializer1(serializers.ModelSerializer):
    rating_for = StudioRatingSerializers()
    rating_from = User_serializers1()

    class Meta:
        model = Rating
        fields = "__all__"


