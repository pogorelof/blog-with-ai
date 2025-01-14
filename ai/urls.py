from django.urls import path
from . import views


app_name = 'ai'

urlpatterns = [
    path('sumarize-subscriptions/', views.summarize_subscriptions, name='sum_subs'),
    path('make-plan/', views.tweet_plan, name='make_plan'),
    path('make-text/', views.make_text, name='make_text'),
    path('make-opinion/', views.opinion, name='make_opinion'),
]
