from django.contrib import admin
from .models import Blog,Code, CustomUser
# Register your models here.

admin.site.register(Blog)
admin.site.register(Code)
admin.site.register(CustomUser)
