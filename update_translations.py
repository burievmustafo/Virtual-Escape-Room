import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'puzzle_game.settings')
django.setup()

from game.models import Room, Puzzle

# Xonalar tarjimalari
rooms_data = [
    {
        'id': 1,
        'title_uz': "Boshlang'ich xona",
        'title_en': 'Beginner Room',
        'title_ja': '初心者の部屋',
        'description_uz': 'Bu sizning birinchi xonangiz. Oddiy jumboqlar bilan boshlang.',
        'description_en': 'This is your first room. Start with simple puzzles.',
        'description_ja': 'これはあなたの最初の部屋です。簡単なパズルから始めましょう。',
    },
    {
        'id': 2,
        'title_uz': "O'rta xona",
        'title_en': 'Intermediate Room',
        'title_ja': '中級の部屋',
        'description_uz': 'Qiyinroq jumboqlar bilan davom eting.',
        'description_en': 'Continue with harder puzzles.',
        'description_ja': 'より難しいパズルに挑戦しましょう。',
    },
    {
        'id': 3,
        'title_uz': 'Qiyin xona',
        'title_en': 'Advanced Room',
        'title_ja': '上級の部屋',
        'description_uz': 'Eng qiyin jumboqlar bu yerda.',
        'description_en': 'The hardest puzzles are here.',
        'description_ja': '最も難しいパズルがここにあります。',
    },
]

# Jumboqlar tarjimalari
puzzles_data = [
    {
        'id': 1,
        'title_uz': "Oddiy qo'shish",
        'title_en': 'Simple Addition',
        'title_ja': '簡単な足し算',
        'description_uz': 'Matematik jumboq',
        'description_en': 'Math puzzle',
        'description_ja': '数学パズル',
        'question_uz': '2 + 2 = ?',
        'question_en': '2 + 2 = ?',
        'question_ja': '2 + 2 = ?',
        'hint_uz': "Oddiy qo'shish amali",
        'hint_en': 'Simple addition operation',
        'hint_ja': '簡単な足し算',
    },
    {
        'id': 2,
        'title_uz': "So'z jumboqi",
        'title_en': 'Word Puzzle',
        'title_ja': '言葉パズル',
        'description_uz': "So'z topish",
        'description_en': 'Find the word',
        'description_ja': '言葉を見つけよう',
        'question_uz': "O'zbekiston poytaxti qayer?",
        'question_en': 'What is the capital of Uzbekistan?',
        'question_ja': 'ウズベキスタンの首都はどこですか？',
        'hint_uz': "O'zbekistonning eng katta shahri",
        'hint_en': 'The largest city in Uzbekistan',
        'hint_ja': 'ウズベキスタン最大の都市',
    },
    {
        'id': 3,
        'title_uz': 'Mantiqiy jumboq',
        'title_en': 'Logic Puzzle',
        'title_ja': '論理パズル',
        'description_uz': 'Mantiqiy fikrlash',
        'description_en': 'Logical thinking',
        'description_ja': '論理的思考',
        'question_uz': "Agar barcha odamlar o'limsiz bo'lsa va Siz odamsiz, demak Siz...?",
        'question_en': 'If all humans are immortal and you are human, then you are...?',
        'question_ja': 'すべての人間が不死で、あなたが人間なら、あなたは...?',
        'hint_uz': 'Mantiqiy xulosa chiqaring',
        'hint_en': 'Draw a logical conclusion',
        'hint_ja': '論理的な結論を導き出してください',
    },
    {
        'id': 4,
        'title_uz': "Ko'paytirish",
        'title_en': 'Multiplication',
        'title_ja': '掛け算',
        'description_uz': 'Matematik jumboq',
        'description_en': 'Math puzzle',
        'description_ja': '数学パズル',
        'question_uz': '7 × 8 = ?',
        'question_en': '7 × 8 = ?',
        'question_ja': '7 × 8 = ?',
        'hint_uz': "Ko'paytirish jadvalini eslang",
        'hint_en': 'Remember the multiplication table',
        'hint_ja': '九九を思い出してください',
    },
    {
        'id': 5,
        'title_uz': "Teskari so'z",
        'title_en': 'Reverse Word',
        'title_ja': '逆さ言葉',
        'description_uz': "So'z jumboqi",
        'description_en': 'Word puzzle',
        'description_ja': '言葉パズル',
        'question_uz': '"KITOB" so\'zini teskari o\'qing',
        'question_en': 'Read "KITOB" backwards',
        'question_ja': '「KITOB」を逆から読んでください',
        'hint_uz': "Harflarni teskari tartibda o'qing",
        'hint_en': 'Read the letters in reverse order',
        'hint_ja': '文字を逆順で読んでください',
    },
    {
        'id': 6,
        'title_uz': 'Murakkab matematika',
        'title_en': 'Complex Math',
        'title_ja': '複雑な数学',
        'description_uz': 'Qiyin matematik masala',
        'description_en': 'Difficult math problem',
        'description_ja': '難しい数学の問題',
        'question_uz': '(10 + 5) × 2 - 8 = ?',
        'question_en': '(10 + 5) × 2 - 8 = ?',
        'question_ja': '(10 + 5) × 2 - 8 = ?',
        'hint_uz': 'Qavslarni avval hisoblang',
        'hint_en': 'Calculate parentheses first',
        'hint_ja': 'まず括弧の中を計算してください',
    },
]

# Xonalarni yangilash
for data in rooms_data:
    try:
        room = Room.objects.get(id=data['id'])
        room.title_uz = data['title_uz']
        room.title_en = data['title_en']
        room.title_ja = data['title_ja']
        room.description_uz = data['description_uz']
        room.description_en = data['description_en']
        room.description_ja = data['description_ja']
        room.save()
        print(f"Xona yangilandi: {data['title_uz']}")
    except Room.DoesNotExist:
        print(f"Xona topilmadi: {data['id']}")

# Jumboqlarni yangilash
for data in puzzles_data:
    try:
        puzzle = Puzzle.objects.get(id=data['id'])
        puzzle.title_uz = data['title_uz']
        puzzle.title_en = data['title_en']
        puzzle.title_ja = data['title_ja']
        puzzle.description_uz = data['description_uz']
        puzzle.description_en = data['description_en']
        puzzle.description_ja = data['description_ja']
        puzzle.question_uz = data['question_uz']
        puzzle.question_en = data['question_en']
        puzzle.question_ja = data['question_ja']
        puzzle.hint_uz = data.get('hint_uz', '')
        puzzle.hint_en = data.get('hint_en', '')
        puzzle.hint_ja = data.get('hint_ja', '')
        puzzle.save()
        print(f"Jumboq yangilandi: {data['title_uz']}")
    except Puzzle.DoesNotExist:
        print(f"Jumboq topilmadi: {data['id']}")

print("\nBarcha tarjimalar qo'shildi!")
