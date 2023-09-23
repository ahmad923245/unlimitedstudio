from django.db.models import Q
from rest_framework import serializers
# from user.models import *
from rest_framework import filters
# from unlimitedstudio.settings import base_url
from datetime import date

from unlimitedstudio.settings import base_url
from user.models import User, VersionControl
from studio.models import Studio
from studio.api.serializers import StudioSerializers

class CheckUserSerializers(serializers.Serializer):
    email = serializers.EmailField(required=True)
    user_type=serializers.CharField(required=False)

class User_serializers(serializers.Serializer):
    first_name=serializers.CharField()
    last_name=serializers.CharField()
    email=serializers.EmailField(required=True)
    #mobile=serializers.CharField(required=False)
    #country_code = serializers.CharField(required=False)
    confirm_password=serializers.CharField(required=True)
    password=serializers.CharField(required=True)
    device_type = serializers.CharField()
    device_token = serializers.CharField()
    fcm_token=serializers.CharField()
    user_type=serializers.CharField(required=True)
    bio=serializers.CharField(required=False)
    notification_status=serializers.BooleanField(required=False)


class User_serializers1(serializers.ModelSerializer):
    profile_image = serializers.SerializerMethodField()
    mobile=serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    user_type = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id","first_name","last_name","last_login",
                  "profile_image","email","country_code","mobile",
                 'is_email_verified',"user_type","is_active","is_sociallogin","strip_Connect_id","strip_customer_id" ,"is_profile_setup", 'is_studio_setup', 'notification_status']

    def get_email(self, user):
        if user.is_sociallogin == True:
            print(user.email,'---------------------53')
            if "@social.id" in user.email:
                email = ''
            else:
                email = user.email
        else:
            email = user.email
        return email

    def get_user_type(self, obj):
        return obj.role.title


    def get_age(self, obj):
        try:
            x = obj.dob
            today = date.today()
            age = today.year - x.year
        except:
            age = None
        return age


    def get_profile_image(self, obj):
        try:
            x = obj.profile_image.url
        except:
            x = None
        return x

    def get_mobile(self, obj):
        if obj.is_sociallogin == True:
            print(obj.email, '---------------------53')
            if "@social.id" in obj.mobile:
                mobile = ''
            else:
                mobile =obj.mobile
        else:
            mobile =obj.mobile
        return mobile

        #print("===== 40 ",obj)
        if obj.is_sociallogin == True:
            return ''
        else:
            return obj.mobile

    def to_representation(self, instance):
        response = super().to_representation(instance)
        user_type = self.context.get('user_type')
        print(user_type, '====================user')
        if user_type == '3':
            s = Studio.objects.filter(created_by=instance.id)
            response['studio_data'] = StudioSerializers(s,many=True).data
        return response






class login_serializers(serializers.Serializer):
    email=serializers.EmailField(required=False)
    mobile = serializers.EmailField(required=False)
    user_type=serializers.CharField(required=True)
    fcm_token=serializers.CharField(required=False)
    device_type = serializers.CharField()
    device_token = serializers.CharField(required=False)
    password=serializers.CharField(required=True)


class Forgot_password(serializers.Serializer):
    email=serializers.EmailField(required=True)

class Forgot_password_reset_serializers(serializers.Serializer):
    password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

class reset_password_serializers(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

class verify_mobile_serializers(serializers.Serializer):
    enter_otp=serializers.CharField(required=True)
    mobile_number = serializers.CharField(required=True)
    country_code = serializers.CharField(required=True)

class verify_email_serializers(serializers.Serializer):
    enter_otp=serializers.CharField(required=False)
    email= serializers.CharField(required=True)
    first_name=serializers.CharField(required=False)
    last_name=serializers.CharField(required=False)
    confirm_password=serializers.CharField(required=False)
    password=serializers.CharField(required=False)
    device_type = serializers.CharField(required=False)
    device_token = serializers.CharField(required=False)
    fcm_token=serializers.CharField(required=False)
    user_type=serializers.CharField(required=False)
    bio=serializers.CharField(required=False)
    notification_status=serializers.BooleanField(required=False)


class resend_email_verification_link_serializers(serializers.Serializer):
    email=serializers.EmailField(required=True)
    user_type=serializers.CharField(required=False)

class resend_otp_serializers(serializers.Serializer):
    country_code = serializers.CharField(required=True)
    mobile=serializers.CharField(required=True)



# class social_login(serializers.Serializer):
#     email = serializers.EmailField(required=False)
#     image_link=serializers.CharField(required=False)
#     name=serializers.CharField(required=False)
#     user_type=serializers.ChoiceField(required=True,choices=type)
#     uid=serializers.CharField(required=True)
#     login_type=serializers.CharField(required=True)
#     mobile=serializers.CharField(required=False)
#     device_token=serializers.CharField(required=True)
#     profile_image=serializers.ImageField(required=False)
#     fcm_token=serializers.CharField(required=False)
#     device_type = serializers.CharField(required=True)


class SocialSignupSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=200, required=False)
    last_name = serializers.CharField(max_length=200, required=False)
    email = serializers.EmailField(max_length=200, required=False)
    country_code = serializers.CharField(max_length=200, required=False)
    mobile = serializers.CharField(max_length=200, required=False)
    device_type = serializers.CharField(max_length=20, required=True)
    device_id = serializers.CharField(max_length=200, required=True)
    social_type = serializers.CharField(max_length=20, required=True)
    social_id = serializers.CharField(max_length=200, required=True)
    user_type = serializers.CharField(required=True)
    profile_image = serializers.ImageField(required=False)


class update_profile_serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =['profile_image', 'email','first_name','last_name','country_code','mobile',]

    def validate(self, data):
        """
        Validation of start and end date.
        """
        mobile=data.get('mobile')
        print('yes------------211')
        if mobile:
            u=User.objects.exclude(id=self.instance.id).filter(
                mobile=mobile).first()
            if u:
                raise serializers.ValidationError("Mobile no. already exit")
        return data


class mobile_serializers(serializers.Serializer):
    user_name=serializers.CharField(required=False)
    email=serializers.EmailField(required=False)
    mobile = serializers.CharField(required=True)
    country_code = serializers.CharField(required=True)

class View_user_profile_seralizer(serializers.Serializer):
    userid =serializers.CharField(required=True)
    type=serializers.CharField(required=False)

class SetNewPasswordSerializers(serializers.Serializer):
    user_id=serializers.CharField(required=True)
    new_password=serializers.CharField(required=True)
    confirm_passsword=serializers.CharField(required=True)

class SettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = VersionControl
        fields = "__all__"

from fcm_django.models import FCMDevice

class FCMSerializer(serializers.Serializer):
    class Meta:
        model = FCMDevice
        fields = '__all__'