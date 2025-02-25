from django.contrib import admin
from .models import CustomUser, Interest, UserGroup, GroupUser, Message, Event

admin.site.register(CustomUser)
admin.site.register(Interest)
admin.site.register(UserGroup)
admin.site.register(GroupUser)
admin.site.register(Message)
admin.site.register(Event)
