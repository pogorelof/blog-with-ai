from . models import Notification


def notifications(request):
    context = {
        'notifications': [],
        'is_new': False
    }

    if request.user.is_authenticated:
        # Old notifications no longer important, but their large number can load database. Thst's why limit[:20]
        n = Notification.objects.filter(recepient=request.user)[:20]
        # Instead of n.filter(is_read=True).exists() because it makes new sql query
        context['is_new'] = any(not noty.is_read for noty in n)
        context['notifications'] = n
        
    return context