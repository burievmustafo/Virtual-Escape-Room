from modeltranslation.translator import translator, TranslationOptions
from .models import Room, Puzzle


class RoomTranslationOptions(TranslationOptions):
    """Xona modeli uchun tarjima maydonlari"""
    fields = ('title', 'description')


class PuzzleTranslationOptions(TranslationOptions):
    """Jumboq modeli uchun tarjima maydonlari"""
    fields = ('title', 'description', 'question', 'hint', 'correct_answer')


translator.register(Room, RoomTranslationOptions)
translator.register(Puzzle, PuzzleTranslationOptions)
