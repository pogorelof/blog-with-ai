from django.urls import path
from . import views


app_name = "notifications"
urlpatterns = [
    path('mark_as_read/', views.mark_all_as_read, name='mark_as_read'),
]