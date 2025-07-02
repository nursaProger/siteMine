from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('chat/', views.chat, name='chat'),
    path('chat/send/', views.send_message, name='chat_send'),
    path('chat/messages/', views.get_messages, name='chat_messages'),
    path('send_message/', views.send_message, name='send_message'),
    path('get_messages/', views.get_messages, name='get_messages'),
    path('server/', views.server_info, name='server_info'),
    path('rules/', views.rules, name='rules'),
    path('stats/', views.stats, name='stats'),
    path('donations/', views.donations, name='donations'),
    path('gallery/', views.gallery, name='gallery'),
    path('forum/', views.forum, name='forum'),
    path('profile/', views.profile, name='profile'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('button-demo/', TemplateView.as_view(template_name='button_demo.html'), name='button_demo'),
] 