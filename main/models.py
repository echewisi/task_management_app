from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Profile(models.Model):
    account= models.ForeignKey(User, on_delete= models.CASCADE)
    tasks= models.ForeignKey("Task", on_delete= models.CASCADE, related_name= "user_tasks")
    
    def __str__(self):
        return self.account.username

class Task(models.Model):
    title= models.CharField(max_length= 255)
    description= models.TextField(null= True, blank= True)
    complete= models.BooleanField(default= False)
    reminder= models.DateTimeField(null= True, blank= True)
    start_time= models.DateTimeField(auto_now_add= True)
    finish_time= models.DateTimeField(null= True, blank=True)
    
    def mark_as_complete(self):
        self.complete = True
        self.finish_time = timezone.now()  
        self.save()

    def __str__(self):
        return self.title
    
    class Meta:
        ordering=["complete"]



# Create your models here.
