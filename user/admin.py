from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(User)
admin.site.register(Notifications)
admin.site.register(UserSession)
admin.site.register(Conversation)
admin.site.register(ChatMessage)
admin.site.register(BlockUser)
admin.site.register(VersionControl)



