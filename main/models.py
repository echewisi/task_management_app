from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
import datetime

class Profile(models.Model):
    account = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    tasks = models.ManyToManyField("Task", related_name="user_profiles", through="TaskOrder")

    def set_task_order(self, new_order):
        task_dict = {str(task.id): task for task in self.tasks.all()}

        new_task_order = []
        for task_id in new_order:
            if task_id in task_dict:
                new_task_order.append(task_dict[task_id])

        for idx, task in enumerate(new_task_order, start=1):
            taskorder, created = TaskOrder.objects.get_or_create(profile=self, task=task)
            taskorder.order = idx
            taskorder.save()

    def get_ordered_tasks(self):
        return self.tasks.order_by("taskorder__order")

    def __str__(self):
        return self.account.username


class TaskOrder(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    task = models.ForeignKey("Task", on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ("profile", "task")
        ordering = ("order",)


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
    if instance.reminder and instance.reminder <= timezone.now():
        subject = 'Task Reminder'
        message = f'Reminder for the task "{instance.title}"'
        recipient_list = [instance.created_by.email]
        send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)




