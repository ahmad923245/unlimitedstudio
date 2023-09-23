import json
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import *
from booking.models import *
from studio.models import *
from unlimitedstudio.apiutils import *
from django.db.models import Avg
from rest_framework.pagination import PageNumberPagination
from firebase_admin import *
from firebase_admin.messaging import Message
from firebase_admin.messaging import Notification as fNotification

class GenericViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'head']
    permission_classes = [IsAuthenticated]
    queryset = Generics.objects.all()
    serializer_class = GenericsSerializers

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            # return self.get_paginated_response(serializer.data)
            d = self.get_paginated_response(serializer.data).data
            m = "GenericViewSet List"
            s = True
            return response_handler(message=m, status=s, data=d)
        serializer = self.get_serializer(queryset, many=True)
        d = serializer.data
        m = "GenericViewSet List"
        s = True
        return response_handler(message=m, status=s, data=d)


class AddStudioViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Studio.objects.all()
    serializer_class = StudioSerializers
    def create(self, request):
        # user=request.user
        serializer = StudioAddSerializers(data=request.data,context={'request': request})
        if serializer.is_valid():
            obj=serializer.save()
            # user = User.objects.get(id=user.id)
            # print(user,'===================user')
            # user.is_profile_setup = True
            # user.save()

            # k.created_by=user
            # k.save()

            d=ProfileSetupSerializers(obj).data
            #d['email']=User_serializers(user).data
            m = "Profile Setup Successfully Done"
            s = True
            return response_handler(message=m, status=s, data=d)
        else:
            m = serialiser_errors(serializer)  # "Error"
            s = False
            d = {}
            return response_handler(message=m, status=s, data=d)

    # def put(self, request, pk, format=None):
    #     snippet = self.get_object(pk)
    #     serializer = StudioAddSerializers(snippet, data=request.data,
    #                                       partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class UpdateStudioViewSet(viewsets.ModelViewSet):
#     # http_method_names = ['petch', 'head']
#     permission_classes = [IsAuthenticated]
#     queryset = Studio.objects.all()
#     serializer_class = StudioUpdateSerializers

#     def update(self, request, *args, **kwargs):
#         snippet = self.get_object()
#         serializer = StudioUpdateSerializers(snippet, data=request.data,
#                                              partial=True)
#         if serializer.is_valid():
#             obj=serializer.save()
#             print('onjjjjjjjjjjjjjjjjjjjj-------83')
#             m ="Update successfully"  # "Error"
#             s = True
#             d=StudioSerializers(obj).data
#             return response_handler(message=m, status=s, data=d)
#         else:
#             m = serialiser_errors(serializer)  # "Error"
#             s = False
#             d = {}
#             return response_handler(message=m, status=s, data=d)

class UpdateStudioViewSet(viewsets.ViewSet):
    http_method_names = ['post', 'head']
    permission_classes = [IsAuthenticated]
 
    serializer_class = StudioUpdateSerializers
    def create(self, request, *args, **kwargs):
        #snippet = self.get_object()
        serializer = StudioUpdateSerializers(data=request.data)
        user = request.user
        if serializer.is_valid():
            remote_service_status = request.data['remote_service_status']
            print('=============remote_service_status========',remote_service_status)
           
            try:
                studio_id=serializer.data['studio_id']
                studio_obj = Studio.objects.get(id=studio_id)

            except:
                d={}
                s = False
                m="id does not exit"
                return response_handler(message=m, status=s, data=d)
            print(studio_id, '==================studio id')

            try:
                price=request.data.get('price')
                studio_obj.price = price
                print(studio_obj.price, "_____________________________1111111111111")
                category = studio_obj.category.all()
                for i in category:

                    if i.id == 1:
                        print(i.name, "_________________________2222222222222222")
                        service_obj = Services.objects.create(ServiceId_id=studio_id,
                                                              ServiceName='Studio/Hourly Services',
                                                              ServicePrice=price)
            except:
                price=''
                studio_obj.price = price

            # try:
            #     is_profile_setup=request.data.get('is_profile_setup')
            # except:
            #     is_profile_setup=False


            # studio_obj.is_profile_setup=is_profile_setup
            studio_obj.save()
            try:
                generic=request.data.get('generic')
                print('----------------->114',generic,type(generic))
                generic=generic.split(',')
                print('generic-----116',generic,type(generic))
                # if str == type(generic):
                #     generic=json.loads(generic)
                # generic=generic  
            except:
                generic=''
            try:
                subcategory=request.data.get('subcategory')
                print('----------------->124',subcategory,type(subcategory))
                subcategory=subcategory.split(',')
                print('subcategory-----126',subcategory,type(subcategory))
                # if str == type(subcategory):
                #     subcategory=json.loads(subcategory)
                # subcategory=subcategory 
            except: 
                subcategory=''
            try:
                services=request.data.get('services')
                temp_service = ''
                if str == type(services):
                    services = json.loads(services)


                    for service in services:
                        try:
                            service_remote_status=service['service_remote_status']
                        except:
                            service_remote_status=False

                        s1=service['service_name']
                        temp_service = temp_service + s1
                        print(temp_service, "______________________174")
                        service_obj=Services.objects.create(ServiceId_id=studio_obj.id,
                            ServiceName=service['service_name'],
                            ServicePrice=service['price'],
                            service_remote_status=service_remote_status)
                else:
                    # studio_obj.temp_services = services['service_name']

                    for service in services:
                        try:
                            service_remote_status=service['service_remote_status']
                        except:
                            service_remote_status=False

                        s1 = service['service_name']
                        temp_service = temp_service + s1
                        service_obj=Services.objects.create(ServiceId_id=studio_obj.id,
                            ServiceName=service['service_name'],
                            ServicePrice=service['price'],
                            service_remote_status=service_remote_status)
                print(temp_service, "______________________187")
                studio_obj.temp_services=temp_service
                studio_obj.remote_service_status=remote_service_status
                studio_obj.save()
            except:
                pass
            try:
                availablity=request.data.get('availablity')
                print(type(availablity),'=========================143444444444444444444444444444444')
                if str == type(availablity):
                    print('================145')
                    availablity = json.loads(availablity)
                    print(availablity,'=====================188888888888888888888888')
                    for av in availablity:
                        print("147-------------",av)
                        day=av['day']
                        # start_time=av['start_time']
                        # end_time=av['end_time']
                        s_seconds = av['start_time'][-2:]
                        start_time = av['start_time'].replace(s_seconds, '00')
                        e_seconds = av['end_time'][-2:]
                        end_time = av['end_time'].replace(e_seconds, '00')
                        print('day',day,'start_time',start_time,'end_time',end_time,'============151')

                        sa = StudioAvailability.objects.create(studio_id=studio_obj.id, days=day)
                        sa.start_time = start_time
                        sa.end_time = end_time
                        sa.save()
                else:
                    for av in availablity:
                        print("160-------------",av)
                        day=av['day']
                        # start_time=av['start_time']
                        # end_time=av['end_time']
                        # if av['end_time']=="00:00:00":
                        #     av['end_time']=24:00:00
                        s_seconds = av['start_time'][-2:]
                        start_time = av['start_time'].replace(s_seconds, '00')
                        e_seconds = av['end_time'][-2:]
                        end_time = av['end_time'].replace(e_seconds, '00')
                        print('day',day,'start_time',start_time,'end_time',end_time)
                        
                        sa, create = StudioAvailability.objects.get_or_create(
                            studio_id=studio_obj.id, days=day)
                        sa.start_time = start_time
                        sa.end_time = end_time
                        sa.save()
            except:
                pass
            studio_obj.generic.set(generic)
            studio_obj.subcategory.set(subcategory)
            studio_obj.save()
            #
            # d1 = StudioSerializers(studio_obj)
            # print("________________data", d1.data['services'][1]['ServiceName'])
            # data1 = StudioSerializers(studio_obj)
            # d2 = data1.data['services']
            # for d in d2:
            #     print(d, "______________________DDDDDDDDDDDDDDDDDDDDD")
            #     print(d['ServiceName'], "________________hi")
            #
            #     if d['ServiceName'] == 'Book Studio':
            #         print("_______________________sssssssuc")
            #         d2.remove(d)
            #         print(d2, "______________________data")
            #
            # d1.data['services'] = d2
            try:
                user = User.objects.get(id=user.id)
                user.is_studio_setup = True
                user.save()
            except:
                pass
            m ="Update successfully"  # "Error"
            s = True
            d=StudioSerializers(studio_obj).data
            return response_handler(message=m, status=s, data=d)
        else:
            m = serialiser_errors(serializer)  # "Error"
            s = False
            d = {}
            return response_handler(message=m, status=s, data=d)


class EditStudioViewset(viewsets.ModelViewSet):
    http_method_names = ['put', 'head']
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        studio = Studio.objects.get(id=kwargs['pk'])
        try:
            comment = request.data['comment']
        except:
            comment="NA"
        try:
            studio_status = request.data['studio_status']
            try:
                x=StudioBlock.objects.get(user=request.user, studio=studio)
                x.studio_status = studio_status
                x.save()
            except:
                StudioBlock.objects.create(user=request.user, studio=studio, studio_status=studio_status, comment=comment)

        except:
            studio_status = 'Approved'

        try:
            request.user.first_name = request.data['studio_name']
            request.user.save()
        except:
            pass
        try:
            try:
                lat = request.data.get('latitude')
                long = request.data.get('longitude')
                print(lat, "_________________________111")
            except:
                lat=studio.latitude
                long=studio.longitude
                print(lat, "_________________________222")
            if lat==None or long==None or lat=='' or long=='':
                pass
            else:

                studio.latitude = lat
                studio.longitude = long
                studio.save()
                print(lat, "_______________________________333333")

        except:
            pass

        try:
            studio_image = request.data['studio_image']
            print(request.data['studio_name'],'==============228')
            print(studio_image,'=========228 image')
            studioimage = StudioImage.objects.get(studio_img=studio)
            studioimage.image = studio_image
            studioimage.save()
            request.user.profile_image=studio_image
            print(request.user.profile_image,'==========236====request.user.profile_image')
        except:
            pass
 
        try:
            studio_images =request.data.getlist('studio_images')
            if studio_images:
                StudioImage.objects.filter(studio_img=studio).delete()
                for image in studio_images:
                    print('image------------->125',image)
                    StudioImage.objects.create(studio_img=studio, image=image)
        except Exception as e:
            print('eeeeeeeeeeeeeee',str(e))


        try:
            generic = request.data.get('generic')
            print(generic,'========233====',type(generic))
            generic=generic.replace('[','').replace(']','')
            print('generic after replace',generic)

            generic = generic.split(',')
            print('generic===============',generic)
            studio.generic.set(generic)
        except Exception as e:
            print(str(e))
            pass
        try:

            category = request.data.get('category')
            print('category===============',category)
            category=category.replace('[','').replace(']','')
            category = category.split(',')
            print('category===============',category)
            studio.category.set(category)
        except:
            pass
        try:
            subcategory = request.data.get('subcategory')
            print(subcategory,'========242====',type(subcategory))
            subcategory=subcategory.replace('[','').replace(']','')
            subcategory = subcategory.split(',')
            print('subcategory===============',subcategory)
            studio.subcategory.set(subcategory)
        except:
            pass
        try:
            services = request.data.get('services')
            if services != None: #or services != '':
                print('services===========264',services)
                print('services type===========264',type(services))

                if str == type(services):

                    services = json.loads(services)
                    print("services===========270",services)
                    Services.objects.filter(ServiceId_id=studio.id).delete()
                    for service in services:
                        print('ser---------1',service)
                        try:
                            service_remote_status=service['service_remote_status']
                        except:
                            service_remote_status=False

                        service_obj = Services.objects.create(ServiceId_id=studio.id,
                                                            ServiceName=service['service_name'],
                                                            ServicePrice=service['price'],
                                                            service_remote_status=service_remote_status)
                else:
                    print("services===========278",services)
                    Services.objects.filter(ServiceId_id=studio.id).delete()
                    for service in services:
                        try:
                            service_remote_status=service['service_remote_status']
                        except:
                            service_remote_status=False
                        print('ser---------1',service)
                        service_obj = Services.objects.create(ServiceId_id=studio.id,
                                                            ServiceName=service['service_name'],
                                                            ServicePrice=service['price'],
                                                            service_remote_status=service_remote_status)
        except Exception as e:
            print('ssssssssssss',str(e))
            pass
        try:
           
            availablity = request.data.get('availablity')
            if availablity != None:# or availablity != '':
                StudioAvailability.objects.filter(studio=studio).delete()
                print('availablity================',availablity)
                if str == type(availablity):
                    availablity = json.loads(availablity)
                    for av in availablity:
                        day = av['day']
                        # start_time = av['start_time']
                        # end_time = av['end_time']
                        s_seconds = av['start_time'][-2:]
                        start_time = av['start_time'].replace(s_seconds, '00')
                        e_seconds = av['end_time'][-2:]
                        end_time = av['end_time'].replace(e_seconds, '00')
                        sa = StudioAvailability.objects.create(studio_id=studio.id, days=day)
                        sa.start_time = start_time
                        sa.end_time = end_time
                        sa.save()
                else:
                    for av in availablity:
                        day = av['day']
                        # start_time = av['start_time']
                        # end_time = av['end_time']
                        s_seconds = av['start_time'][-2:]
                        start_time = av['start_time'].replace(s_seconds, '00')
                        e_seconds = av['end_time'][-2:]
                        end_time = av['end_time'].replace(e_seconds, '00')

                        sa, create = StudioAvailability.objects.get_or_create(
                            studio_id=studio.id, days=day)
                        sa.start_time = start_time
                        sa.end_time = end_time
                        sa.save()
        except:
            pass

        serializer = EditStudioSerializer(instance=studio, data=request.data, partial=True)
        if serializer.is_valid():
            print("______________________8888")
            self.perform_update(serializer)

            d1 = StudioSerializers(studio)
            # print("________________data", d1.data['services'][1]['ServiceName'] )
            # data1 = StudioSerializers(studio)
            # d2 = data1.data['services']
            # for d in d2:
            #     print(d,"______________________DDDDDDDDDDDDDDDDDDDDD")
            #     print(d['ServiceName'], "________________hi")
            #
            #     if d['ServiceName'] == 'Book Studio':
            #         print("_______________________sssssssuc")
            #         d2.remove(d)
            #         print(d2, "______________________data")
            #
            # d1.data['services']=d2
            #
            # #print(d1, "___________________________________________________________d1")
            # print("_____________services________________", data1)

            # for key, val in d1.data['services']:
            #     for i in val:
            #         print(i, "_____________________i")

            m = "Update successfully"
            s = True
            return response_handler(message=m, status=s, data=d1.data)
        else:
            m = "Update successfully"
            s = True
            return response_handler(message=m, status=s, data=serializer.errors)



        
class SubCategoryViewSet(viewsets.ModelViewSet):
    http_method_names = ['get','post','head']
    permission_classes = [IsAuthenticated]
    #queryset = SubCategory.objects.all()
    #serializer_class = SubCategorySerializers

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            # return self.get_paginated_response(serializer.data)
            d = self.get_paginated_response(serializer.data).data
            m = " SubCategory List Fetched"
            s = True
            return response_handler(message=m, status=s, data=d)
        serializer = self.get_serializer(queryset, many=True)
        d = serializer.data
        m = "SubCategory List"
        s = True
        return response_handler(message=m, status=s, data=d)

    def create(self, request):
        try:
            category_ids=request.data['category']
            print(type(category_ids),'===============361')
            if  type(category_ids) == str:
                print('============362')
                category_ids=json.loads(category_ids)
            # else:
            #     pass
            #ids=json.load=(category_ids)
            # print('categor print(type(category_ids),'================361')
            #category_y------------------------------------',category_ids,type(category_ids))
                
            print(type(category_ids),'====================364')
            #print(type(cat_ids),cat_ids)
            sub_cat_list=[]
            sub_cat=SubCategory.objects.filter(category__in=category_ids).values('id','name')
            print(sub_cat,'=================368')
            sub_cat_data=SubCategoryListSerializers(sub_cat,many=True)
            print('sub_cat_data',sub_cat_data)
            d = sub_cat_data.data
            m = "SubCategory List Fetched"
            s = True
            return response_handler(message=m, status=s, data=d) 
        except Exception as e:
            d = {}
            m = str(e)
            s = False
            return response_handler(message=m, status=s, data=d) 

class CategoryViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'head']
    permission_classes = [IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategorySerializers

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            # return self.get_paginated_response(serializer.data)
            d = self.get_paginated_response(serializer.data).data
            m = "Category List"
            s = True
            return response_handler(message=m, status=s, data=d)
        serializer = self.get_serializer(queryset, many=True)
        d = serializer.data
        m = "Category List"
        s = True
        return response_handler(message=m, status=s, data=d)

class SpecificStudioViewSet(viewsets.ModelViewSet):
    queryset = Studio.objects.all()
    serializer_class = StudioSerializers
    permission_classes = [AllowAny]
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        print(instance,'=========403',instance.id,'=========instance')
        print(request.user.id,'=============request.user.id')
        serializer = StudioSerializers(instance).data
        try:
            fav_status=Favourite.objects.filter(studio__id=instance.id,musician_user__id=request.user.id).last().is_favourite  
            print("269--------------------fav_status",fav_status)
        except Exception as e:
            print(str(e))
            print('==============410')
            fav_status=False
        try:
            reserved_date = Booking.objects.filter(studio=instance, accepted=True).values_list('appointment_date', flat=True).distinct()

        except Exception as e:
            reserved_date = str(e)
        try:
            query_obj = Rating.objects.filter(rating_for=instance)
            avarage_rating = query_obj.aggregate(rating=Avg('rating'))
            avarage_rating=int(avarage_rating['rating'])
            total_reviews=query_obj.count()
            rating = RatingSerializer1(query_obj, many=True).data
        except:
            avarage_rating=0
            total_reviews=0
            rating={}
        for i in instance.category.all():
            if i.name == "Studios":
                reserved_date = []
            else:
                reserved_date = reserved_date
        serializer['is_favourite'] = fav_status
        serializer['reserved_date'] = reserved_date
        serializer['total_reviews'] = total_reviews
        serializer['avarage_rating'] = avarage_rating
        serializer['rating'] = rating
        return response_handler(message='Success', status=True, data=serializer)

class GenreWiseStudioViewSet(viewsets.ModelViewSet):
    queryset = Studio.objects.all()
    serializer_class = StudioSerializers
    permission_classes = [AllowAny]
    def list(self, request):
        try:
            try:
                keyword = self.request.GET.get('keyword')
            except:
                keyword = ""
            try:
                distance = float(self.request.GET.get('distance'))
            except:
                distance = 50
            try:
                latitude = float(self.request.GET.get('latitude'))
            except:
                latitude = 33.753746
            try:
                longitude = float(self.request.GET.get('longitude'))
            except:
                longitude = -84.386330

            try:
                genre = int(self.request.GET.get('genre_id'))
                print('genre id-----------300',genre)
            except:
                genre = 1

            radlat = Radians(latitude) # given latitude
            radlong = Radians(longitude) # given longitude
            radflat = Radians(F('latitude'))
            radflong = Radians(F('longitude'))


            Expression = 3958.756 * Acos(Cos(radlat) * Cos(radflat) *Cos(radflong - radlong) + Sin(radlat) * Sin(radflat))
            studio = Studio.objects.filter(generic__id=genre).annotate(distance=Expression).order_by('distance')#.filter(distance__lte=distance)
            if keyword != None and keyword != '' and len(keyword) != 0:
                studio = studio.filter(studio_name__icontains=keyword)
            studio_data = StudioDistanceSerializers(studio, many=True)
            d = studio_data.data
            m = "Generic Wise Studio list Fetched"
            s = True
            return response_handler(message=m, status=s, data=d)
        except Exception as e:
            print('------------------331',str(e))
            d = {}
            m = str(e)
            s = False
            return response_handler(message=m, status=s, data=d)



from django.db.models import Func, F
class Sin(Func):
    function = 'SIN'
class Cos(Func):
    function = 'COS'
class Acos(Func):
    function = 'ACOS'
class Radians(Func):
    function = 'RADIANS'


import requests
class StudioMapViewset(viewsets.ModelViewSet):
    def list(self, request):
        print('--------------------298')


        # x_ip = request.META.get('HTTP_X_FORWARDED_FOR')
        # if x_ip is not None:
        #     ip = x_ip.split(",")[0]
        # else:
        #     ip = request.META.get('REMOTE_ADDR')
        # print(ip, "__________________________________________________528")
        #
        #
        # res = requests.get("http://ip-api.com/json/124.59.75.221")
        # print(res, "_________________________537")
        # location = res.text
        # d = json.loads(location)
        # print(d, "_________________________________________________540")
        # lat = d['lat']
        # lon = d['lon']
        # print(lat, "______________________543")
        # print(lon, "__________________________________544")


        try:
            try:
                distance = self.request.GET.get('distance')
                print(distance, "___________________550")
                if distance == None or distance == '':
                    distance = 100
                    print(distance, "________________d________")

            except:
                distance = 100
                print(distance, "____________________________________________________________________________distance")
            try:
                latitude = float(self.request.GET.get('latitude'))
                print(latitude, "____________523")
            except Exception as e:
                print(str(e), "________________525")
                latitude = 33.753746
            try:
                longitude = float(self.request.GET.get('longitude'))
            except:
                longitude = -84.386330

            try:
                category = self.request.GET.get('category')
                print('_____________________________530',category)
                category = category.split(',')
            except Exception as e :
                print(str(e), "KKKKKKKKKKKKK")
                category = ""

            try:
                subcategory = self.request.GET.get('subcategory')
                if subcategory == "":
                    subcategory = None
                print(subcategory,"===========================358")
                subcategory=subcategory.split(',')
            except Exception as e:
                print(str(e), "______________________542")

                subcategory = ''

            try:
                generic_ids = self.request.GET.get('generic_ids')
                if generic_ids == "":
                    generic_ids = None
                generic_ids=generic_ids.split(',')
                print('generic_ids===============',generic_ids)
            except:
                generic_ids = ''

            try:
                remote_status = self.request.GET.get('remote_status')
                print('remote_status---------------',remote_status)
                print('remote_status---------------',type(remote_status))
            except:
                remote_status = ''

            try:
                budget = self.request.GET.get('budget')
            except:
                budget = ''

            try:
                keyword = self.request.GET.get('keyword')
            except:
                keyword = ""


            radlat = Radians(latitude) # given latitude
            radlong = Radians(longitude) # given longitude
            radflat = Radians(F('latitude'))
            radflong = Radians(F('longitude'))


            Expression = 3958.756 * Acos(Cos(radlat) * Cos(radflat) *Cos(radflong - radlong) + Sin(radlat) * Sin(radflat))
            print('Expression',Expression)
            studio = Studio.objects.all().annotate(distance=Expression).order_by('distance')

            # studio = studio.filter(studio_status='Approved')
            #studio1 = StudioBlock.objects.filter(user=request.user).filter(Q(studio_status='Blocked') | Q(studio_status='Reported')).values_list('studio')
            studio1=StudioBlock.objects.filter(user=request.user).values_list('studio',flat=True)
            print(studio1, "_________________________________7333")
            studio = studio.exclude(id__in=studio1)
            studio=studio.filter(status=True)


            # try:
            #     for s in studio:
            #         print("392222222222222---->",int(s.studio_distance))
            #         fix_distance = round(s.studio_distance,1)
            #         print(fix_distance,'==========================fix_distace')
            #         s.studio_distance = fix_distance
            #         s.save()
            # except:
            #     pass
            if category != None and category != '':
                studio = studio.filter(category__id__in=category).distinct()
                print("________________593", len(studio))

            if subcategory != None and subcategory != '' and len(subcategory) != 0:
                print(subcategory, '=============389')
                studio = studio.filter(subcategory__id__in=subcategory).distinct()
                print(subcategory, '=============389')


            if remote_status != None and remote_status != '':
                print(remote_status,"_______________605")
                print(len(studio), "__________606")
                studio = studio.filter(remote_service_status=remote_status)
                print(len(studio), '=============389')


            try:
                if budget != None and budget != '':
                    studio_budget = Services.objects.filter(ServicePrice__lte=int(float(budget))).values_list('ServiceId')
                    studio = studio.filter(id__in=studio_budget)
                    print(studio_budget, "____________________________________648")

                    print(len(studio), "____________________________________650")
            except Exception as e:
                print(str(e), "_____________except")

            if generic_ids != None and generic_ids != '' and len(generic_ids)!=0:
                studio = studio.filter(generic__id__in=generic_ids)
                #print(studio, '=============389')

            if keyword != None and keyword != '' and len(keyword) != 0:

                studio = studio.filter(Q(studio_name__icontains=keyword) | Q(category__name__icontains=keyword) | Q(subcategory__name__icontains=keyword) | Q(temp_services__icontains=keyword)).distinct()
                print(studio, "__________________studio__________")
            # try:
            #     if distance != None and distance != '' and distance != 0:
            #         print(distance, "___________________615")
            #         x=studio.values_list('id','distance')
            #         all=[]
            #         for i in x:
            #             print(i,"______________625")
            #             print(i[1], "___________________622")
            #             if type(i[1])!="NoneType":
            #                 if i[1] <= int(distance):
            #                     si=i[0]
            #                     all.append(si)
            #         print(all,"______________________all")
            #         studio=studio.filter(id__in=all)
            # except Exception as e:
            #     print('expessssssss',str(e))
                # studio = studio.filter(studio_distance__lte=distance)

            per_page_data = 10
            try:
                total = studio.count()
                total_page = total / per_page_data
                import math
                total_pages = math.ceil(total_page)
                print(total_pages,'====================total pages')
            except:
                total_pages = 0
            paginator = PageNumberPagination()
            paginator.page_size = 10
            studio = paginator.paginate_queryset(studio, request)
            per_page_data=10
            try:
                total=len(studio)
                print('total studio',total)
                total_page=total/per_page_data
                print('total_page before ------------->',total_page)
                import math 
                total_pages=math.ceil(total_page)
                print('total_pages------------->',total_pages)
            except Exception as e:
                print('pagination----->',str(e))
                total_pages=0

            studio_data = StudioDistanceSerializers(studio,context={'category': category}, many=True)
            paginated = paginator.get_paginated_response(studio_data.data)
            print(type(paginated))
            d = paginated.data
            d["total_pages"] = total_pages
            d["per_page_data"] = per_page_data
            m = "Studio Map list Fetched"
            s = True
            return response_handler(message=m, status=s, data=d)
        except Exception as e:
            print('------------------331',str(e))
            d = {}
            m = str(e)
            s = False
            return response_handler(message=m, status=s, data=d)



class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        print('---------381', serializer)
        serializer.is_valid(raise_exception=True)
        y = serializer.save()
        print('yyyyyyyyyyyyyyyyyyyyyyyyyyyyy', y.id)

        s = RatingSerializer1(y)
        try:
            studio_owner=s.data['rating_for']['id']
            studio_owner_id=Studio.objects.get(id=studio_owner).created_by
            fcmdevice = FCMDevice.objects.get(user=studio_owner_id)
            notification = messaging.Notification(
            title="Musician has given you ratings",
            body="Rated by musician USER",)
            k = messaging.Message(
                notification=notification,
                data={
                    'id':str(y.id),
                    'title': "Rated by musician",
                    'message': "Rated by musician",
                    'type': 'Rated_By_Musician',
                },
                token=str(fcmdevice.registration_id))
            x = fcmdevice.send_message(k)
            Notifications.objects.create(user=studio_owner_id,
                                         title='Musician has given you ratings',
                                         message="Rated by musician USER", type="Rated_By_Musician",
                                         booking_id=str(y.id))

        except Exception as e:
            print(str(e),"------------------------>")
            print("Booking cancelled by Musician")
        headers = self.get_success_headers(s.data)
        return response_handler(message='Success', status=True, data=s.data)

    def list(self, request, ):
        user = self.request.user
        print('rating------------>',user)
        query_obj = Rating.objects.filter(rating_for=user.id)
        try:
            avarage_rating = query_obj.aggregate(rating=Avg('rating'))
            avarage_rating=int(avarage_rating['rating'])
        except:
            avarage_rating=0
        serializer = RatingSerializer1(query_obj, many=True)
        rating_dict = {'avarage_rating':avarage_rating, 'ratings': serializer.data}
        return response_handler(message='Success', status=True, data=rating_dict)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = RatingSerializer1(instance)
        return response_handler(message='Success', status=True, data=serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance:
            self.perform_destroy(instance)
            return response_handler(message='Rating Details deleted', status=True, data={})
        else:
            return response_handler(message='Rating not found', status=False, data={})

    def update(self, request, *args, **kwargs):
        data1 = super(RatingViewSet, self).update(request, args, *kwargs)
        return response_handler(message='Rating Details updateD', status=True, data=data1.data)


class SpecificStudioRatingViewSet(viewsets.ModelViewSet):
    def create(self, request):
        try:
            studio_id =request.data['studio_id']
            print('studio_id------------------------------------',studio_id,type(studio_id))
        except:
            return response_handler(message='studio_id not exist', status=False, data=rating_dict)
        query_obj = Rating.objects.filter(rating_for=studio_id)
        try:
            avarage_rating = query_obj.aggregate(rating=Avg('rating'))
            avarage_rating=int(avarage_rating['rating'])
            total_reviews=query_obj.count()
        except:
            avarage_rating=0
            total_reviews=0
        serializer = RatingSerializer1(query_obj, many=True)
        rating_dict = {'avarage_rating':avarage_rating,'total_reviews':total_reviews,'ratings': serializer.data}
        return response_handler(message='Success', status=True, data=rating_dict)




class FavouriteStudioViewsets(viewsets.ModelViewSet):
    queryset = Favourite.objects.all()
    serializer_class = FavouriteStudioSerializer
    permission_classes = [IsAuthenticated]
    def list(self, request, ):
        user = self.request.user
        fav_obj = Favourite.objects.filter(is_favourite=True,musician_user =user.id)
        data = FavouriteStudioSerializer(fav_obj, many=True)
        return response_handler(message='Success', status=True, data=data.data)

    def create(self, request):
        is_favourite = request.data['is_favourite']
        studio_id = request.data['studio_id']
        user_id = request.data['user_id']
        print('studio_id : ', studio_id)
        print('user_id : ', user_id)
        print('is_favourite : ', is_favourite)
        try:
            studio_id=Studio.objects.get(id=studio_id)
            user_id=User.objects.get(id=user_id)
            print('---------------user',user_id)
            try:
                temp_obj = Favourite.objects.filter(studio=studio_id,musician_user=user_id).last()
                temp_obj.user_id = user_id.id
                temp_obj.is_favourite = is_favourite
                temp_obj.save()
            except Exception as e:
                print("--------------------------458",str(e))
                temp_obj = Favourite.objects.create(studio=studio_id,musician_user=user_id,
                                                        is_favourite=is_favourite)

            data = FavouriteStudioSerializer(temp_obj)
            return response_handler(message='Success', status=True, data=data.data)
        except Exception as e:
            print('----------------------465',str(e))
            m = str(e)
            s = False
            d = {}
            return response_handler(message=m, status=s, data=d)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance:
            self.perform_destroy(instance)
            return response_handler(message='Favourite Removed', status=True, data={})
        else:
            return response_handler(message='data not found', status=False, data={})


class GetSpecificStudioViewSet(viewsets.ModelViewSet):
    queryset = Studio.objects.all()
    serializer_class = StudioSerializers
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        try:
            studio_data=Studio.objects.filter(created_by=request.user.id).last()
            print("5588888888888888 studio_data",studio_data)
            if studio_data == None:
                return response_handler(message='data not found', status=False, data={})
            data1=StudioSerializers(studio_data).data
            return response_handler(message='Success', status=True, data=data1)

        except Exception as e:
            print('580------------------------>',str(e))
            return response_handler(message='Data not Found', status=False, data={})


class RaiseDisputeViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = RaiseDisputeSerializer(data=request.data)
        user = request.user
        if serializer.is_valid():
            studio_id = serializer.data['studio_id']
            studio = Studio.objects.get(id=studio_id)
            raise_dispute = RaiseDispute.objects.create(musician=user, studio=studio, status=True)
            d = []
            m = "Your dispute request has been sent to admin"
            s = True
            return response_handler(message=m, status=s, data=d)

        else:
            m = serialiser_errors(serializer)
            s = False
            data = {}
            return response_handler(message=m, status=s, data=data)

from datetime import datetime, timedelta
import json

from datetime import datetime
class CheckAvailabilityViewset(viewsets.ModelViewSet):
    queryset = Studio.objects.all()
    serializer_class = StudioSerializers
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):

        try:
            appointment_date = request.data['appointment_date']
            print(appointment_date, "______________________appointment_date")
            days = datetime.strptime(appointment_date,"%Y-%m-%d")
            print(days, "_________________944")
            print(type(days), "____________________22222222")
            studio_id = request.data['studio_id']
            day=days.strftime("%A")
            print(day,"tttttttttttttttttt")
            obj_b = Booking.objects.filter(studio_id=studio_id, appointment_date=appointment_date)
            print(obj_b, "__________________________obj")
            st_avail = StudioAvailability.objects.filter(studio_id=studio_id, days=day)
            studio_avail_list = []
            booking_slot_list = []
            time_diff_list = []
            for s in st_avail:
                # print("______________________for loop")
                # print(s.start_time, "_jjjjjjjjjjjjjjj_______________start_time")
                # start_time = s.start_time.replace(s.start_time[:-3:-1], "00")
                # # print(start_time[-2:], "________________start_time")
                # print(start_time, "________________st")
                # print(s.end_time, "____________________before________et")
                #
                # end_time = s.end_time.replace(s.end_time[:-3:-1], "00")
                # print(end_time, "______________________endt")
                # s.save()


                start_time = s.start_time
                end_time = s.end_time
                s_time = datetime.strptime(start_time, "%H:%M:%S")
                e_time = datetime.strptime(end_time, "%H:%M:%S")

                # local_time = convert_to_localtime(e_time)
                # print(e_time, "__________________________e_time")
                # print(local_time, "______________local_time")

                # dt = datetime.strptime(str(e_time - s_time), "%H:%M:%S").time().minute
                # if dt != 00:
                i = s_time
                while i < e_time:
                    print("______________________while_____________1")
                    if str(e_time - i) == "0:30:00":
                        i = i - timedelta(minutes=30)
                    i = i + timedelta(minutes=60)
                    diff = (i-s_time)/60
                    current_time = datetime.now().strftime("%H:%M:%S")
                    current_date = datetime.now().strftime("%Y-%m-%d")
                    d_current = datetime.strptime(current_date, "%Y-%m-%d")
                    t_current = datetime.strptime(current_time, "%H:%M:%S").time()
                    if s_time.time() > t_current and d_current == days:
                        k = str(s_time.time()) + "-" + str(i.time())
                        s_time = i
                        time_diff_list.append({
                            'available_slots': k,
                            'time_difference': diff,
                        })
                        if i == e_time:
                            break
                    elif d_current != days:
                        k = str(s_time.time()) + "-" + str(i.time())
                        s_time = i
                        time_diff_list.append({
                            'available_slots': k,
                            'time_difference': diff,
                        })
                        if i == e_time:
                            break
                    else:
                        s_time = i
                else:
                    i = s_time
                    while e_time < i:
                        print("___________________while_____________2")
                        x = str(i.time())
                        z = str(e_time.time())
                        format = '%H:%M:%S'
                        timea = datetime.strptime(x, format) - datetime.strptime(z, format)
                        if str(timea) == "-1 day, 23:30:00":
                            i = i - timedelta(minutes=30)
                        i = i + timedelta(minutes=60)
                        diff = (i - s_time) / 60
                        k = str(s_time.time()) + "-" + str(i.time())
                        s_time = i
                        time_diff_list.append({
                            'available_slots': k,
                            'time_difference': diff,
                        })
                        if i.time() == e_time.time():
                            break
                # print(time_diff_list,"ggggggggggggggggggggggggg")
                # else:
                #     i = s_time
                #     while i < e_time:
                #         i = i + timedelta(minutes=60)
                #         diff = (i - s_time) / 60
                #         k = str(s_time.time()) + "-" + str(i.time())
                #         s_time = i
                #         time_diff_list.append({
                #             'available_slots': k,
                #             'time_difference': diff,
                #         })
                #         if i == e_time:
                #             break
                for i in obj_b:
                    print(i.time_slot.split(","),"_______________________984")
                    t_slot = i.time_slot.split(",")
                    for j in t_slot:
                        booking_slot_list.append(j)

            for i in time_diff_list:
                if i['available_slots'] not in booking_slot_list:
                    studio_avail_list.append(i)
            m = "Time slots Fetched"
            print(studio_avail_list, "____________________studio_avail_list")
            if len(studio_avail_list)==0:
                m = "No slot available for this date"
            d = studio_avail_list
            s = True
            return response_handler(message=m, status=s, data=d)
        except Exception as e:
            print(str(e))
            d = []
            m = str(e)
            s = False
            return response_handler(message=m, status=s, data=d)




# import pytz
# from django.utils import timezone
#
#
# def convert_to_localtime(utctime):
#   fmt = '%d/%m/%Y %H:%M:%S'
#   utc = utctime.replace(tzinfo=pytz.UTC)
#   localtz = utc.astimezone(timezone.get_current_timezone())
#
#   return localtz.strftime(fmt)



# class CheckAvailabilityViewset(viewsets.ModelViewSet):
#     queryset = Studio.objects.all()
#     serializer_class = StudioSerializers
#     permission_classes = [AllowAny]
#
#     def create(self, request, *args, **kwargs):
#
#         try:
#             appointment_date = request.data['appointment_date']
#             day = datetime.strptime(appointment_date,"%Y-%m-%d")
#             studio_id = request.data['studio_id']
#             day=day.strftime("%A")
#             print(day,"tttttttttttttttttt")
#             obj_b = Booking.objects.filter(studio_id=studio_id, appointment_date=appointment_date)
#             st_avail = StudioAvailability.objects.filter(studio_id=studio_id, days=day)
#             studio_avail_list = []
#             booking_slot_list = []
#             time_diff_list = []
#             for s in st_avail:
#                 start_time = s.start_time
#                 end_time = s.end_time
#                 s_time = datetime.strptime(start_time, "%H:%M:%S")
#                 e_time = datetime.strptime(end_time, "%H:%M:%S")
#                 dt = datetime.strptime(str(e_time - s_time), "%H:%M:%S").time().minute
#                 # if dt != 00:
#                 i = s_time
#                 while i < e_time:
#                     w = 0
#                     while w != 2:
#                         # if str(e_time - i) == "0:30:00":
#                         #     i = i - timedelta(minutes=30)
#                         i = i + timedelta(minutes=30)
#                         diff = (i-s_time)/60
#                         k = str(s_time.time()) + "-" + str(i.time())
#                         s_time = i
#                         time_diff_list.append({
#                             'available_slots': k,
#                             'time_difference': diff,
#                         })
#                         if i == e_time:
#                             break
#                         w+=1
#
#                 # else:
#                 #     i = s_time
#                 #     while i < e_time:
#                 #         w = 0
#                 #         while w != 2:
#                 #             i = i + timedelta(minutes=30)
#                 #             diff = (i - s_time) / 60
#                 #             k = str(s_time.time()) + "-" + str(i.time())
#                 #             s_time = i
#                 #             time_diff_list.append({
#                 #                 'available_slots': k,
#                 #                 'time_difference': diff,
#                 #             })
#                 #             if i == e_time:
#                 #                 break
#                 #             w+=1
#
#                 for d in obj_b:
#                     t_slot = d.time_slot.split(",")
#                     for a in t_slot:
#                         ts = a.split("-")[0]
#                         ts = datetime.strptime(ts, "%H:%M:%S")
#                         te = a.split("-")[1]
#                         te = datetime.strptime(te, "%H:%M:%S")
#                         i = ts
#                         while i < te:
#                             w = 0
#                             while w != 2:
#                                 i = i + timedelta(minutes=30)
#                                 k = str(ts.time()) + "-" + str(i.time())
#                                 booking_slot_list.append(k)
#                                 ts = i
#                                 if i == te:
#                                     break
#                                 w += 1
#             for i in time_diff_list:
#                 if i['available_slots'] not in booking_slot_list:
#                     studio_avail_list.append(i)
#             m = "Time slots Fetched"
#             if len(studio_avail_list)==0:
#                 m = "No slot available for this date"
#             d = studio_avail_list
#             s = True
#             return response_handler(message=m, status=s, data=d)
#         except Exception as e:
#             print(str(e))
#             d = []
#             m = str(e)
#             s = False
#             return response_handler(message=m, status=s, data=d)
