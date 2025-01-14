from django.urls import path
from . import views


app_name = 'articles'

urlpatterns = [
    path('rate/<int:pk>/<int:star>', views.rate_article, name='rate_article'),
    path('create/', views.create_article, name='create_article'),
    path('delete/<int:pk>', views.delete_article, name='delete_article'),
    path('<int:pk>/', views.DetailArticle.as_view(), name='detail_article'),
    path('comment/create/<int:article>', views.create_comment, name='create_comment'),
    path('write/', views.write_page, name='write')
]
