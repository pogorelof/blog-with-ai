from django.contrib import admin
from .models import User, Subscription
from django.contrib.auth.admin import UserAdmin


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'photo', 'rating', 'last_seen')  # поля, которые будут отображаться в списке пользователей

admin.site.register(User, UserAdmin)
admin.site.register(Subscription)