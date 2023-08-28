from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings

class Profile(models.Model):
    account = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank= True)
    tasks = models.ForeignKey("Task", on_delete=models.CASCADE, related_name="user_tasks", null=True, blank=True)

    def __str__(self):
        return self.account.username
    


class Task(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="created_tasks")
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    reminder = models.DateTimeField(null=True, blank=True)
    start_time = models.DateTimeField(auto_now_add=True)
    finish_time = models.DateTimeField(null=True, blank=True)

    def mark_as_complete(self):
        self.complete = True
        self.finish_time = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-complete"]

@receiver(post_save, sender=Task)
def task_created(sender, instance, created, **kwargs):
    if created:
        instance.start_time = timezone.now()
        instance.save()
        # Send an email when a new task is created
        subject = 'New Task Created'
        message = f'A new task "{instance.title}" has been created at {instance.start_time}'
        recipient_list = [instance.created_by.email]
        send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)

@receiver(post_save, sender=Task)        
def task_completed(sender, instance, **kwargs):
    if instance.complete and not instance.finish_time:
        # Task has been completed
        instance.finish_time = timezone.now()
        instance.save()

        # Send an email when a task is completed
        subject = 'Task Completed'
        message = f'The task "{instance.title}" has been completed at {instance.finish_time}'
        recipient_list = [instance.created_by.email]
        send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)

@receiver(pre_delete, sender=Task)
def task_deleted(sender, instance, **kwargs):
    subject = 'Task Deleted'
    message = f'The task "{instance.title}" has been deleted.'
    recipient_list = [instance.created_by.email]
    send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)

@receiver(post_save, sender=Task)
def send_reminder_email(sender, instance, **kwargs):
    if instance.reminder and instance.reminder == timezone.now():
        subject = 'Task Reminder'
        message = f'Reminder for the task "{instance.title}"'
        recipient_list = [instance.created_by.email]
        send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(account=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

