from django.contrib import admin
from SNApp.models import *

admin.site.register(User)
admin.site.register(Post)
admin.site.register(Follow)
admin.site.register(UserPostRelation)