from django.contrib import admin
from .models import Post, UserNetwork, User
# Register your models here.

admin.site.register(Post)
admin.site.register(UserNetwork)
admin.site.register(User)