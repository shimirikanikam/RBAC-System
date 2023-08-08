from django.contrib import admin
from .models import CustomUser,store_user_token
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(store_user_token)