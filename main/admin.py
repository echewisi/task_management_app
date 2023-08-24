from django.contrib import admin
from .models import Profile, Task



admin.site.register(Profile)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display=[
        "title",
        "complete",
        "start_time",
        "finish_time"
        
    ]



# Register your models here.
