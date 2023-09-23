from rest_framework.authentication import TokenAuthentication
from rest_framework import HTTP_HEADER_ENCODING, exceptions
from rest_framework.response import Response
from rest_framework.views import exception_handler
from fcm_django.models import FCMDevice


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
    if response is not None:
        if response.status_code == 401:
            return Response({'message': "Incorrect authentication details, Please check whether you are login or not.", 'code': response.status_code, 'data': response.data.get('detail'), 'error_message': response.data.get('detail','Login required')})
        # print(response.data.get('detail'))
        response.data['status_code'] = response.status_code
        response.data['error_message']=response.data.get('detail')

    return response

def serialiser_errors(serializer):
    for k, error in serializer.errors.items():
        print(k, error[0])
    error_message = " & ".join([f"{k}:-{str(v[0])}" for k, v in serializer.errors.items()])
    return error_message

def response_handler(data,message,status):
    dict={"status":status,"message":message,"data":data}
    return Response(dict)


def device_update(user, registration_id, device_type, device_id="abc"):
    try:
        device, created = FCMDevice.objects.get_or_create(user=user)
        device.registration_id = registration_id
        device.type = device_type
        print('hiiiiiiiiiiiiiiiiiiiiiiiiiii',device.type)
        device.device_id = device_id
        print('ggggggggggggggggggggggggggg',device.device_id)
        device.active = True
        device.save()
    except Exception as ex:
        print(str(ex))