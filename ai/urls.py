from django.urls import path
from . import views


app_name = 'ai'

urlpatterns = [
    path('sumarize-subscriptions/', views.summarize_subscriptions, name='sum_subs'),
]
