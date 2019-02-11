from django.contrib import admin

from .models import User
from .models import Position

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
	list_display =['name','username','sex','age']

@admin.register(Position)
class UserAdmin(admin.ModelAdmin):
	list_display =['job_title','description','start_date','end_date', 'user']