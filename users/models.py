from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.timezone import now
from django.contrib.auth.models import Permission


class User(AbstractUser):
    photo = models.ImageField(upload_to='images/user', default='images/user/default.jpg', blank=True, null=True, verbose_name='Фото')
    rating = models.DecimalField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(5.0)], max_digits=5, decimal_places=1)
    last_seen = models.DateTimeField(null=True, blank=True)

    class Meta:
        permissions = [
            ('ai_write', 'Access to ai write'),
        ]

    def has_access_to_ai_write(self):
        if self.articles.count() > 10 and self.rating >= 4.0:
            return True
        return False

    def update_rating(self):
        total_rating = sum(a.rating for a in self.articles.all())
        if self.articles.count() < 2:
            self.rating = total_rating
        else:
            self.rating = total_rating / self.articles.count()
        self.save()

        if self.has_access_to_ai_write():
            self.user_permissions.add(Permission.objects.get(codename='ai_write'))
        else:
            self.user_permissions.remove(Permission.objects.get(codename='ai_write'))

    def last_activity(self):
        seconds = (now() - self.last_seen).total_seconds()
        if seconds / 60 <= 1:
            return 'online'

        minutes = (now() - self.last_seen).total_seconds() / 60
        hours = int(minutes / 60)
        years = now().date().year - self.last_seen.year
        if minutes < 60:
            return f'{int(minutes)} минут назад'
        elif hours <= 24:
            if hours in (1, 21):
                return f'{int(hours)} час назад'
            elif hours in (2,3,4,22,23,24):
                return f'{int(hours)} часа назад'
            else:
                return f'{int(hours)} часов назад'
        elif years >= 1:
            return 'Давно'
        else:
            return self.last_seen.strftime("%d.%m")

    def is_subscribed(self, other_user):
        return self.subscribers.filter(subscribed_to=other_user).exists()


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscribers')
    subscribed_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    
    class Meta:
        unique_together = ('user', 'subscribed_to')
        
    def __str__(self):
        return f'{self.user} подписан на {self.subscribed_to}'