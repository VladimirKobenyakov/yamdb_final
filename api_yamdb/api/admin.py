from django.contrib import admin

from user.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('role',)


admin.site.register(User, UserAdmin)
