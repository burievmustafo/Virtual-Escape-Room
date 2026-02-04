from django.core.management.base import BaseCommand
from game.models import Room, Puzzle


class Command(BaseCommand):
    help = 'Namuna ma\'lumotlar yaratish'

    def handle(self, *args, **options):
        # Xona 1
        room1, created = Room.objects.get_or_create(
            order=1,
            defaults={
                'title': 'Boshlang\'ich xona',
                'description': 'Bu sizning birinchi xonangiz. Oddiy jumboqlar bilan boshlang.',
                'is_active': True
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'Xona yaratildi: {room1.title}'))
            
            # Jumboq 1-1
            Puzzle.objects.get_or_create(
                room=room1,
                order=1,
                defaults={
                    'title': 'Oddiy qo\'shish',
                    'description': 'Matematik jumboq',
                    'puzzle_type': 'math',
                    'question': '2 + 2 = ?',
                    'correct_answer': '4',
                    'points': 10,
                    'hint': 'Oddiy qo\'shish amali'
                }
            )
            
            # Jumboq 1-2
            Puzzle.objects.get_or_create(
                room=room1,
                order=2,
                defaults={
                    'title': 'So\'z jumboqi',
                    'description': 'So\'z topish',
                    'puzzle_type': 'word',
                    'question': 'O\'zbekiston poytaxti qayer?',
                    'correct_answer': 'toshkent',
                    'points': 15,
                    'hint': 'O\'zbekistonning eng katta shahri'
                }
            )
            
            # Jumboq 1-3
            Puzzle.objects.get_or_create(
                room=room1,
                order=3,
                defaults={
                    'title': 'Mantiqiy jumboq',
                    'description': 'Mantiqiy fikrlash',
                    'puzzle_type': 'logic',
                    'question': 'Agar barcha odamlar o\'limsiz bo\'lsa va Siz odamsiz, demak Siz...?',
                    'correct_answer': 'o\'limsiz',
                    'points': 20,
                    'hint': 'Mantiqiy xulosa chiqaring'
                }
            )
        
        # Xona 2
        room2, created = Room.objects.get_or_create(
            order=2,
            defaults={
                'title': 'O\'rta xona',
                'description': 'Qiyinroq jumboqlar bilan davom eting.',
                'is_active': True
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'Xona yaratildi: {room2.title}'))
            
            # Jumboq 2-1
            Puzzle.objects.get_or_create(
                room=room2,
                order=1,
                defaults={
                    'title': 'Ko\'paytirish',
                    'description': 'Matematik jumboq',
                    'puzzle_type': 'math',
                    'question': '7 × 8 = ?',
                    'correct_answer': '56',
                    'points': 15,
                    'hint': 'Ko\'paytirish jadvalini eslang'
                }
            )
            
            # Jumboq 2-2
            Puzzle.objects.get_or_create(
                room=room2,
                order=2,
                defaults={
                    'title': 'Teskari so\'z',
                    'description': 'So\'z jumboqi',
                    'puzzle_type': 'word',
                    'question': '"KITOB" so\'zini teskari o\'qing',
                    'correct_answer': 'botik',
                    'points': 20,
                    'hint': 'Harflarni teskari tartibda o\'qing'
                }
            )
        
        # Xona 3
        room3, created = Room.objects.get_or_create(
            order=3,
            defaults={
                'title': 'Qiyin xona',
                'description': 'Eng qiyin jumboqlar bu yerda.',
                'is_active': True
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'Xona yaratildi: {room3.title}'))
            
            # Jumboq 3-1
            Puzzle.objects.get_or_create(
                room=room3,
                order=1,
                defaults={
                    'title': 'Murakkab matematika',
                    'description': 'Qiyin matematik masala',
                    'puzzle_type': 'math',
                    'question': '(10 + 5) × 2 - 8 = ?',
                    'correct_answer': '22',
                    'points': 25,
                    'hint': 'Qavslarni avval hisoblang'
                }
            )
        
        self.stdout.write(self.style.SUCCESS('Namuna ma\'lumotlar muvaffaqiyatli yaratildi!'))


