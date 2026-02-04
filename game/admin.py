from django.contrib import admin
from .models import Room, Puzzle, UserProgress, UserStatistics


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['order', 'title', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'description']
    list_per_page = 20


@admin.register(Puzzle)
class PuzzleAdmin(admin.ModelAdmin):
    list_display = ['title', 'room', 'puzzle_type', 'points', 'order']
    list_filter = ['puzzle_type', 'room']
    search_fields = ['title', 'question', 'correct_answer']
    ordering = ['room', 'order']
    list_per_page = 25
    
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('room', 'title', 'description', 'puzzle_type', 'order')
        }),
        ('Savol va javob', {
            'fields': ('question', 'correct_answer', 'hint')
        }),
        ('Ball', {
            'fields': ('points',)
        }),
    )


@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'puzzle', 'room', 'is_completed', 'score', 'time_taken', 'attempts', 'completed_at']
    list_filter = ['is_completed', 'room', 'completed_at']
    search_fields = ['user__username', 'puzzle__title']
    readonly_fields = ['started_at', 'completed_at', 'score']
    list_per_page = 30


@admin.register(UserStatistics)
class UserStatisticsAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_score', 'rooms_completed', 'puzzles_completed', 'total_time', 'current_room', 'updated_at']
    list_filter = ['rooms_completed', 'updated_at']
    search_fields = ['user__username']
    readonly_fields = ['updated_at', 'total_score', 'rooms_completed', 'puzzles_completed', 'total_time']
    list_per_page = 30


