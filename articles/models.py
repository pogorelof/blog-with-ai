from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import get_user_model


class Article(models.Model):
    body = models.TextField()
    photo = models.ImageField(upload_to='images/article', blank=True, null=True, verbose_name='Фото')
    rating = models.DecimalField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(5.0)], max_digits=5, decimal_places=1)
    upload_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='articles')
    
    class Meta:
        ordering = ['-upload_at']
    
    def update_rating(self):
        ratings = UsersRating.objects.filter(article=self)
        
        if ratings.exists():
            total_rating = sum(rating.rate for rating in ratings)
            self.rating = total_rating / ratings.count()
        else:
            self.rating = 0.0
        
        self.save()

class UsersRating(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    rate = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    
    class Meta:
        unique_together = ('user', 'article')
        
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.article.update_rating()
        
    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.article.update_rating()
        
class Comment(models.Model):
    body = models.TextField()
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='comments')
    upload_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-upload_at']
    
    def __str__(self):
        return self.body