from django.contrib import admin
from .models import Article, UsersRating, Comment


admin.site.register(Article)
admin.site.register(UsersRating)
admin.site.register(Comment)