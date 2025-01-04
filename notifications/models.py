from django.db import models
from users.models import User
from articles.models import Article


class Notification(models.Model):
    recepient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.message

class ArticleNotification(Notification):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

class UserNotification(Notification):
    user = models.ForeignKey(User, on_delete=models.CASCADE)