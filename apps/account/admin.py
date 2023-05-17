from django.contrib import admin
from django.contrib.auth.models import Group, User


admin.site.unregister(Group)
admin.site.unregister(User)

from apps.account.components.users import UserAdmin

admin.site.site_header = "Admininstración | API de usuarios"
