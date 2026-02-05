from django.core.management.base import BaseCommand
from game.models import Room, Puzzle


class Command(BaseCommand):
    help = 'Ma\'lumotlarga tarjimalar qo\'shish'

    def handle(self, *args, **options):
        # Xonalar tarjimalari
        room_translations = {
            "Boshlang'ich xona": {
                'en': {'title': 'Beginner Room', 'description': 'This is your first room. Start with simple puzzles.'},
                'ja': {'title': '初心者の部屋', 'description': 'これはあなたの最初の部屋です。簡単なパズルから始めましょう。'},
            },
            "O'rta xona": {
                'en': {'title': 'Intermediate Room', 'description': 'Continue with harder puzzles.'},
                'ja': {'title': '中級の部屋', 'description': 'より難しいパズルに挑戦しましょう。'},
            },
            "Qiyin xona": {
                'en': {'title': 'Advanced Room', 'description': 'The hardest puzzles are here.'},
                'ja': {'title': '上級の部屋', 'description': '最も難しいパズルがここにあります。'},
            },
        }

        # Jumboqlar tarjimalari
        puzzle_translations = {
            "Oddiy qo'shish": {
                'en': {
                    'title': 'Simple Addition',
                    'description': 'Math puzzle',
                    'question': '2 + 2 = ?',
                    'hint': 'Simple addition operation'
                },
                'ja': {
                    'title': '簡単な足し算',
                    'description': '数学パズル',
                    'question': '2 + 2 = ?',
                    'hint': '簡単な足し算'
                },
            },
            "So'z jumboqi": {
                'en': {
                    'title': 'Word Puzzle',
                    'description': 'Find the word',
                    'question': 'What is the capital of Uzbekistan?',
                    'hint': 'The largest city in Uzbekistan'
                },
                'ja': {
                    'title': '言葉パズル',
                    'description': '言葉を見つけよう',
                    'question': 'ウズベキスタンの首都はどこですか？',
                    'hint': 'ウズベキスタン最大の都市'
                },
            },
            "Mantiqiy jumboq": {
                'en': {
                    'title': 'Logic Puzzle',
                    'description': 'Logical thinking',
                    'question': 'If all humans are immortal and you are human, then you are...?',
                    'hint': 'Draw a logical conclusion'
                },
                'ja': {
                    'title': '論理パズル',
                    'description': '論理的思考',
                    'question': 'すべての人間が不死で、あなたが人間なら、あなたは...?',
                    'hint': '論理的な結論を導き出してください'
                },
            },
            "Ko'paytirish": {
                'en': {
                    'title': 'Multiplication',
                    'description': 'Math puzzle',
                    'question': '7 × 8 = ?',
                    'hint': 'Remember the multiplication table'
                },
                'ja': {
                    'title': '掛け算',
                    'description': '数学パズル',
                    'question': '7 × 8 = ?',
                    'hint': '九九を思い出してください'
                },
            },
            "Teskari so'z": {
                'en': {
                    'title': 'Reverse Word',
                    'description': 'Word puzzle',
                    'question': 'Read "KITOB" backwards',
                    'hint': 'Read the letters in reverse order'
                },
                'ja': {
                    'title': '逆さ言葉',
                    'description': '言葉パズル',
                    'question': '「KITOB」を逆から読んでください',
                    'hint': '文字を逆順で読んでください'
                },
            },
            "Murakkab matematika": {
                'en': {
                    'title': 'Complex Math',
                    'description': 'Difficult math problem',
                    'question': '(10 + 5) × 2 - 8 = ?',
                    'hint': 'Calculate parentheses first'
                },
                'ja': {
                    'title': '複雑な数学',
                    'description': '難しい数学の問題',
                    'question': '(10 + 5) × 2 - 8 = ?',
                    'hint': 'まず括弧の中を計算してください'
                },
            },
        }

        # Xonalarni yangilash
        for room in Room.objects.all():
            title_uz = room.title_uz or room.title
            
            # Tarjimalarni qo'shish
            for key, trans in room_translations.items():
                if key in str(title_uz):
                    room.title_en = trans['en']['title']
                    room.description_en = trans['en']['description']
                    room.title_ja = trans['ja']['title']
                    room.description_ja = trans['ja']['description']
                    room.save()
                    self.stdout.write(self.style.SUCCESS(f'Xona yangilandi: {key}'))
                    break

        # Jumboqlarni yangilash
        for puzzle in Puzzle.objects.all():
            title_uz = puzzle.title_uz or puzzle.title
            
            # Tarjimalarni qo'shish
            for key, trans in puzzle_translations.items():
                if key in str(title_uz):
                    puzzle.title_en = trans['en']['title']
                    puzzle.description_en = trans['en']['description']
                    puzzle.question_en = trans['en']['question']
                    puzzle.hint_en = trans['en'].get('hint', '')
                    
                    puzzle.title_ja = trans['ja']['title']
                    puzzle.description_ja = trans['ja']['description']
                    puzzle.question_ja = trans['ja']['question']
                    puzzle.hint_ja = trans['ja'].get('hint', '')
                    puzzle.save()
                    self.stdout.write(self.style.SUCCESS(f'Jumboq yangilandi: {key}'))
                    break

        self.stdout.write(self.style.SUCCESS('Barcha tarjimalar qo\'shildi!'))
