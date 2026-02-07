from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils import timezone, translation
from django.db.models import Sum, Q, Count, Avg
import re
from django.contrib.auth.models import User
from datetime import timedelta
import math
import json

from .models import Room, Puzzle, UserProgress, UserStatistics


def get_user_badges(user):
    """Foydalanuvchi yutuqlarini hisoblash"""
    stats, _ = UserStatistics.objects.get_or_create(user=user)
    completed = UserProgress.objects.filter(user=user, is_completed=True)
    fastest = completed.order_by('time_taken').first()
    total_completed = completed.count()
    total_time = completed.aggregate(total=Sum('time_taken'))['total'] or 0
    lang = translation.get_language() or 'uz'

    def t(uz, en, ja):
        return {'uz': uz, 'en': en, 'ja': ja}.get(lang, uz)

    badges = []

    if total_completed >= 1:
        badges.append({
            'icon': '🧩',
            'title': t('Boshlovchi', 'Beginner', '初心者'),
            'desc': t("Birinchi jumboqni yechdingiz", 'Solved your first puzzle', '最初のパズルを解いた'),
            'tone': 'primary',
        })

    if fastest and fastest.time_taken <= 30:
        badges.append({
            'icon': '⚡',
            'title': t('Tezkor', 'Speedster', 'スピードスター'),
            'desc': t('30 soniyadan kam vaqtda yechildi', 'Solved under 30 seconds', '30秒以内に解決'),
            'tone': 'accent',
        })

    if stats.rooms_completed >= 2:
        badges.append({
            'icon': '🗺️',
            'title': t('Tadqiqotchi', 'Explorer', '探検家'),
            'desc': t('Kamida 2 ta xona tugallandi', 'Completed at least 2 rooms', '2つ以上の部屋を完了'),
            'tone': 'success',
        })

    if stats.total_score >= 200:
        badges.append({
            'icon': '🏆',
            'title': t('Ustoz', 'Master', 'マスター'),
            'desc': t('200+ ball yig\'dingiz', 'Scored 200+ points', '200点以上を獲得'),
            'tone': 'gold',
        })

    if total_time >= 600:
        badges.append({
            'icon': '⏱️',
            'title': t('Marafon', 'Marathon', 'マラソン'),
            'desc': t('10+ daqiqa o\'ynadingiz', 'Played for 10+ minutes', '10分以上プレイ'),
            'tone': 'neutral',
        })

    return badges


def get_daily_puzzle(user):
    """Kunlik jumboqni aniqlash (deterministik)"""
    puzzles = list(Puzzle.objects.all().order_by('id'))
    if not puzzles:
        return None, False
    today_index = timezone.localdate().toordinal() % len(puzzles)
    puzzle = puzzles[today_index]
    completed = UserProgress.objects.filter(user=user, puzzle=puzzle, is_completed=True).exists()
    return puzzle, completed


def normalize_answer(value):
    return re.sub(r"\s+", " ", value.strip().lower())


def get_correct_answers(puzzle, lang_code):
    lang = (lang_code or 'uz').split('-')[0]
    localized_field = f'correct_answer_{lang}'
    localized_value = ''
    if hasattr(puzzle, localized_field):
        localized_value = getattr(puzzle, localized_field) or ''

    source_value = localized_value if localized_value.strip() else (puzzle.correct_answer or '')
    parts = re.split(r"[,\n;|]+", source_value)
    return {normalize_answer(p) for p in parts if p.strip()}


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
    
    daily_puzzle, daily_completed = get_daily_puzzle(request.user)
    leaderboard = UserStatistics.objects.select_related('user').order_by(
        '-total_score', 'total_time', 'user__username'
    )[:10]
    higher_rank_count = UserStatistics.objects.filter(
        Q(total_score__gt=stats.total_score) |
        Q(total_score=stats.total_score, total_time__lt=stats.total_time) |
        Q(total_score=stats.total_score, total_time=stats.total_time, user__username__lt=request.user.username)
    ).count()

    context = {
        'stats': stats,
        'rooms': progress_data,
        'badges': get_user_badges(request.user),
        'daily_puzzle': daily_puzzle,
        'daily_completed': daily_completed,
        'leaderboard': leaderboard,
        'current_rank': higher_rank_count + 1,
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
    
    # Vaqtni hisoblash - har safar yangi jumboqqa kirganda vaqt qaytadan boshlanadi
    if progress.is_completed:
        # Tugallangan jumboq uchun eski vaqtni ko'rsatish
        start_time = progress.started_at
    else:
        # Tugallanmagan jumboq uchun vaqtni qaytadan boshlash
        start_time = timezone.now()
        progress.started_at = start_time
        progress.save()
    
    # JavaScript uchun timestamp
    start_timestamp = int(start_time.timestamp()) if start_time else 0
    
    stats, _ = UserStatistics.objects.get_or_create(user=request.user)
    stats.ensure_hint_tokens()

    context = {
        'puzzle': puzzle,
        'progress': progress,
        'start_time': start_timestamp,
        'hint_tokens': stats.hint_tokens,
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
    
    lang_code = translation.get_language() or 'uz'
    correct_answers = get_correct_answers(puzzle, lang_code)
    is_correct = normalize_answer(user_answer) in correct_answers
    
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
def dashboard_view(request):
    """Dashboard - barcha o'yinchilar statistikasi"""
    # Barcha o'yinchilar ro'yxati
    all_users = User.objects.all().order_by('-date_joined')
    
    # Barcha o'yinchilar statistikasi
    user_stats = []
    for user in all_users:
        stats, _ = UserStatistics.objects.get_or_create(user=user)
        completed = UserProgress.objects.filter(user=user, is_completed=True)
        user_stats.append({
            'user': user,
            'stats': stats,
            'completed_count': completed.count(),
            'avg_time': completed.aggregate(avg=Avg('time_taken'))['avg'] or 0,
        })
    
    # Top o'yinchilar
    top_players = sorted(user_stats, key=lambda x: x['stats'].total_score, reverse=True)[:5]
    max_top_score = max((item['stats'].total_score for item in top_players), default=0)
    for item in top_players:
        item['progress_percent'] = int((item['stats'].total_score / max_top_score) * 100) if max_top_score > 0 else 5
    
    # Umumiy statistika
    total_stats = {
        'total_users': User.objects.count(),
        'total_rooms': Room.objects.filter(is_active=True).count(),
        'total_puzzles': Puzzle.objects.count(),
        'total_completed': UserProgress.objects.filter(is_completed=True).count(),
    }
    
    # Xonalar statistikasi
    rooms = Room.objects.filter(is_active=True).order_by('order')
    room_stats = []
    for room in rooms:
        completed_progress = UserProgress.objects.filter(
            room=room,
            is_completed=True
        )
        total_puzzles = room.puzzles.count()
        room_stats.append({
            'room': room,
            'completed': completed_progress.count(),
            'total': total_puzzles,
            'score': completed_progress.aggregate(total=Sum('score'))['total'] or 0,
            'time': completed_progress.aggregate(total=Sum('time_taken'))['total'] or 0,
            'progress_percent': int((completed_progress.count() / total_puzzles) * 100) if total_puzzles > 0 else 0,
        })
    
    # So'nggi faoliyat
    recent_activities = UserProgress.objects.filter(
        is_completed=True
    ).select_related('user', 'puzzle', 'room').order_by('-completed_at')[:10]

    def build_line_series(items, width=320, height=130, padding=22):
        raw_max = max((item['count'] for item in items), default=0) or 1
        nice_max = max(400, int(math.ceil(raw_max / 100.0) * 100))
        step = (width - padding * 2) / (len(items) - 1) if len(items) > 1 else 0
        points = []
        for index, item in enumerate(items):
            x = padding + (index * step)
            y = (height - padding) - ((item['count'] / nice_max) * (height - padding * 2))
            points.append({'x': round(x, 1), 'y': round(y, 1), 'label': item['label']})
        points_str = " ".join([f"{p['x']},{p['y']}" for p in points])
        baseline_y = height - padding
        area_points = [f"{points[0]['x']},{baseline_y}"] + points_str.split() + [f"{points[-1]['x']},{baseline_y}"]
        area_points_str = " ".join(area_points)
        tick_values = [
            int(nice_max * 0.33),
            int(nice_max * 0.66),
            nice_max,
        ]
        ticks = []
        for value in tick_values:
            y = (height - padding) - ((value / nice_max) * (height - padding * 2))
            ticks.append({'value': value, 'y': round(y, 1)})
        return {
            'points': points,
            'points_str': points_str,
            'area_points_str': area_points_str,
            'ticks': ticks,
        }

    def build_bar_series(items, width=320, height=130, padding=24):
        raw_max = max((item['count'] for item in items), default=0) or 1
        nice_max = max(60, int(math.ceil(raw_max / 10.0) * 10))
        inner_width = width - padding * 2
        count = len(items)
        if count == 0:
            ticks = []
            for value in [nice_max, int(nice_max * 2 / 3), int(nice_max / 3), 0]:
                y = (height - padding) - ((value / nice_max) * (height - padding * 2))
                ticks.append({'value': value, 'y': round(y, 1)})
            return {
                'bars': [],
                'ticks': ticks,
            }
        gap = inner_width / count
        bar_width = min(10, gap * 0.4)
        bars = []
        for index, item in enumerate(items):
            x = padding + (index * gap) + (gap - bar_width) / 2
            bar_height = ((item['count'] / nice_max) * (height - padding * 2))
            y = (height - padding) - bar_height
            bars.append({
                'x': round(x, 1),
                'y': round(y, 1),
                'height': round(bar_height, 1),
                'label': item['label'],
                'count': item['count'],
            })
        ticks = []
        for value in [nice_max, int(nice_max * 2 / 3), int(nice_max / 3), 0]:
            y = (height - padding) - ((value / nice_max) * (height - padding * 2))
            ticks.append({'value': value, 'y': round(y, 1)})
        return {
            'bars': bars,
            'ticks': ticks,
        }

    # Haftalik faoliyat (so'nggi 7 kun)
    today = timezone.localdate()
    weekly_days = [today - timedelta(days=offset) for offset in range(6, -1, -1)]
    weekly_counts = []
    
    # Tilga qarab kun nomlarini olish
    lang = translation.get_language() or 'uz'
    days_map = {
        'uz': ['Du', 'Se', 'Ch', 'Pa', 'Ju', 'Sh', 'Ya'],
        'en': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        'ja': ['月', '火', '水', '木', '金', '土', '日']
    }
    active_days = days_map.get(lang, days_map['uz'])

    for day in weekly_days:
        count = UserProgress.objects.filter(
            is_completed=True,
            completed_at__date=day
        ).count()
        label = active_days[day.weekday()]
        weekly_counts.append({'label': label, 'count': count})
    weekly_bars = build_bar_series(weekly_counts)

    # Oylik statistika (so'nggi 7 hafta)
    weekly_ranges = []
    for offset in range(6, -1, -1):
        start = today - timedelta(weeks=offset)
        end = start + timedelta(days=7)
        weekly_ranges.append((start, end))
    monthly_counts = []
    for start, end in weekly_ranges:
        count = UserProgress.objects.filter(
            is_completed=True,
            completed_at__date__gte=start,
            completed_at__date__lt=end
        ).count()
        # Haftaning boshlanish sanasi (masalan: 01.01)
        label = start.strftime('%d.%m')
        monthly_counts.append({'label': label, 'count': count})
    monthly_bars = build_bar_series(monthly_counts)

    # Xonalar bo'yicha yechimlar (top 7)
    room_completion_counts = []
    for room in rooms[:7]:
        count = UserProgress.objects.filter(
            room=room,
            is_completed=True
        ).count()
        room_completion_counts.append({'label': f"{room.order}", 'count': count})
    room_bars = build_bar_series(room_completion_counts)
    
    context = {
        'user_stats': user_stats,
        'top_players': top_players,
        'total_stats': total_stats,
        'room_stats': room_stats,
        'recent_activities': recent_activities,
        'weekly_bars': weekly_bars,
        'monthly_bars': monthly_bars,
        'room_bars': room_bars,
        'weekly_total': sum(item['count'] for item in weekly_counts),
        'monthly_total': sum(item['count'] for item in monthly_counts),
        'room_total': sum(item['count'] for item in room_completion_counts),
    }
    return render(request, 'game/dashboard.html', context)


@login_required
def profile_view(request):
    """Foydalanuvchi profili"""
    stats, _ = UserStatistics.objects.get_or_create(user=request.user)
    stats.update_statistics()

    recent_progress = UserProgress.objects.filter(
        user=request.user,
        is_completed=True
    ).select_related('puzzle', 'room').order_by('-completed_at')[:5]

    context = {
        'stats': stats,
        'recent_progress': recent_progress,
        'badges': get_user_badges(request.user),
    }
    return render(request, 'game/profile.html', context)


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

    leaderboard = UserStatistics.objects.select_related('user').order_by(
        '-total_score', 'total_time', 'user__username'
    )[:10]

    higher_rank_count = UserStatistics.objects.filter(
        Q(total_score__gt=stats.total_score) |
        Q(total_score=stats.total_score, total_time__lt=stats.total_time) |
        Q(total_score=stats.total_score, total_time=stats.total_time, user__username__lt=request.user.username)
    ).count()

    context = {
        'stats': stats,
        'completed_progress': completed_progress[:20],  # Oxirgi 20 ta
        'room_stats': room_stats,
        'badges': get_user_badges(request.user),
        'leaderboard': leaderboard,
        'current_rank': higher_rank_count + 1,
    }
    return render(request, 'game/statistics.html', context)


@require_http_methods(["POST"])
def set_language(request):
    """Tilni o'zgartirish"""
    from django.utils import translation
    
    data = json.loads(request.body)
    lang_code = data.get('language', 'uz')
    
    if lang_code in ['uz', 'en', 'ja']:
        translation.activate(lang_code)
        request.session['django_language'] = lang_code
        response = JsonResponse({'success': True, 'language': lang_code})
        response.set_cookie('django_language', lang_code, max_age=365*24*60*60)
        return response
    
    return JsonResponse({'success': False, 'message': 'Invalid language'})


@login_required
@require_http_methods(["POST"])
def use_hint(request, puzzle_id):
    """Maslahat tokenidan foydalanish"""
    try:
        puzzle = Puzzle.objects.get(id=puzzle_id)
    except Puzzle.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Jumboq topilmadi'})

    progress, _ = UserProgress.objects.get_or_create(
        user=request.user,
        puzzle=puzzle,
        defaults={'room': puzzle.room, 'started_at': timezone.now()}
    )

    if not puzzle.hint:
        return JsonResponse({'success': False, 'message': 'Maslahat mavjud emas'})

    stats, _ = UserStatistics.objects.get_or_create(user=request.user)
    stats.ensure_hint_tokens()

    if progress.used_hint:
        return JsonResponse({
            'success': True,
            'hint': puzzle.hint,
            'tokens_left': stats.hint_tokens,
            'already_used': True,
        })

    if stats.hint_tokens <= 0:
        return JsonResponse({'success': False, 'message': 'Token qolmadi'})

    stats.hint_tokens -= 1
    stats.save(update_fields=['hint_tokens'])
    progress.used_hint = True
    progress.save(update_fields=['used_hint'])

    return JsonResponse({
        'success': True,
        'hint': puzzle.hint,
        'tokens_left': stats.hint_tokens,
        'already_used': False,
    })

