from django.shortcuts import render
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import redirect
from .forms import RegisterForm, LoginForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Message
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'home.html')

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
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')

def rules(request):
    return render(request, 'rules.html')

def stats(request):
    return render(request, 'stats.html')

@login_required
def chat(request):
    messages = Message.objects.select_related('user').order_by('-created_at')[:50][::-1]
    return render(request, 'chat.html', {'messages': messages})

@login_required
@require_POST
def send_message(request):
    text = request.POST.get('text', '').strip()
    if text:
        Message.objects.create(user=request.user, text=text)
    return JsonResponse({'success': True})

@login_required
def get_messages(request):
    messages = Message.objects.select_related('user').order_by('-created_at')[:50][::-1]
    data = [
        {
            'user': m.user.username,
            'text': m.text,
            'created_at': m.created_at.strftime('%H:%M:%S')
        } for m in messages
    ]
    return JsonResponse({'messages': data})

def donate(request):
    return render(request, 'donate.html') 