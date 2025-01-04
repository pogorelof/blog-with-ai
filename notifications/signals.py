from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from articles.models import UsersRating
from users.models import Subscription
from .models import ArticleNotification, UserNotification


@receiver(post_save, sender=UsersRating)
def create_rating_notification(sender, instance, created, **kwargs):
    if created:
        rate = instance.rate
        user = instance.user
        article = instance.article

        if article.author != user:
            message = f'{user} поставил {rate} звёзд вашему сообщению {article.body[:20]}'
            ArticleNotification.objects.create(
                recepient=article.author,
                article=article,
                message=message
            )


@receiver(post_delete, sender=UsersRating)
def delete_rating_notification(sender, instance, **kwargs):
    article = instance.article
    user = article.author

    notification = ArticleNotification.objects.filter(recepient=user,article=article)
    if notification:
        notification.delete()

@receiver(post_save, sender=Subscription)
def create_subscription_notification(sender, instance, created, **kwargs):
    if created:
        message = f'{instance.user} подписался на вас'
        UserNotification.objects.create(
            recepient=instance.subscribed_to,
            user=instance.user,
            message=message
        )

@receiver(post_delete, sender=Subscription)
def delete_subscription_notification(sender, instance, **kwargs):
    notification = UserNotification.objects.filter(recepient=instance.subscribed_to, user=instance.user)
    if notification:
        notification.delete()
