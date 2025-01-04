from django.shortcuts import render, redirect
from .models import Notification


def mark_all_as_read(request):
    notifications = Notification.objects.filter(recepient=request.user)
    notifications.update(is_read=True)
    return redirect(request.META.get('HTTP_REFERER', '/'))