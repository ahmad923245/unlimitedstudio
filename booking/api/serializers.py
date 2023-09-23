from rest_framework import serializers
from ..models import *
from studio.api.serializers import *
from user.serializers import*
from unlimitedstudio.settings import base_url


class BookingAppointmentSerializer(serializers.Serializer):
    appointment_time = serializers.TimeField(required=False)
    appointment_end_time = serializers.TimeField(required=False)
    time_slot = serializers.CharField(required=False)
class BookingSerializer(serializers.ModelSerializer):
    studio = StudioSerializers(required=False)
    class Meta:
        model = Booking
        fields = "__all__"


class BookingCreateSerializer(serializers.ModelSerializer):
    studio = StudioSerializers(required=False)
    musician = User_serializers1(required=False)
    time_slot= serializers.SerializerMethodField()
    class Meta:
        model = Booking
        fields = "__all__"

    def get_time_slot(self, obj):

        try:
            time_slots = obj.time_slot.split(",")

            time_slots=[item.replace("'", "") for item in time_slots]
        except:
            time_slots = []
        return time_slots


class BookingStudioSerializers(serializers.ModelSerializer):
    class Meta:
        model =Studio
        fields = ['id','studio_name']

class BookingSerializer(serializers.ModelSerializer):
    studio = BookingStudioSerializers(required=False)
    musician = User_serializers1(required=False)
    time_slot= serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = "__all__"

    def get_time_slot(self, obj):

        try:
            time_slots = obj.time_slot.split(",")

            time_slots = [item.replace("'", "") for item in time_slots]
        except:
            time_slots = []
        return time_slots

    def to_representation(self, instance):
        response = super().to_representation(instance)
        accepted = instance.accepted
        if accepted == True:
            response['reserved_date'] = instance.appointment_date

        return response


class PaymentIntentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentIntent
        fields = "__all__"


class MusicianCancleBookingSerializers(serializers.Serializer):
    booking_id=serializers.CharField(required=True)


class StripeBookingSerializer(serializers.Serializer):
    amount = serializers.CharField(required=True, allow_blank=True)
    description = serializers.CharField(required=False, allow_blank=False)
    currency = serializers.CharField(required=False, allow_blank=False)
    source = serializers.CharField(required=False, allow_blank=False)
    payment_method_types = serializers.CharField(required=False, allow_blank=False)
    idempotency_key = serializers.CharField(required=False, allow_blank=True)


class MusicianTransactionSerializer(serializers.ModelSerializer):
    studio_name = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    class Meta:
        model = BookingPayment
        fields = "__all__"

    def get_studio_name(self, obj):
        try:
            studio = obj.studio.studio_name
        except:
            studio = ""
        return studio

    def get_image(self, obj):
        try:
            studio_image = StudioImage.objects.get(studio_img=obj.studio.id)
            image =  studio_image.image.url
        except:
            image = ""
        return image


class Service_ProviderTransactionSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = BookingPayment
        fields = "__all__"

    def get_username(self, obj):
        try:
            studio = obj.musician.first_name
        except:
            studio = ""
        return studio

    def get_image(self, obj):
        try:
            # studio_image = StudioImage.objects.get(studio_img=obj.studio.id)
            image = obj.musician.profile_image.url
        except:
            image = ""
        return image


class NotificationOnOffSerializer(serializers.Serializer):
    status = serializers.CharField(required=True)


class NotificationListSerializer(serializers.ModelSerializer):
    icon=serializers.SerializerMethodField()
    class Meta:
        model = Notifications
        fields = "__all__"

    def get_icon(self, obj):
        try:
            icon = obj.user.email[0]
        except:
            icon = ""
        return icon



class UserChatSerializer(serializers.ModelSerializer):
    profile_image = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "profile_image"]
    def get_profile_image(self, obj):
        x = None
        if obj.profile_image:
            x = obj.profile_image.url
        return str(x)    


class ChatMessageSerializer(serializers.ModelSerializer):
    sender = UserChatSerializer()
    receiver = UserChatSerializer()
    image = serializers.SerializerMethodField()
    thumbnail_image = serializers.SerializerMethodField()

    class Meta:
        model = ChatMessage
        fields = "__all__"

    def get_image(self, obj):
        x = None
        if obj.image:
            x =obj.image
        return x

    def get_thumbnail_image(self, obj):
        x = None
        if obj.thumbnail_image:
            x = obj.thumbnail_image
        return x


class ChatconverstionSerializer(serializers.ModelSerializer):
    sender =UserChatSerializer()
    receiver =UserChatSerializer()
    class Meta:
        model = Conversation
        fields='__all__'

    def to_representation(self, instance):
        # user = self.context['request'].user
        #current_user = self.context['current_user']
        response = super().to_representation(instance)
        #response['block'] = False
        #response['is_myside_block'] = False
        #y = BlockUser.objects.filter(Q(created_by__id=current_user) | Q(users__id=current_user))
        
        #count_obj = ChatMessage.objects.filter(conversation_id=instance,receiver = current_user).count()
        #print(count_obj, '===========count_obj====================count_obj=============498')
        #if len(y) > 0:
        #    response['block'] = True
        #print(x, '====================501')
        #myblock = BlockUser.objects.filter(created_by__id=current_user).first()
        #print('---------------------------------501', myblock)
        #response['message_count'] = count_obj
        #if myblock:
        #    response['is_myside_block'] = True
        try:
            x = ChatMessage.objects.filter(conversation_id=instance).last()
            response['last_message'] = x.message
            #response['last_message_time']=x.message_at
        except Exception as e:
            response['last_message'] = ''
            #response['last_message_time']=str(e)
            print('Exception in ChatconverstionSerializer 195',str(e))
        return response