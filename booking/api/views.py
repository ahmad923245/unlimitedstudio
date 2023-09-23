import json
from datetime import date
from time import strftime

from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import *
from user.api.serializers import User_serializers1
from booking.models import *
from setting.models import AdminCharges
from unlimitedstudio.apiutils import *
from django.db.models import Avg
from studio.models import *
import stripe
from unlimitedstudio.settings import *
from user.models import User
from django.shortcuts import render, redirect
from django.urls import reverse
from rest_framework.pagination import PageNumberPagination
import functools
from firebase_admin import *
from firebase_admin.messaging import Message
from firebase_admin.messaging import Notification as fNotification



class StripeBookingPayment(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request):
        serializer = StripeBookingSerializer(data=request.data)
        user = request.user
        if serializer.is_valid():
            amount = int(serializer.validated_data.get('amount'))
            description = serializer.validated_data.get('description')
            currency = serializer.validated_data.get('currency')
            payment_method_types = serializer.validated_data.get('payment_method_types')
            print(type(payment_method_types),'=========================')
            idempotency_key = serializer.validated_data.get('idempotency_key')
            stripe.api_key = STRIPE_SECRET_KEY
            try:
                customer=user.strip_customer_id
                print('customer----->',customer)
            except Exception as e:
                customer=str(e)

            paymentintent = stripe.PaymentIntent.create(
                amount=int(amount)*100,
                currency="usd",
                #payment_method_types=payment_method_types,
                customer=customer,
                description=description,
            )
            m = "Success"
            s = True
            d = paymentintent
            return response_handler(message=m, status=s, data=d)

        else:
            m = serialiser_errors(serializer)
            s = False
            d = {}
            return response_handler(message=m, status=s, data=d)


class BookingViewsets(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingCreateSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, ):
        user = self.request.user
        #print('role----------->',user.role.title)
        #if user.is_musician
        booking_obj = Booking.objects.filter(musician=user.id).order_by('-id')
        data = BookingSerializer(booking_obj, many=True)
        return response_handler(message='Booking list Fetched', status=True, data=data.data)

    def create(self, request):
        serail = BookingAppointmentSerializer(data=request.data)
        if serail.is_valid():

            try:
                user1 = request.user
                studio_id = request.data['studio_id']
                studio = Studio.objects.get(id=studio_id)
                user_id = request.data['user_id']
                user = User.objects.get(id=user_id)
                appointment_date = request.data['appointment_date']
                paid_amount = request.data['paid_amount']
                appointment_time = serail.validated_data.get('appointment_time',None)
                end_time = serail.validated_data.get('appointment_end_time', None)
                time_slot = serail.validated_data.get('time_slot', "")
                print(time_slot, "__________________time_slot")

                # if type(time_slot)==str:
                #     print("__________________time_slot")
                #     time_slot = json.loads(time_slot)

                try:
                    time_slot = time_slot.replace("[", "").replace("]", "").replace('"', '')
                except:
                    pass
                # end_time = request.data['appointment_end_time']
                # try:
                #
                #     appointment_time = request.data['appointment_time']
                #     end_time = request.data['appointment_end_time']
                #     # if appointment_time == '' or end_time == '':
                #     #     appointment_time = strftime("23:59:59")
                #     #     end_time = strftime("23:59:59")
                #
                # except:
                #     appointment_time= strftime("23:59:59")
                #     end_time =  strftime("23:59:59")
                #



                try:
                    paymentintentid = request.data['paymentIntentId']
                except:
                    paymentintentid = 'NA'
                try:
                    payment_method_nonce = request.data['payment_method_nonce']
                except:
                    payment_method_nonce = 'NA'

                try:
                    transaction_id = request.data['transaction_id']
                    print('transaction_id : ', transaction_id)
                except:
                    transaction_id = 'NA'

                try:
                    payment_status = request.data['payment_status']
                    print('payment_status : ', payment_status)
                except:
                    payment_status = 'NA'

                try:
                    service_id = request.data['service_id']
                    service_id = service_id.split(',')
                    services_data = Services.objects.filter(id__in=service_id)
                    services = []
                    for i in services_data:
                        services.append(i.ServiceName)

                    services = ','.join(services)
                except:
                    services = ''

                # d = strftime("23:59:59")

                temp_obj = Booking.objects.create(studio=studio,musician=user,
                                                appointment_date=appointment_date,
                                                paid_amount=paid_amount,
                                                appointment_time=appointment_time,
                                                end_time=end_time,
                                                time_slot=time_slot,
                                                payment_method_nonce=payment_method_nonce,
                                                transaction_id=transaction_id,
                                                payment_status=payment_status,
                                                service_id=services)

                paymentintentobj = PaymentIntent.objects.create(paymentintentid=paymentintentid,
                                                                created_by=user1,
                                                                status=payment_status
                                                                )
                bookingpaymentobj=BookingPayment.objects.create(
                                                            customer_id=user.strip_customer_id,
                                                            booking=temp_obj,
                                                            payment_method_nonce=payment_method_nonce,
                                                            transaction_id=transaction_id,
                                                            amount=paid_amount,
                                                            status=payment_status,
                                                            musician=user1,
                                                            studio=studio
                                                            )
                data = BookingCreateSerializer(temp_obj)

                try:
                    title="New session request from "+ str(user.first_name)

                    fcmdevice = FCMDevice.objects.get(
                        user__id=studio.created_by.id)
                    print(fcmdevice, "FCM Device____________________________")
                    notification = messaging.Notification(
                    title=title,
                    body="You receive new session request",)
                    k = messaging.Message(
                        notification=notification,
                        data={
                            'data':"",
                            'id': str(temp_obj.id),
                            'title': title,
                            'message': "You receive new booking request.",
                            'type': 'New_Booking_Received',
                        },


                        token=str(fcmdevice.registration_id))
                    x = fcmdevice.send_message(k)
                    print("Notification Fired--------------------->", x)
                    Notifications.objects.create(user=studio.created_by,title=title,
                        message="You receive new session request", type="New_Booking_Received", booking_id = str(temp_obj.id))

                except Exception as e:
                    print(str(e),"429999999999999999999999")
                    print("wdqwdwqdqwdqwdqwdwq")
                return response_handler(message='Success', status=True, data=data.data)
            except Exception as e:
                print('----------------------36',str(e))
                m = str(e)
                s = False
                d = {}
                return response_handler(message=m, status=s, data=d)

    def update(self, request, *args, **kwargs):
        data1 = super(BookingViewsets, self).update(request, args, *kwargs)
        try:
            y= data1.data['appointment_date']
            x1=datetime.strptime(y, "%Y-%m-%d").strftime("%m-%d-%Y")
            title=str(data1.data['studio']['studio_name'])+" has accepted your session request for "+x1
            print(title, "___________title")
            user1=User.objects.get(email=data1.data['musician']['email'])
            fcmdevice = FCMDevice.objects.get(user=user1)
            notification = messaging.Notification(
            title=str(title),
            body=str(title),)
            k = messaging.Message(
                notification=notification,
                data={
                    'id':str(data1.data['id']),
                    'title': str(title),
                    'message': str(title),
                    'type': 'Booking_Accepted',
                },
                token=str(fcmdevice.registration_id))
            x = fcmdevice.send_message(k)
            Notifications.objects.create(user=user1, title=str(title),
                                         message=str(title), type="Booking_Accepted", booking_id =str(data1.data['id']) )

        except Exception as e:
            print(str(e),"Booking Accepted")
            print("Booking Accepted------------->")
        # try:
        #     user1=User.objects.get(email=data1.data['musician']['email'])
        #     fcmdevice = FCMDevice.objects.get(
        #         user=user1)
        #     print(fcmdevice,'============169')
        #     k = Message(notification=fNotification(
        #         title="Booking Accepted by service provider",
        #         body=str({"Booking_id":"234"})))
        #     x = fcmdevice.send_message(k)
        # except Exception as e:
        #     print(str(e),"579999999999999")
        #     print("Accepted True")
        return response_handler(message='Booking Updated Successfully', status=True, data=data1.data)


class MyTransactionViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        user = request.user
        if user.role.title == "MUSICIAN":
            transaction = BookingPayment.objects.filter(musician=user)
            paginator = PageNumberPagination()
            paginator.page_size = 10
            transaction_page = paginator.paginate_queryset(transaction, request)

            if len(transaction) > 0:
                d = MusicianTransactionSerializer(transaction_page, many=True)
                data = paginator.get_paginated_response(d.data)
                d = data.data
                m = "transaction  deatils fatched successfully"
                s = True
                return response_handler(message=m, status=s, data=d)
            m = "transaction deatils list is empty"
            s = True
            data = {}
            return response_handler(message=m, status=s, data=data)

        else:
            studio = Studio.objects.filter(created_by=user).last()
            transaction = BookingPayment.objects.filter(studio=studio,status="succeeded",cashout_status=False,booking__accepted=True).order_by('-id')
            amount = transaction.values_list('amount', flat=True)
            amount = list(map(int, amount))
            try:
                total_amount = functools.reduce(lambda a, b: a + b, amount)
            except:
                total_amount=amount
            paginator = PageNumberPagination()
            paginator.page_size = 10
            transaction_page = paginator.paginate_queryset(transaction, request)

            if len(transaction) > 0:
                d = Service_ProviderTransactionSerializer(transaction_page, many=True)
                data = paginator.get_paginated_response(d.data)
                d = data.data
                d["total_amount"] = total_amount
                m = "transaction  deatils fatched successfully"
                s = True
                return response_handler(message=m, status=s, data=d)
            m = "transaction deatils list is empty"
            s = True
            data = {}
            return response_handler(message=m, status=s, data=data)


class BookingTypeListViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        studio_id = request.data['studio_id']
        print('studio_id-------------27', studio_id)
        studio = Studio.objects.get(id=studio_id)
        print('studio', studio)
        booking_status = request.data['booking_status']

        if booking_status == "Pending":
            data = Booking.objects.filter(studio=studio, accepted=False, cancelled=False, decline=False).order_by('-id')
        elif booking_status == 'Ongoing':
            import datetime
            today = datetime.date.today()
            print('today=====================77', today)
            data = Booking.objects.filter(studio=studio, accepted=True, cancelled=False, decline=False,appointment_date__gte=today).order_by('-id')
        elif booking_status == "Completed":
            import datetime
            today = datetime.date.today()
            print('today=====================77', today)
            data=Booking.objects.filter(studio=studio, appointment_date__lt=today).order_by('-id')
        else:
            m = "data not found"
            s = False
            d = {}
            return response_handler(message=m, status=s, data=d)
        m = "Booking list fetched"
        s = True
        d = BookingSerializer(data, many=True)
        return response_handler(message=m, status=s, data=d.data)


class RecentBookingListViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request):
        try:
            studio_id = request.data['studio_id']
            status = request.data['status']
            print('status---------------92', status)
            print('studio id------------------------------------', studio_id, type(studio_id))
            print('------------------>94', status==False)
            if status == 'False':
                booking_obj = Booking.objects.filter(studio__id=studio_id,cancelled=False, accepted=False, decline=False).order_by('-id')
                booking_data = BookingSerializer(booking_obj, many=True)
                #print('booking_data',booking_data)
                d = booking_data.data
                m = "Recent Booking List Fetched"
                s = True
                return response_handler(message=m, status=s, data=d)
            else:
                booking_obj = Booking.objects.filter(studio__id=studio_id,decline=False,accepted=True).order_by('-id')
                booking_data = BookingSerializer(booking_obj, many=True)
                #print('Accept Booking Listing',booking_data)
                d = booking_data.data
                m = "Accepted Booking List Fetched"
                s = True
                return response_handler(message=m, status=s, data=d)
        except Exception as e:
            print('exception in recent booking list', str(e))
            d = {}
            m = 'Booking Data Not Found'
            s = False
        return response_handler(message=m, status=s, data=d)


class BookingType_MusicianList_ViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user.id
        booking_status = request.data['booking_status']

        if booking_status == "Pending":
            data = Booking.objects.filter(musician=user, accepted=False, cancelled=False, decline=False).order_by('-id')
        elif booking_status == 'Ongoing':
            import datetime
            today = datetime.date.today()
            print('today=====================77', today)
            data = Booking.objects.filter(musician=user, accepted=True, cancelled=False, decline=False,appointment_date__gte=today).order_by('-id')
        elif booking_status == "Completed":
            import datetime
            today = datetime.date.today()
            print('today=====================77', today)
            data=Booking.objects.filter(musician=user, appointment_date__lt=today).order_by('-id')
        else:
            m = "data not found"
            s = False
            d = {}
            return response_handler(message=m, status=s, data=d)
        m = "Booking list fetched"
        s = True
        d = BookingSerializer(data, many=True)
        return response_handler(message=m, status=s, data=d.data)

# class BookingTypeListViewSet(viewsets.ModelViewSet):
#     queryset = Booking.objects.all()
#     serializer_class = BookingSerializer
#     permission_classes = [IsAuthenticated]

#     def list(self, request, *args, **kwargs):
#         print(request.GET.get('type'))
#         type = request.GET.get('type')
#         if type == "Ongoing":
#             data=Booking.objects.all()
#         elif type=='Completed':
#             data=Booking.objects.all()
#         elif type=="Pending":
#             data=Booking.objects.all()
#         else:
#             m = "data not found"
#             s = False
#             d = {}
#             return response_handler(message=m, status=s, data=d)
#         m = "Booking list fetched"
#         s = True
#         d = BookingSerializer(data,many=True)
#         return response_handler(message=m, status=s, data=d.data)



    # def destroy(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     if instance:
    #         self.perform_destroy(instance)
    #         return response_handler(message='Favourite Removed', status=True, data={})
    #     else:
    #         return response_handler(message='data not found', status=False, data={})



def stripe_view(request):
    stripe.api_key = STRIPE_SECRET_KEY
    code = request.GET.getlist("code")
    state = request.GET.getlist("state")
    # print("========= 422 ", code[0])
    # print("============= 423 ", state[0])
    response = stripe.OAuth.token(
        grant_type="authorization_code",#state[0] ,#'authorization_code',
        code=code[0],
    )
    connected_account_id = response['stripe_user_id']
#    try:
    usr = User.objects.get(strip_customer_id=state[0])
    usr.strip_Connect_id = connected_account_id
    usr.save()
    # print("================== 431 ",connected_account_id)
    return redirect('stripe_successfully')
    # x=TermsConditions.objects.get(active=True)
    # context = {'content': x.content}

def stripe_successfully(request):
    from django.http import HttpResponse
    return HttpResponse("<h1> Stripe account created Successfully </h1>")

    #return render(request, 'stripe_successfully.html')

class stripe_connect(viewsets.ViewSet):
    def list(self, request):
        stripe.api_key = STRIPE_SECRET_KEY
        user = request.user
        # print('-----------------')
        if user.strip_Connect_id == None or user.strip_Connect_id == '':
            strip_client_id = STRIPE_CLIENT_ID
            state = user.strip_customer_id
            email = user.email
            if state == None:
                try:
                    Name = user.username
                except:
                    Name = " "

                strip_customer = stripe.Customer.create(
                    description=Name,
                    email=user.email
                )
                # print("hiii 2197 ")
                state = strip_customer.id
                xyu = User.objects.get(id=user.id)
                xyu.strip_customer_id = state
                # print("user ======", user.id)
                xyu.save()
            else:
                pass
            stripe_redirect_url= "http://{}{}".format(request.META['HTTP_HOST'], reverse('stripe'))
            # print(stripe_redirect_url)
            # x="https://connect.stripe.com/express/oauth/authorize?redirect_uri=https://python.demo2server.com/stripe/&client_id=ca_IX0lV9HJz6Ixb85otJnzc3GzQvF37XFV&state={}&stripe_user[email]={}&scope=read_write&always_prompt=tru#/".format(state,email)
            strip_url = "https://connect.stripe.com/express/oauth/authorize?redirect_uri={}&client_id={}&state={}&stripe_user[email]={}&scope=read_write&always_prompt=tru#/".format(
                stripe_redirect_url, strip_client_id, state, email)
            dict = {"status": bool("true"), "message": "successfull ", "data": strip_url}
            return Response(dict)
        # return Response({"code": 200, 'message': message, "data": serializer.data, "error_message": ""})
        else:
            return Response("Having ID")

class PaymentIntentViewset(viewsets.ModelViewSet):
    queryset = PaymentIntent.objects.all()
    serializer_class = PaymentIntentSerializer



class MusicianCancleBooking(viewsets.ModelViewSet):
    http_method_names = ['post', 'head']
    serializer_class = MusicianCancleBookingSerializers

    def create(self, request):
        stripe.api_key = STRIPE_SECRET_KEY
        serializer = MusicianCancleBookingSerializers(data=request.data)
        user = request.user 
        try:
            booking_id = request.data['booking_id']
            booking_obj = Booking.objects.get(id=booking_id)
            print('booking_id----------------',booking_id)
            # today = date.today()
            # print(" date : ", today)
            # print(" date type  : ", type(today))
            # from datetime import datetime
            # tym = datetime.now()
            # current_time = tym.time()  # .strftime("%H:%M:%S")
            # print(type(current_time), current_time, '============944')
            # c_dt = datetime.combine(today, tym.time())
            #
            # booking_tym = booking_obj.appointment_time
            # booking_date=booking_obj.appointment_date
            # booking_dt = datetime.combine(booking_date, booking_tym)
            #
            # print("obj :", booking_dt)
            # print("obj :", c_dt)
            # # time_delta = booking_dt - c_dt
            # time_delta = booking_dt - c_dt
            # total_time = (time_delta.seconds * 24) // 60
            # print('time_delta---------------', total_time)

            # if total_time < 2880:
            tran_obj = BookingPayment.objects.filter(booking=booking_obj).last()
            if tran_obj:
                print('in tran_obj-----')
                payment_intent_id = tran_obj.transaction_id
                result = stripe.Refund.create(payment_intent=payment_intent_id)
                print(result)
                if result.status == 'succeeded':
                    amount = tran_obj.amount
                    transaction_id = result.id
                    booking_obj.cancelled=True
                    booking_obj.save()
                    BookingPayment.objects.create(musician=user,
                                                    customer_id=tran_obj.customer_id,
                                                    transaction_id=transaction_id,
                                                    amount=amount,
                                                    booking=booking_obj,
                                                    studio=booking_obj.studio,
                                                    payment_method_nonce=tran_obj.payment_method_nonce,
                                                    status='refund')
                    tran_obj.status = 'refund'
                    tran_obj.save()

                    try:
                        fcmdevice = FCMDevice.objects.get(
                            user=tran_obj.studio.created_by)
                        title =str(user.first_name)+ " has canceled their session on "+ str(booking_obj.appointment_date.strftime("%m-%d-%Y"))
                        notification = messaging.Notification(
                        title=title,
                        body=title,)
                        k = messaging.Message(
                            notification=notification,
                            data={
                                'id':str(booking_obj.id),
                                'title': title,
                                'message': title,
                                'type': 'Booking_Cancelled',
                            },
                            token=str(fcmdevice.registration_id))
                        x = fcmdevice.send_message(k)
                        Notifications.objects.create(user=tran_obj.studio.created_by,
                                                     title=title,
                                                     message=title, type="Booking_Cancelled",
                                                     booking_id = str(booking_obj.id))


                    except Exception as e:
                        print(str(e),"------------------------>")
                        print("Booking cancelled by Musician")

            data = {'result': result}
            m = "Booking cancelled successfully and payment refund"
            s = True
            return response_handler(message=m, status=s, data=data)

            # else:
            #     m = "You can only cancel booking 48 hours prior to the booking date"
            #     s = False
            #     return response_handler(message=m, status=s, data={})

        except Exception as e:
            m = str(e)
            s = False
            data = {}
            return response_handler(message=m, status=s, data=data)



                      

        


class Service_ProviderBookingCancel(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        stripe.api_key = STRIPE_SECRET_KEY
        try:
            user = request.user
            studio = Studio.objects.filter(created_by=user).last()
            booking_id = request.data['booking_id']
            print('booking_id-------------->',booking_id)
            try:
                booking_obj = Booking.objects.get(id=booking_id)
                tran_obj = BookingPayment.objects.filter(booking=booking_obj).last()
                # today = date.today()
                # print(" date : ", today)
                # print(" date type  : ", type(today))
                # from datetime import datetime
                # tym = datetime.now()
                # current_time = tym.time()  # .strftime("%H:%M:%S")
                # print(type(current_time), current_time, '============944')
                # c_dt = datetime.combine(today, tym.time())
                #
                # booking_tym = booking_obj.appointment_time
                # booking_date = booking_obj.appointment_date
                # booking_dt = datetime.combine(booking_date, booking_tym)
                #
                # print("obj :", booking_dt)
                # print("obj :", c_dt)
                # # time_delta = booking_dt - c_dt
                # time_delta = booking_dt - c_dt
                # total_time = (time_delta.seconds * 24) // 60
                # print('time_delta---------------', total_time)
                #
                # if total_time < 2880:
                if tran_obj:
                    transaction_id = tran_obj.transaction_id
                    result = stripe.Refund.create(payment_intent=transaction_id)
                    print(result)
                    if result.status == 'succeeded':
                        amount = tran_obj.amount
                        transaction_id = result.id
                        booking_obj.decline = True
                        booking_obj.accepted = False
                        booking_obj.save()
                        BookingPayment.objects.create(musician=tran_obj.musician,
                                                      customer_id=tran_obj.customer_id,
                                                      transaction_id=transaction_id,
                                                      amount=amount,
                                                      booking=booking_obj,
                                                      payment_method_nonce=tran_obj.payment_method_nonce,
                                                      studio=studio,
                                                      status='refund')
                        tran_obj.status = 'refund'
                        tran_obj.save()

                        data = {'result': result}
                        m = "Booking cancelled successfully and payment refund"
                        s = True
                        try:
                            title = str(booking_obj.studio.studio_name) +" has rejected your session request for "+ str(booking_obj.appointment_date.strftime("%m-%d-%Y"))
                            fcmdevice = FCMDevice.objects.get(
                                user=tran_obj.musician)
                            notification = messaging.Notification(
                            title=title,
                            body=title,)
                            k = messaging.Message(
                                notification=notification,
                                data={
                                    'id':str(booking_obj.id),
                                    'title': title,
                                    'message': title,
                                    'type': 'Booking_Declined',
                                },
                                token=str(fcmdevice.registration_id))
                            x = fcmdevice.send_message(k)
                            Notifications.objects.create(user=tran_obj.musician,
                                                         title=title,
                                                         message=title,
                                                         type="Booking_Declined",
                                                         booking_id = str(booking_obj.id))
                        except Exception as e:
                            print(str(e),"3333333333333333333333333333333")
                            print("Booking_Declined")

                        return response_handler(message=m, status=s, data=data)
                # else:
                #     m = "You can only cancel booking 48 hours prior to the booking date"
                #     s = False
                #     data = {}
                #     return response_handler(message=m, status=s, data=data)
                #

            except Exception as e:
                m = str(e)
                s = False
                data = {}
                return response_handler(message=m, status=s, data=data)    
                
        except Exception as e:
            print('----------------------36', str(e))
            m =  str(e)
            s = False
            d = {}
            return response_handler(message=m, status=s, data=d)


class ServiceProviderPayoutTransaction(viewsets.ViewSet):
    def list(self, request):
        from datetime import date
        today = date.today()

        try:
            stripe.api_key = STRIPE_SECRET_KEY
            user = request.user 
            studio_strip_Connect_id = User.objects.get(id=user.id).strip_Connect_id
            print('studio_strip_Connect_id',studio_strip_Connect_id)
            # if studio_strip_Connect_id=='' or studio_strip_Connect_id == None:
            #     return response_handler(message='Please Create Your Strip Account', status=False, data={})

            studio_id = Studio.objects.get(created_by=user).id
            print(studio_id, "______________589")
            bookings = BookingPayment.objects.filter(studio=studio_id, booking__decline=False, booking__cancelled=False, booking__accepted=True, cashout_status=False, booking__appointment_date__lt=today)
            print(len(bookings), "__________________________________591")
            if bookings.count() == 0:
                m = "You have not any pending amount and remaining amount request accept after service completed"
                s = False
                data = {}
                return response_handler(message=m, status=s, data=data)
                            
            for i in bookings:
                try:
                    booking_paid_amount = i.amount
                    booking_paid_amount=booking_paid_amount
                    print('booking_paid_amount',booking_paid_amount)
                    if booking_paid_amount and booking_paid_amount != None and float(booking_paid_amount) > 0:
                        try:
                            adminCommision = int(AdminCharges.objects.last().admin_percentes)
                        except:
                            adminCommision = 10
                        commission_amount=float(booking_paid_amount)*float(adminCommision/100)
                        print('commission_amount',commission_amount)    
                        payable_amount = float(booking_paid_amount)-commission_amount
                        print('payable_amount------------',payable_amount)
                        result = stripe.Transfer.create(
                            amount=int(payable_amount*100),
                            currency="usd",
                            destination=studio_strip_Connect_id,
                            transfer_group='amount paid',
                        )
                        print(result,'===============rsult')
                        i.cashout_status = True

                        i.admincommision = commission_amount
                        i.cashout_date = today
                        i.save()
                        print(i.cashout_status, "____________618")

                except Exception as e:
                    print('eeeeeeeeeeeeeeeeeeeeeeeeee', str(e))
                    pass

            m = "Cashout Request Accepted"
            s = True
            data = {}
            return response_handler(message=m, status=s, data=data)
        except Exception as e:
            m = "Some Technical Issue"
            s = False
            data = str(e)
            return response_handler(message=m, status=s, data=data)


class UserNotificationViewset(viewsets.ModelViewSet):
    queryset = Notifications.objects.all()
    serializer_class = NotificationListSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Notifications.objects.filter(user=self.request.user)


    def create(self, request):
        user = request.user
        serializer = NotificationOnOffSerializer(data=request.data)
        if serializer.is_valid():
            status = serializer.data['status']
            user = User.objects.get(id=user.id)
            if status == 'True':
                user.notification_status = status
                user.save()
                data = User_serializers1(user)
                d = data.data
                m = "Notification are on now."
                s = True
                return response_handler(message=m, status=s, data=d)
            else:
                user.notification_status = False
                user.save()
                data = User_serializers1(user)
                d = data.data
                m = "Notifications are off now."
                s = True
                return response_handler(message=m, status=s, data=d,)
        else:
            m = serialiser_errors(serializer)
            s = False
            data = {}
            return response_handler(message=m, status=s, data=data)

    def list(self, request, *args, **kwargs):
        paginator = PageNumberPagination()
        paginator.page_size = 10
        user = request.user
        try:
            try:
                notification = Notifications.objects.filter(user=user.id).order_by('-id')
                notification.update(is_read=True)
                print(notification, "________________________797")
            except:
                notification = Notifications.objects.filter(user=user.id).order_by('-id')
                print(notification, "__________________________________800")

            notification = paginator.paginate_queryset(notification, request)
            notification = NotificationListSerializer(notification, many=True)
            paginated_data = paginator.get_paginated_response(notification.data)

            d = paginated_data.data
            m = "Notification List Fetched"
            s = True
            return response_handler(message=m, status=s, data=d)

        except Exception as e:
            m = "data not found"
            s = False
            data = str(e)
            return response_handler(message=m, status=s, data=data)

    # def list(self, request, *args, **kwargs):
    #     paginator = PageNumberPagination()
    #     paginator.page_size = 10
    #     user = request.user
    #     try:
    #         notification = Notifications.objects.filter(user=user.id)
    #         notification = paginator.paginate_queryset(notification, request)
    #         notification = NotificationListSerializer(notification, many=True)
    #         paginated_data = paginator.get_paginated_response(notification.data)
    #
    #         d = paginated_data.data
    #         m = "Notification List Fetched"
    #         s = True
    #         return response_handler(message=m, status=s, data=d)
    #
    #     except Exception as e:
    #         m = "data not found"
    #         s = False
    #         data = str(e)
    #         return response_handler(message=m, status=s, data=data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance:
            self.perform_destroy(instance)
            return response_handler(message='Notification Removed Successfully', status=True, data={})
        else:
            return response_handler(message='id not found', status=False, data={})



class CheckNotificationViewsets(viewsets.ModelViewSet):
    queryset = Notifications.objects.all()
    serializer_class = NotificationListSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, ):
        user = self.request.user
        #print('role----------->',user.role.title)
        #if user.is_musician
        notification_obj = Notifications.objects.filter(user=user, is_read=False).count()
        context={'count': notification_obj}
        return response_handler(message='Unread Notifications Fetched', status=True, data=context)


from datetime import datetime
def today_bookings(request):
    today = datetime.today()
    print(today, "___________Today's date")

    booking_obj = Booking.objects.filter(appointment_date=today).order_by('-id')
    musician = booking_obj.values_list('musician', flat=True)
    print('musician', musician)
    try:
        for i in musician:
            user =User.objects.get(id=i)
            fcmdevice = FCMDevice.objects.filter(
                user=user).last()
            notification = messaging.Notification(
                title="Today's Booking Reminder",
                body="Today you have Booking Schedule", )
            k = messaging.Message(
                notification=notification,
                data={
                    'data': {},
                    'id': {},
                    'title': "Booking Reminder.",
                    'message': "Today you have Booking Schedule.",
                    'type': 'New_Booking_Reminder',
                },
                token=str(fcmdevice.registration_id))

            # x = fcmdevice.send_message(k)
            Notifications.objects.create(user=user, title='Booking Reminder.',
                                         message="Today you have Booking Schedule.", type="New_Booking_Reminder",
                                         booking_id='')

    except Exception as e:
        print(str(e), "except block")
    return HttpResponse("OK")
