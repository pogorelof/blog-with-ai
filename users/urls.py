from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView


app_name = 'users'
urlpatterns = [
    path('login/', views.LoginUser.as_view(), name='login'),
    path('register/',views.RegisterUser.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/<int:pk>/', views.Profile.as_view(), name='profile'),
    path('search/', views.search_user, name='search'),
    path('subscribe/<int:pk>', views.subscribe, name='subscribe'),
    path('unsubscribe/<int:pk>', views.unsubscribe, name='unsubscribe'),
    path('subscriptions/', views.Subscriptions.as_view(), name='subscriptions'),
    path('edit/', views.Edit.as_view(), name='edit'),
    path('change_photo/', views.change_photo, name='change_photo'),
    path('change_password', views.change_password, name='change_password'),
]
