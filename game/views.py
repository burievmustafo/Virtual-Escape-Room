from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils import timezone
from django.db.models import Sum
from datetime import datetime
import json

from .models import Room, Puzzle, UserProgress, UserStatistics


def register_view(request):
    """Ro'yxatdan o'tish"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Statistikani yaratish
            UserStatistics.objects.create(user=user)
            username = form.cleaned_data.get('username')
            messages.success(request, f'Hisob yaratildi: {username}')
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'game/register.html', {'form': form})


def login_view(request):
    """Kirish"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Noto\'g\'ri foydalanuvchi nomi yoki parol')
    return render(request, 'game/login.html')


@login_required
def home_view(request):
    """Asosiy sahifa"""
    stats, created = UserStatistics.objects.get_or_create(user=request.user)
    stats.update_statistics()
    
    rooms = Room.objects.filter(is_active=True).order_by('order')
    progress_data = []
    
    for room in rooms:
        room_puzzles = room.puzzles.all()
        completed_count = UserProgress.objects.filter(
            user=request.user,
            puzzle__in=room_puzzles,
            is_completed=True
        ).count()
        total_count = room_puzzles.count()
        is_locked = False
        
        # Oldingi xona tugallanganligini tekshirish
        if room.order > 1:
            prev_room = Room.objects.filter(order=room.order - 1, is_active=True).first()
            if prev_room:
                prev_puzzles = prev_room.puzzles.all()
                prev_completed = UserProgress.objects.filter(
                    user=request.user,
                    puzzle__in=prev_puzzles,
                    is_completed=True
                ).count()
                if prev_completed < prev_puzzles.count():
                    is_locked = True
        
        progress_data.append({
            'room': room,
            'completed': completed_count,
            'total': total_count,
            'is_locked': is_locked,
            'progress_percent': int((completed_count / total_count * 100)) if total_count > 0 else 0
        })
    
    context = {
        'stats': stats,
        'rooms': progress_data,
    }
    return render(request, 'game/home.html', context)


@login_required
def room_view(request, room_id):
    """Xona sahifasi"""
    try:
        room = Room.objects.get(id=room_id, is_active=True)
    except Room.DoesNotExist:
        messages.error(request, 'Xona topilmadi')
        return redirect('home')
    
    # Xona ochiqligini tekshirish
    if room.order > 1:
        prev_room = Room.objects.filter(order=room.order - 1, is_active=True).first()
        if prev_room:
            prev_puzzles = prev_room.puzzles.all()
            prev_completed = UserProgress.objects.filter(
                user=request.user,
                puzzle__in=prev_puzzles,
                is_completed=True
            ).count()
            if prev_completed < prev_puzzles.count():
                messages.error(request, 'Avval oldingi xonani tugallang!')
                return redirect('home')
    
    puzzles = room.puzzles.all().order_by('order')
    puzzle_data = []
    
    for puzzle in puzzles:
        progress, created = UserProgress.objects.get_or_create(
            user=request.user,
            puzzle=puzzle,
            defaults={'room': puzzle.room, 'started_at': timezone.now()}
        )
        puzzle_data.append({
            'puzzle': puzzle,
            'progress': progress,
        })
    
    context = {
        'room': room,
        'puzzles': puzzle_data,
    }
    return render(request, 'game/room.html', context)


@login_required
def puzzle_view(request, puzzle_id):
    """Jumboq sahifasi"""
    try:
        puzzle = Puzzle.objects.get(id=puzzle_id)
    except Puzzle.DoesNotExist:
        messages.error(request, 'Jumboq topilmadi')
        return redirect('home')
    
    progress, created = UserProgress.objects.get_or_create(
        user=request.user,
        puzzle=puzzle,
        defaults={'room': puzzle.room, 'started_at': timezone.now()}
    )
    
    # Vaqtni hisoblash
    if created:
        start_time = timezone.now()
    else:
        start_time = progress.started_at
    
    # JavaScript uchun timestamp
    start_timestamp = int(start_time.timestamp()) if start_time else 0
    
    context = {
        'puzzle': puzzle,
        'progress': progress,
        'start_time': start_timestamp,
    }
    return render(request, 'game/puzzle.html', context)


@login_required
@require_http_methods(["POST"])
@ensure_csrf_cookie
def submit_answer(request, puzzle_id):
    """Javobni yuborish"""
    try:
        puzzle = Puzzle.objects.get(id=puzzle_id)
    except Puzzle.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Jumboq topilmadi'}, status=404)
    
    data = json.loads(request.body)
    user_answer = data.get('answer', '').strip().lower()
    time_taken = int(data.get('time_taken', 0))
    
    progress, created = UserProgress.objects.get_or_create(
        user=request.user,
        puzzle=puzzle,
        defaults={'room': puzzle.room, 'started_at': timezone.now()}
    )
    
    correct_answer = puzzle.correct_answer.strip().lower()
    is_correct = user_answer == correct_answer
    
    if not progress.is_completed:
        progress.attempts += 1
        
        if is_correct:
            progress.complete(time_taken)
            
            # Statistikani yangilash
            stats, _ = UserStatistics.objects.get_or_create(user=request.user)
            stats.update_statistics()
            
            # Keyingi jumboqni topish
            next_puzzle = Puzzle.objects.filter(
                room=puzzle.room,
                order__gt=puzzle.order
            ).order_by('order').first()
            
            # Agar xonadagi barcha jumboqlar tugallangan bo'lsa
            room_puzzles = puzzle.room.puzzles.all()
            completed_count = UserProgress.objects.filter(
                user=request.user,
                puzzle__in=room_puzzles,
                is_completed=True
            ).count()
            
            room_completed = completed_count == room_puzzles.count()
            
            # Keyingi xonani topish
            next_room = None
            if room_completed:
                next_room_obj = Room.objects.filter(
                    order__gt=puzzle.room.order,
                    is_active=True
                ).order_by('order').first()
                if next_room_obj:
                    next_room = {
                        'id': next_room_obj.id,
                        'title': next_room_obj.title,
                    }
            
            return JsonResponse({
                'success': True,
                'correct': True,
                'message': 'To\'g\'ri javob!',
                'score': progress.score,
                'next_puzzle_id': next_puzzle.id if next_puzzle else None,
                'room_completed': room_completed,
                'next_room': next_room,
            })
        else:
            progress.save()
            return JsonResponse({
                'success': True,
                'correct': False,
                'message': 'Noto\'g\'ri javob. Qayta urinib ko\'ring!',
                'attempts': progress.attempts,
            })
    else:
        return JsonResponse({
            'success': False,
            'message': 'Bu jumboq allaqachon tugallangan',
        })


@login_required
def statistics_view(request):
    """Statistika sahifasi"""
    stats, created = UserStatistics.objects.get_or_create(user=request.user)
    stats.update_statistics()
    
    # Batafsil statistika
    all_progress = UserProgress.objects.filter(user=request.user).order_by('-completed_at')
    completed_progress = all_progress.filter(is_completed=True)
    
    # Xonalar bo'yicha statistika
    room_stats = []
    rooms = Room.objects.filter(is_active=True).order_by('order')
    for room in rooms:
        room_puzzles = room.puzzles.all()
        completed = UserProgress.objects.filter(
            user=request.user,
            puzzle__in=room_puzzles,
            is_completed=True
        )
        room_score = completed.aggregate(total=Sum('score'))['total'] or 0
        room_time = completed.aggregate(total=Sum('time_taken'))['total'] or 0
        
        room_stats.append({
            'room': room,
            'completed': completed.count(),
            'total': room_puzzles.count(),
            'score': room_score,
            'time': room_time,
        })
    
    context = {
        'stats': stats,
        'completed_progress': completed_progress[:20],  # Oxirgi 20 ta
        'room_stats': room_stats,
    }
    return render(request, 'game/statistics.html', context)

