from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from django.conf import settings

@shared_task
def send_reminder_email(task_id):
    from .models import Task
    try:
        task = Task.objects.get(id=task_id)
        if task.reminder and task.reminder <= timezone.now():
            subject = 'Task Reminder'
            message = f'Reminder for the task "{task.title}"'
            recipient_list = [task.created_by.email]
            send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)
    except Task.DoesNotExist:
        pass  # Task not found
