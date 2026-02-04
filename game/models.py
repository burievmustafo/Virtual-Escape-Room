from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Room(models.Model):
    """Xona modeli - har birida maxsus jumboq"""
    title = models.CharField(max_length=200, verbose_name="Xona nomi")
    description = models.TextField(verbose_name="Tavsif")
    order = models.IntegerField(unique=True, verbose_name="Tartib raqami")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Xona"
        verbose_name_plural = "Xonalar"
        ordering = ['order']
    
    def __str__(self):
        return f"{self.order}. {self.title}"


class Puzzle(models.Model):
    """Jumboq modeli"""
    PUZZLE_TYPES = [
        ('math', 'Matematika'),
        ('logic', 'Mantiqiy'),
        ('word', 'So\'z'),
        ('memory', 'Xotira'),
        ('pattern', 'Naqsh'),
    ]
    
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='puzzles', verbose_name="Xona")
    title = models.CharField(max_length=200, verbose_name="Jumboq nomi")
    description = models.TextField(verbose_name="Tavsif")
    puzzle_type = models.CharField(max_length=20, choices=PUZZLE_TYPES, verbose_name="Jumboq turi")
    question = models.TextField(verbose_name="Savol")
    correct_answer = models.CharField(max_length=500, verbose_name="To'g'ri javob")
    points = models.IntegerField(default=10, verbose_name="Ball")
    order = models.IntegerField(verbose_name="Tartib raqami")
    hint = models.TextField(blank=True, null=True, verbose_name="Maslahat")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Jumboq"
        verbose_name_plural = "Jumboqlar"
        ordering = ['room', 'order']
        unique_together = ['room', 'order']
    
    def __str__(self):
        return f"{self.room.title} - {self.title}"


class UserProgress(models.Model):
    """Foydalanuvchi progressi"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progress', verbose_name="Foydalanuvchi")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='user_progress', verbose_name="Xona")
    puzzle = models.ForeignKey(Puzzle, on_delete=models.CASCADE, related_name='user_progress', verbose_name="Jumboq")
    is_completed = models.BooleanField(default=False, verbose_name="Tugallangan")
    started_at = models.DateTimeField(auto_now_add=True, verbose_name="Boshlangan vaqt")
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name="Tugallangan vaqt")
    time_taken = models.IntegerField(default=0, verbose_name="O'tkazilgan vaqt (soniya)")
    attempts = models.IntegerField(default=0, verbose_name="Urinishlar soni")
    score = models.IntegerField(default=0, verbose_name="Ball")
    
    class Meta:
        verbose_name = "Foydalanuvchi progressi"
        verbose_name_plural = "Foydalanuvchi progresslari"
        unique_together = ['user', 'puzzle']
        ordering = ['-completed_at', '-started_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.puzzle.title}"
    
    def complete(self, time_taken):
        """Jumboqni tugallash"""
        self.is_completed = True
        self.completed_at = timezone.now()
        self.time_taken = time_taken
        self.attempts += 1
        # Vaqtga qarab ball hisoblash
        base_score = self.puzzle.points
        if time_taken < 30:
            self.score = base_score
        elif time_taken < 60:
            self.score = int(base_score * 0.9)
        elif time_taken < 120:
            self.score = int(base_score * 0.7)
        else:
            self.score = int(base_score * 0.5)
        self.save()


class UserStatistics(models.Model):
    """Foydalanuvchi statistikasi"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='statistics', verbose_name="Foydalanuvchi")
    total_score = models.IntegerField(default=0, verbose_name="Jami ball")
    rooms_completed = models.IntegerField(default=0, verbose_name="Tugallangan xonalar")
    puzzles_completed = models.IntegerField(default=0, verbose_name="Tugallangan jumboqlar")
    total_time = models.IntegerField(default=0, verbose_name="Jami vaqt (soniya)")
    current_room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True, 
                                     related_name='current_users', verbose_name="Joriy xona")
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Foydalanuvchi statistikasi"
        verbose_name_plural = "Foydalanuvchi statistikasi"
    
    def __str__(self):
        return f"{self.user.username} - {self.total_score} ball"
    
    def update_statistics(self):
        """Statistikani yangilash"""
        from django.db.models import Sum
        completed_progress = UserProgress.objects.filter(user=self.user, is_completed=True)
        self.puzzles_completed = completed_progress.count()
        self.total_score = completed_progress.aggregate(total=Sum('score'))['total'] or 0
        self.total_time = completed_progress.aggregate(total=Sum('time_taken'))['total'] or 0
        
        # Tugallangan xonalarni hisoblash
        completed_rooms = Room.objects.filter(
            puzzles__user_progress__user=self.user,
            puzzles__user_progress__is_completed=True
        ).distinct()
        
        # Barcha jumboqlari tugallangan xonalarni topish
        all_rooms = Room.objects.filter(is_active=True).order_by('order')
        self.rooms_completed = 0
        for room in all_rooms:
            room_puzzles = room.puzzles.all()
            if room_puzzles.exists():
                completed_count = UserProgress.objects.filter(
                    user=self.user,
                    puzzle__in=room_puzzles,
                    is_completed=True
                ).count()
                if completed_count == room_puzzles.count():
                    self.rooms_completed += 1
                else:
                    break
        
        # Joriy xonani aniqlash
        if self.rooms_completed < all_rooms.count():
            self.current_room = all_rooms[self.rooms_completed] if self.rooms_completed < all_rooms.count() else None
        else:
            self.current_room = None
        
        self.save()

