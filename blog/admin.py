from django.contrib import admin
from django.contrib.auth.models import User
from .models import Blog,Code, CustomUser
# Register your models here.

class User(admin.ModelAdmin):
    list_display=('is_active')

admin.site.register(Blog)
admin.site.register(Code)
admin.site.register(CustomUser)
