from django.db.models import Q
from rest_framework import serializers
from user.models import *
from rest_framework import filters

from datetime import date

# class QrcodeSerilizer(serializers.ModelSerializer):
#     image = serializers.SerializerMethodField()
#     class Meta:
#         model= QrCode
#         fields=['image']
#
#     def get_image(self,obj):
#         try:
#             x = (base_url + obj.image.url)
#         except:
#             x = None
#         return x
#
# class ProfileImage_Serilizer(serializers.ModelSerializer):
#     image=serializers.SerializerMethodField()
#     class Meta:
#         fields='__all__'
#         model= ProfileImage
#
#     def get_image(self,obj):
#         try:
#             x = (base_url + obj.image.url)
#         except:
#             x = None
#         return x
from unlimitedstudio.utils import create_status

class User_serializers(serializers.ModelSerializer):
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


class User_serializers1(serializers.ModelSerializer):
    actions=serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email','mobile','actions',"profile_image"]#"__all__"

    page_url = "user"

    def get_actions(self,obj):


        return ''
    def get_profile_image(self, obj):
        try:
            x = obj.profile_image.url
        except:
            x = None
        return x
    def to_representation(self, instance):
        response = super().to_representation(instance)
        # s = ProfileImage.objects.filter(user=instance.id)
        # image = ProfileImage_Serilizer(s, many=True)

        # Qrcode_image = QrCode.objects.filter(user=instance.id).first()
        # x = QrcodeSerilizer(Qrcode_image, many=True)
        # try:
        #     qrcode=base_url +Qrcode_image.image.url
        # except:
        #     qrcode = None
        #
        # plan = Subscription.objects.filter(purchase_by=instance.id, status=True).first()
        # if plan:
        #     response['subcription_plan'] = plan.plan.plan_type
        #     response['premium'] = True
        # else:
        #     response['subcription_plan'] = None
        #     response['premium'] = False
        # response['Qrcode_image'] = qrcode
        # response['following'] = str(following)
        # response['followers'] = str(followers)

        response['status']=create_status(instance.status, instance.id, {"1": "Active", "0": "Inactive"},'user.updateStatus')
        # response['actions'] = " "
        return response