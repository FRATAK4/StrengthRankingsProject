from django.contrib import admin

from .models import Group, GroupAddRequest, GroupMembership

admin.site.register(Group)
admin.site.register(GroupAddRequest)
admin.site.register(GroupMembership)
