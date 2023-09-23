from user.models import *
import socketio
from booking.api.serializers import *
sio = socketio.Server(cors_allowed_origins='*', allowEIO3=True,ping_interval=25)
# @sio.event
# def connect(sid, environ, auth):
#     print("I'm connected!")
from unlimitedstudio.apiutils import *
from firebase_admin import *
from firebase_admin.messaging import Message
from firebase_admin.messaging import Notification as fNotification
@sio.event
def connect(sid, environ, auth):
    print('query string at socket connection',environ)
    ar = environ['QUERY_STRING'].split('user_id')[1]
    user_id = ar.split("&")[0].replace('=', '')
    try:
        user_id = int(user_id)
        user = User.objects.get(id=user_id)
        try:
            session = UserSession.objects.get(user=user)
            session.session_id = sid
            session.is_online = True
            session.save()
            # chat_obj = ChatMessage.objects.filter(receiver=user_id, seen='0').update(seen='1')
            # print(chat_obj, '=======chat_obj==========')
            sio.emit('event_response', {'data': 'session updated'}, to=sid)
        except:
            sio.emit('event_response', {'data': "nnnnnnnnnnnadnandad"}, to=sid)
            UserSession.objects.create(user=user, session_id=sid)
            # chat_obj = ChatMessage.objects.filter(receiver=user_id, seen='0').update(seen='1')
    except:
        msg = 'Invalid user_id'
        sio.emit('event_response', {'data': msg}, to=sid)


@sio.on('send_message')
def send_message(sid, data):
    sender_id = data['sender_id']
    receiver_id = data['receiver_id']
    print("________________41")
    try:
        message = data['message']
    except:
        message = None
    try:
        message_type = data['message_type']
    except:
        message_type = None
    try:
        image = data['image']
    except:
        image = None
    try:
        thumbnail_image = data['thumbnail_image']
    except:
        thumbnail_image = None

    print("sender_id here:", sender_id)
    print("receiver_id here:", receiver_id)
    sender = User.objects.get(id=sender_id)
    receiver = User.objects.get(id=receiver_id)

    try:
        conversation_id = Conversation.objects.get(
            Q(sender=sender_id, receiver=receiver_id) | Q(sender=receiver_id, receiver=sender_id))
    except Exception as e:
        conversation_id = Conversation.objects.create(sender=sender, receiver=receiver)

    chat_obj = ChatMessage.objects.create(sender=sender, receiver=receiver, message=message, 
                                            image=image, thumbnail_image=thumbnail_image, 
                                            message_type=message_type,conversation_id=conversation_id)

    conversation_id.is_check = True
    conversation_id.conversation_delete = "0"
    conversation_id.save()
    chat_data = ChatMessageSerializer(chat_obj)

    try:
        m1 = str(chat_obj.message)
        title=str(sender.first_name)+" sent you a message"
        fcmdevice = FCMDevice.objects.get(user=receiver)
        notification = messaging.Notification(
        title=title,
        body=m1,)
        k = messaging.Message(
            notification=notification,
            data={
                'data': str(chat_data.data),
                'title': title,
                'message': m1,
                'type': 'New_Message',
            },
            token=str(fcmdevice.registration_id))
        x = fcmdevice.send_message(k)
        print(x, "Send Message Fire")
        # Notifications.objects.create(user=receiver,
        #                              title=title,
        #                              message=m1, type="New_Message", sender_id=sender
        #                              )

    except Exception as e:
        print(str(e),"429999999999999999999999")
        print("wdqwdwqdqwdqwdqwdwq")

    sio.emit('send_message_response', {'data': chat_data.data},
             to=UserSession.objects.get(user__id=sender_id).session_id)

    sio.emit('send_message_reciver_response', {'data': chat_data.data},
             to=UserSession.objects.get(user__id=receiver_id).session_id)

    




@sio.on('block_user')
def block_user(sid, data):
    try:
        users = data['user']
        usr_obj = User.objects.get(id=users)
        #print(usr_obj, '=========================246')
    except:
        users = None
    try:
        is_block = data['is_block']
    except:
        is_block=None

    try:
        created_by = data['created_by']
        createdby_obj = User.objects.get(id=created_by)
        #print(createdby_obj, '=========================251')
    except:
        created_by = None

    try:

        data1={}
        data1['user']=users
        data1['is_block']=is_block
        data1['created_by']=created_by
        data1['checkblock']="False"
        data1['is_myside_block']="False"

        try:
            x = BlockUser.objects.get(user=createdby_obj, created_by=usr_obj, )
            print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',x)
            if x:
                data1['is_myside_block']="True"
        except Exception as e:
            print(str(e))
            pass

        # if not is_block:
        x = BlockUser.objects.get(user=usr_obj,
                                  created_by=createdby_obj, )
        sendsid=UserSession.objects.get(user=usr_obj).session_id
        x.delete()
        checkblock = "False"
        is_myside_block = "False"
        y = BlockUser.objects.filter(
            Q(created_by=createdby_obj, user=usr_obj) |
            Q(created_by=usr_obj, user=createdby_obj))

        if len(y) > 0:
            checkblock = "True"
            data1['is_block'] = "True"
            data['is_block']= "True"
        myblock = BlockUser.objects.filter(created_by=createdby_obj,
                                           user=usr_obj,
                                           block_user_id=created_by,
                                           block=True)
        if len(myblock) > 0:
            is_myside_block = "True"

        data['checkblock']=checkblock
        data['is_myside_block']=is_myside_block

        message = "user unblock successfully"
        sio.emit('block_user_response', {'data': data, 'message': message},
                 to=sid)
        sio.emit('block_user_response', {'data': data1, 'message': message},
                 to=sendsid)

        # if x.block == True:
        #     #if x.block = True:
        #     print(x,'===========if============260')
        #     x.block = False
        #     x.block_user_id = "0"
        #     x.save()
        #     message ="user unblock successfully"
        #     sio.emit('block_user_response', {'data':data,'message':message},
        #                 to=sid)
        # else:
        #     print('==================else===========268')
        #     x.block = True
        #     x.block_user_id = createdby_obj.id
        #     x.save()
        #     message ="user block successfully"
        #     sio.emit('block_user_response', {'data':data,'message':message},
        #                 to=sid)

    except:
        data1={}
        data1['user']=users
        data1['is_block']=is_block
        data1['created_by']=created_by
        data1['checkblock']="False"
        data1['is_myside_block']="False"

        try:
            x = BlockUser.objects.get(user=createdby_obj, created_by=usr_obj, )
            print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',x)
            if x:
                data1['is_myside_block']="True"
        except Exception as e:
            print(str(e))
            pass


        x = BlockUser.objects.create(user=usr_obj, created_by=createdby_obj, )
        sendsid=UserSession.objects.get(user=usr_obj).session_id
        x.block = is_block
        x.block_user_id = createdby_obj.id
        x.save()

        checkblock = "False"
        is_myside_block = "False"
        y = BlockUser.objects.filter(
            Q(created_by=createdby_obj, user=usr_obj) | Q(created_by=usr_obj,
                                                                         user=createdby_obj))

        if len(y) > 0:
            checkblock = "True"
        myblock = BlockUser.objects.filter(created_by=createdby_obj, user=usr_obj,
                                           block_user_id=created_by,
                                           block=True)
        if len(myblock) > 0:
            is_myside_block = "True"
    
        
        data['checkblock']=checkblock
        data['is_myside_block']=is_myside_block

        message = "user block successfully"
        sio.emit('block_user_response', {'data': data, 'message': message},
                 to=sid)
        sio.emit('block_user_response', {'data': data1, 'message': message},
                 to=sendsid)

# @sio.on('block_user')
# def block_user(sid, data):
#     try:
#         user = data['user']
#         usr_obj = User.objects.get(id=user)
#     except:
#         user = None
#     try:
#         is_block = data['is_block']
#     except:
#         is_block = None

#     try:
#         created_by = data['created_by']
#         createdby_obj = User.objects.get(id=created_by)
#         print(createdby_obj)
#     except:
#         created_by = None

#     try:
#         x = Block_User.objects.get(user=usr_obj, created_by=createdby_obj)
#         sendsid = UserSession.objects.get(user=usr_obj).session_id
#         x.delete()
#         checkblock = False
#         is_myside_block = False

#         block_user = Block_User.objects.filter(Q(created_by=createdby_obj, user=usr_obj) | Q(created_by=usr_obj, user=createdby_obj))

#         if len(block_user) > 0:
#             checkblock = True

#         myblock = Block_User.objects.filter(created_by=createdby_obj, user=usr_obj, block=True, block_user_id=created_by)
#         if len(myblock) > 0:
#             is_myside_block = True

#         data['checkblock'] = checkblock
#         data['is_myside_block'] = is_myside_block

#         message = "user unblock successfully"
#         sio.emit('block_user_response', {'data': data, 'message': message},
#                  to=sid)
#         sio.emit('block_user_response', {'data': data, 'message': message},
#                  to=sendsid)
#     except:
#         x = Block_User.objects.create(user=usr_obj, created_by=createdby_obj)
#         sendsid = UserSession.objects.get(user=usr_obj).session_id
#         x.block = is_block
#         block_user_id=createdby_obj,

#         x.save()
#         checkblock = False
#         is_myside_block = False

#         block_user = Block_User.objects.filter(
#             Q(created_by=createdby_obj, user=usr_obj) | Q(created_by=usr_obj, user=createdby_obj))

#         if len(block_user) > 0:
#             checkblock = True

#         myblock = Block_User.objects.filter(created_by=createdby_obj, user=usr_obj, block=True, block_user_id=created_by)
#         if len(myblock) > 0:
#             is_myside_block = True

#         data['checkblock'] = checkblock
#         data['is_myside_block'] = is_myside_block

#         message = "user block successfully"
#         sio.emit('block_user_response', {'data': data, 'message': message},
#                  to=sid)
#         sio.emit('block_user_response', {'data': data, 'message': message},
#                  to=sendsid)

@sio.on('chat_converstion')
def chat_history(sid, data):
    sender_id = data['sender_id']
    Chatconver_obj = Conversation.objects.filter(Q(sender=sender_id) | Q(receiver=sender_id)).exclude(
        conversation_delete=sender_id).exclude(conversation_delete='-1').order_by("-updated_at")

    chat_data = ChatconverstionSerializer(Chatconver_obj,context={"current_user": sender_id},many=True)
    sio.emit('chat_converstion_response', {'data':chat_data.data},
            to=sid)

@sio.on('chat_history')
def chat_history_event(sid, data):
    sender_id = data['sender_id']
    receiver_id = data['receiver_id']
    print('sender_id here', sender_id)
    print('receiver_id here', receiver_id)
    try:
        page = data['page']
    except:
        page = 0
    item_page = 20
    start_index = int(page) * item_page
    print('start_index', start_index)
    end_index = int(start_index) + item_page
    chat_obj = ChatMessage.objects.filter(Q(sender__id=sender_id, receiver__id=receiver_id)
                                          | Q(sender__id=receiver_id, receiver__id=sender_id)).order_by('-id')[start_index:end_index]
    checkdata = False
    if len(chat_obj) > 0:
        checkdata = "True"
    block = "False"
    is_myside_block = "False"
    y = BlockUser.objects.filter(Q(created_by__id=sender_id, user__id=receiver_id) | Q(created_by__id=receiver_id, user__id=sender_id))
    if len(y) > 0:
        block = "True"
    myblock = BlockUser.objects.filter(created_by__id=sender_id, user=receiver_id,block_user_id=sender_id,block=True)
    if len(myblock) > 0:
        is_myside_block = "True"

    chat_data = ChatMessageSerializer(chat_obj, many=True)
    context = {'is_block': block,
             'is_myside_block':is_myside_block,
             'checkdata': checkdata,
             'data': chat_data.data}

    sio.emit('chat_history_response', context, to=sid)

















@sio.event
def disconnect(sid):
     user = UserSession.objects.get(session_id=sid)
     user.is_online = False
     user.save()
     print('disconnect ', sid)
