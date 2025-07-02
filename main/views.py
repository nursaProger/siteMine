from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import RegisterForm, LoginForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Message
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime, timedelta
import random

def home(request):
    server_data = {
        'ip': 'asphaltcraft.okak.skin',
        'version': '1.21.4',
    }
    return render(request, 'home.html', {'server': server_data})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                # Добавляем ошибку в контекст
                return render(request, 'login.html', {'form': {'errors': True}})
    return render(request, 'login.html', {'form': {}})

def user_logout(request):
    logout(request)
    return redirect('home')

def rules(request):
    rules_list = [
        {
            'title': 'Общие правила',
            'rules': [
                'Уважайте других игроков',
                'Не используйте читы и модификации',
                'Не спамьте в чате',
                'Не разрушайте чужие постройки',
                'Следуйте указаниям администрации'
            ]
        },
        {
            'title': 'Правила чата',
            'rules': [
                'Не используйте нецензурную лексику',
                'Не оскорбляйте других игроков',
                'Не рекламируйте другие серверы',
                'Используйте русский язык в общем чате'
            ]
        },
        {
            'title': 'Правила строительства',
            'rules': [
                'Не стройте неприличные сооружения',
                'Соблюдайте архитектурный стиль',
                'Не загораживайте проходы',
                'Используйте только разрешенные блоки'
            ]
        }
    ]
    return render(request, 'rules.html', {'rules': rules_list})

def stats(request):
    # Симуляция статистики
    stats_data = {
        'total_players': 1250,
        'online_now': random.randint(15, 45),
        'peak_today': 67,
        'total_playtime': '1,234,567 часов',
        'top_players': [
            {'name': 'Player1', 'playtime': '1,234 ч', 'level': 85},
            {'name': 'Player2', 'playtime': '987 ч', 'level': 72},
            {'name': 'Player3', 'playtime': '756 ч', 'level': 68},
            {'name': 'Player4', 'playtime': '654 ч', 'level': 61},
            {'name': 'Player5', 'playtime': '543 ч', 'level': 58},
        ],
        'server_stats': {
            'total_blocks_placed': '15,678,901',
            'total_mobs_killed': '2,345,678',
            'total_deaths': '89,123',
            'total_items_crafted': '456,789'
        }
    }
    return render(request, 'stats.html', {'stats': stats_data})

@login_required
def chat(request):
    messages = Message.objects.select_related('user').order_by('-created_at')[:50][::-1]
    return render(request, 'chat.html', {'messages': messages})

@csrf_exempt
def send_message(request):
    if request.method == 'POST':
        text = request.POST.get('text', '').strip()
        if text and request.user.is_authenticated:
            Message.objects.create(user=request.user, text=text)
            return JsonResponse({'success': True})
    return JsonResponse({'success': False})

def get_messages(request):
    messages = Message.objects.select_related('user').order_by('-created_at')[:50][::-1]
    message_list = []
    for m in messages:
        message_list.append({
            'user': m.user.username,
            'created_at': m.created_at.strftime('%H:%M:%S'),
            'text': m.text,
        })
    return JsonResponse({'messages': message_list})

def server_info(request):
    # Симуляция данных сервера
    server_data = {
        'name': 'Minecraft Server',
        'version': '1.21.4',
        'ip': 'asphaltcraft.okak.skin',
        'port': 25565,
        'max_players': 100,
        'online_players': random.randint(15, 45),
        'uptime': '99.8%',
        'tps': '20.0',
        'world_size': '2.5 GB',
        'plugins': [
            'EssentialsX',
            'WorldEdit',
            'WorldGuard',
            'LuckPerms',
            'CoreProtect'
        ]
    }
    return render(request, 'server_info.html', {'server': server_data})

def donations(request):
    donation_packages = [
        {
            'name': 'VIP',
            'price': 500,
            'currency': '₸',
            'features': [
                'Префикс [VIP]',
                'Доступ к /kit vip',
                'Возможность летать',
                'Больше слотов в инвентаре'
            ]
        },
        {
            'name': 'Premium',
            'price': 1000,
            'currency': '₸',
            'features': [
                'Все возможности VIP',
                'Префикс [Premium]',
                'Доступ к /kit premium',
                'Возможность телепортации',
                'Приоритетный вход на сервер'
            ]
        },
        {
            'name': 'Legend',
            'price': 2000,
            'currency': '₸',
            'features': [
                'Все возможности Premium',
                'Префикс [Legend]',
                'Доступ к /kit legend',
                'Возможность создавать варпы',
                'Доступ к командам модератора'
            ]
        }
    ]
    return render(request, 'donations.html', {'packages': donation_packages})

def gallery(request):
    # Симуляция галереи скриншотов
    gallery_data = {
        'categories': [
            {
                'name': 'Постройки игроков',
                'images': [
                    {'title': 'Средневековый замок', 'author': 'Player1', 'likes': 45, 'image': 'https://via.placeholder.com/300x200/00d4ff/ffffff?text=Castle'},
                    {'title': 'Современный город', 'author': 'Player2', 'likes': 32, 'image': 'https://via.placeholder.com/300x200/ff006e/ffffff?text=City'},
                    {'title': 'Футуристическая база', 'author': 'Player3', 'likes': 28, 'image': 'https://via.placeholder.com/300x200/ffd700/000000?text=Base'},
                ]
            },
            {
                'name': 'Ландшафт',
                'images': [
                    {'title': 'Горный пейзаж', 'author': 'Player4', 'likes': 38, 'image': 'https://via.placeholder.com/300x200/00ff88/000000?text=Mountains'},
                    {'title': 'Океанский вид', 'author': 'Player5', 'likes': 25, 'image': 'https://via.placeholder.com/300x200/ffaa00/000000?text=Ocean'},
                ]
            },
            {
                'name': 'События',
                'images': [
                    {'title': 'Турнир PvP', 'author': 'Admin', 'likes': 67, 'image': 'https://via.placeholder.com/300x200/ff4444/ffffff?text=PvP'},
                    {'title': 'Конкурс строительства', 'author': 'Admin', 'likes': 89, 'image': 'https://via.placeholder.com/300x200/9932cc/ffffff?text=Contest'},
                ]
            }
        ]
    }
    return render(request, 'gallery.html', {'gallery': gallery_data})

def forum(request):
    # Симуляция форума
    forum_data = {
        'categories': [
            {
                'name': 'Общие обсуждения',
                'description': 'Общие темы и обсуждения сервера',
                'topics': 45,
                'posts': 234
            },
            {
                'name': 'Техническая поддержка',
                'description': 'Помощь с игрой и технические вопросы',
                'topics': 23,
                'posts': 156
            },
            {
                'name': 'Предложения',
                'description': 'Предложения по улучшению сервера',
                'topics': 12,
                'posts': 89
            },
            {
                'name': 'Новости',
                'description': 'Обновления и новости сервера',
                'topics': 8,
                'posts': 67
            }
        ],
        'recent_topics': [
            {'title': 'Новый плагин экономики', 'author': 'Admin', 'replies': 15, 'views': 234},
            {'title': 'Проблемы с подключением', 'author': 'Player1', 'replies': 8, 'views': 156},
            {'title': 'Идеи для новых событий', 'author': 'Player2', 'replies': 23, 'views': 445},
        ]
    }
    return render(request, 'forum.html', {'forum': forum_data})

@login_required
def profile(request):
    # Симуляция профиля пользователя
    profile_data = {
        'user': request.user,
        'stats': {
            'join_date': '2024-01-15',
            'total_playtime': '156 часов',
            'blocks_placed': '45,678',
            'mobs_killed': '12,345',
            'deaths': '89',
            'achievements': 15
        },
        'achievements': [
            {'name': 'Первые шаги', 'description': 'Проведите 1 час на сервере', 'earned': True},
            {'name': 'Строитель', 'description': 'Разместите 1000 блоков', 'earned': True},
            {'name': 'Исследователь', 'description': 'Посетите 10 разных биомов', 'earned': False},
            {'name': 'Выживший', 'description': 'Проживите 7 дней без смерти', 'earned': True},
        ],
        'recent_activity': [
            {'action': 'Подключился к серверу', 'time': '2 часа назад'},
            {'action': 'Разместил 50 блоков', 'time': '3 часа назад'},
            {'action': 'Убил 10 зомби', 'time': '5 часов назад'},
        ]
    }
    return render(request, 'profile.html', {'profile': profile_data})

def leaderboard(request):
    # Симуляция таблицы лидеров
    leaderboard_data = {
        'categories': [
            {
                'name': 'Время игры',
                'players': [
                    {'rank': 1, 'name': 'AquaHM', 'value': '2,000 ч', 'level': 99},
                    {'rank': 2, 'name': 'Player1', 'value': '1,234 ч', 'level': 85},
                    {'rank': 3, 'name': 'Player2', 'value': '987 ч', 'level': 72},
                ]
            },
            {
                'name': 'Блоки размещено',
                'players': [
                    {'rank': 1, 'name': 'AquaHM', 'value': '3,000,000', 'level': 99},
                    {'rank': 2, 'name': 'Builder1', 'value': '2,345,678', 'level': 92},
                    {'rank': 3, 'name': 'Builder2', 'value': '1,987,654', 'level': 78},
                ]
            },
            {
                'name': 'Мобы убито',
                'players': [
                    {'rank': 1, 'name': 'AquaHM', 'value': '100,000', 'level': 99},
                    {'rank': 2, 'name': 'Hunter1', 'value': '45,678', 'level': 88},
                    {'rank': 3, 'name': 'Hunter2', 'value': '34,567', 'level': 75},
                ]
            }
        ]
    }
    return render(request, 'leaderboard.html', {'leaderboard': leaderboard_data}) 