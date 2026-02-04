from django.core.management.base import BaseCommand
from game.models import Room, Puzzle


class Command(BaseCommand):
    help = 'Har bir xonaga 15 ta jumboq yaratish (qiyinchilik darajasi bilan)'

    def handle(self, *args, **options):
        # Mavjud jumboqlarni o'chirish
        Puzzle.objects.all().delete()
        self.stdout.write(self.style.WARNING('Eski jumboqlar o\'chirildi'))
        
        # Xona 1: Boshlang'ich (Oddiy matematika va so'z jumboqlari)
        room1, _ = Room.objects.get_or_create(
            order=1,
            defaults={
                'title': 'Boshlang\'ich xona',
                'description': 'Oddiy jumboqlar bilan boshlang. Matematika va so\'z jumboqlari.',
                'is_active': True
            }
        )
        self._create_room1_puzzles(room1)
        
        # Xona 2: O'rta (Murakkab matematika va mantiqiy jumboqlar)
        room2, _ = Room.objects.get_or_create(
            order=2,
            defaults={
                'title': 'O\'rta xona',
                'description': 'Qiyinroq matematika va mantiqiy jumboqlar.',
                'is_active': True
            }
        )
        self._create_room2_puzzles(room2)
        
        # Xona 3: Qiyin (Murakkab mantiqiy jumboqlar)
        room3, _ = Room.objects.get_or_create(
            order=3,
            defaults={
                'title': 'Qiyin xona',
                'description': 'Murakkab mantiqiy jumboqlar.',
                'is_active': True
            }
        )
        self._create_room3_puzzles(room3)
        
        # Xona 4: Juda qiyin (Faqat mantiqiy fikrlash)
        room4, _ = Room.objects.get_or_create(
            order=4,
            defaults={
                'title': 'Juda qiyin xona',
                'description': 'Faqat mantiqiy fikrlash kerak bo\'lgan jumboqlar.',
                'is_active': True
            }
        )
        self._create_room4_puzzles(room4)
        
        self.stdout.write(self.style.SUCCESS('Barcha jumboqlar muvaffaqiyatli yaratildi!'))

    def _create_room1_puzzles(self, room):
        """Boshlang'ich xona - Oddiy jumboqlar"""
        puzzles = [
            {'order': 1, 'title': 'Oddiy qo\'shish', 'type': 'math', 
             'question': '2 + 3 = ?', 'answer': '5', 'points': 10, 
             'hint': 'Oddiy qo\'shish amali'},
            {'order': 2, 'title': 'Ko\'paytirish', 'type': 'math',
             'question': '4 × 5 = ?', 'answer': '20', 'points': 10,
             'hint': 'Ko\'paytirish jadvalini eslang'},
            {'order': 3, 'title': 'Ayirish', 'type': 'math',
             'question': '10 - 7 = ?', 'answer': '3', 'points': 10,
             'hint': 'Oddiy ayirish'},
            {'order': 4, 'title': 'Bo\'lish', 'type': 'math',
             'question': '15 ÷ 3 = ?', 'answer': '5', 'points': 10,
             'hint': 'Bo\'lish amali'},
            {'order': 5, 'title': 'O\'zbekiston poytaxti', 'type': 'word',
             'question': 'O\'zbekiston poytaxti qayer?', 'answer': 'toshkent', 'points': 15,
             'hint': 'O\'zbekistonning eng katta shahri'},
            {'order': 6, 'title': 'Rang', 'type': 'word',
             'question': 'Quyosh rangini yozing', 'answer': 'sariq', 'points': 10,
             'hint': 'Quyosh qanday rangda?'},
            {'order': 7, 'title': 'Qo\'shish', 'type': 'math',
             'question': '7 + 8 = ?', 'answer': '15', 'points': 10,
             'hint': 'Qo\'shish'},
            {'order': 8, 'title': 'Ko\'paytirish', 'type': 'math',
             'question': '6 × 7 = ?', 'answer': '42', 'points': 15,
             'hint': 'Ko\'paytirish'},
            {'order': 9, 'title': 'Teskari so\'z', 'type': 'word',
             'question': '"KITOB" so\'zini teskari o\'qing', 'answer': 'botik', 'points': 15,
             'hint': 'Harflarni teskari tartibda o\'qing'},
            {'order': 10, 'title': 'Qo\'shish', 'type': 'math',
             'question': '12 + 15 = ?', 'answer': '27', 'points': 10,
             'hint': 'Qo\'shish'},
            {'order': 11, 'title': 'Ayirish', 'type': 'math',
             'question': '20 - 9 = ?', 'answer': '11', 'points': 10,
             'hint': 'Ayirish'},
            {'order': 12, 'title': 'Bo\'lish', 'type': 'math',
             'question': '24 ÷ 4 = ?', 'answer': '6', 'points': 10,
             'hint': 'Bo\'lish'},
            {'order': 13, 'title': 'Ko\'paytirish', 'type': 'math',
             'question': '9 × 9 = ?', 'answer': '81', 'points': 15,
             'hint': 'Ko\'paytirish'},
            {'order': 14, 'title': 'So\'z jumboqi', 'type': 'word',
             'question': 'Yilning birinchi oyi?', 'answer': 'yanvar', 'points': 10,
             'hint': 'Yilning birinchi oyi'},
            {'order': 15, 'title': 'Qo\'shish', 'type': 'math',
             'question': '25 + 17 = ?', 'answer': '42', 'points': 15,
             'hint': 'Qo\'shish'},
        ]
        self._create_puzzles(room, puzzles)

    def _create_room2_puzzles(self, room):
        """O'rta xona - Murakkab matematika va mantiqiy"""
        puzzles = [
            {'order': 1, 'title': 'Murakkab qo\'shish', 'type': 'math',
             'question': '(10 + 5) × 2 = ?', 'answer': '30', 'points': 20,
             'hint': 'Qavslarni avval hisoblang'},
            {'order': 2, 'title': 'Mantiqiy jumboq 1', 'type': 'logic',
             'question': 'Agar barcha odamlar o\'limsiz bo\'lsa va Siz odamsiz, demak Siz...?', 
             'answer': 'o\'limsiz', 'points': 25,
             'hint': 'Mantiqiy xulosa chiqaring'},
            {'order': 3, 'title': 'Ko\'paytirish', 'type': 'math',
             'question': '7 × 8 = ?', 'answer': '56', 'points': 15,
             'hint': 'Ko\'paytirish'},
            {'order': 4, 'title': 'Mantiqiy jumboq 2', 'type': 'logic',
             'question': 'Agar barcha qushlar uchsa va penguin qush bo\'lsa, penguin...?', 
             'answer': 'uchmaydi', 'points': 30,
             'hint': 'Penguin haqida o\'ylang'},
            {'order': 5, 'title': 'Murakkab matematika', 'type': 'math',
             'question': '(15 + 5) × 3 - 10 = ?', 'answer': '50', 'points': 25,
             'hint': 'Qavslarni avval hisoblang'},
            {'order': 6, 'title': 'Mantiqiy jumboq 3', 'type': 'logic',
             'question': 'Agar barcha mevalar shirin bo\'lsa va limon meva bo\'lsa, limon...?', 
             'answer': 'shirin emas', 'points': 30,
             'hint': 'Limon haqida o\'ylang'},
            {'order': 7, 'title': 'Bo\'lish', 'type': 'math',
             'question': '100 ÷ 4 = ?', 'answer': '25', 'points': 15,
             'hint': 'Bo\'lish'},
            {'order': 8, 'title': 'Mantiqiy jumboq 4', 'type': 'logic',
             'question': 'Agar barcha sutemizuvchilar yashasa va baliq sutemizuvchi bo\'lmasa, baliq...?', 
             'answer': 'yashaydi', 'points': 30,
             'hint': 'Mantiqiy fikrlang'},
            {'order': 9, 'title': 'Ko\'paytirish', 'type': 'math',
             'question': '12 × 6 = ?', 'answer': '72', 'points': 20,
             'hint': 'Ko\'paytirish'},
            {'order': 10, 'title': 'Mantiqiy jumboq 5', 'type': 'logic',
             'question': 'Agar barcha hayvonlar yurish qobiliyatiga ega bo\'lsa va baliq hayvon bo\'lsa, baliq...?', 
             'answer': 'yurmaydi', 'points': 30,
             'hint': 'Baliq qanday harakatlanadi?'},
            {'order': 11, 'title': 'Murakkab matematika', 'type': 'math',
             'question': '50 - (10 × 3) = ?', 'answer': '20', 'points': 20,
             'hint': 'Ko\'paytirishni avval bajaring'},
            {'order': 12, 'title': 'Mantiqiy jumboq 6', 'type': 'logic',
             'question': 'Agar barcha qushlar tuxum qo\'ysa va tuya qush bo\'lmasa, tuya...?', 
             'answer': 'tuxum qo\'ymaydi', 'points': 25,
             'hint': 'Mantiqiy fikrlang'},
            {'order': 13, 'title': 'Qo\'shish', 'type': 'math',
             'question': '35 + 47 = ?', 'answer': '82', 'points': 20,
             'hint': 'Qo\'shish'},
            {'order': 14, 'title': 'Mantiqiy jumboq 7', 'type': 'logic',
             'question': 'Agar barcha mevalar o\'simlik bo\'lsa va olma meva bo\'lsa, olma...?', 
             'answer': 'o\'simlik', 'points': 25,
             'hint': 'Mantiqiy xulosa'},
            {'order': 15, 'title': 'Murakkab matematika', 'type': 'math',
             'question': '(20 + 10) ÷ 5 = ?', 'answer': '6', 'points': 20,
             'hint': 'Qavslarni avval hisoblang'},
        ]
        self._create_puzzles(room, puzzles)

    def _create_room3_puzzles(self, room):
        """Qiyin xona - Murakkab mantiqiy jumboqlar"""
        puzzles = [
            {'order': 1, 'title': 'Mantiqiy jumboq 1', 'type': 'logic',
             'question': 'Agar barcha kitoblar qog\'ozdan bo\'lsa va elektron kitob kitob bo\'lsa, elektron kitob...?', 
             'answer': 'qog\'ozdan emas', 'points': 35,
             'hint': 'Elektron kitob haqida o\'ylang'},
            {'order': 2, 'title': 'Mantiqiy jumboq 2', 'type': 'logic',
             'question': 'Agar barcha transport vositalari yo\'lda harakatlansa va samolyot transport bo\'lsa, samolyot...?', 
             'answer': 'yo\'lda harakatlanmaydi', 'points': 35,
             'hint': 'Samolyot qayerda harakatlanadi?'},
            {'order': 3, 'title': 'Mantiqiy jumboq 3', 'type': 'logic',
             'question': 'Agar barcha sutemizuvchilar tirik bo\'lsa va dinozavr sutemizuvchi bo\'lmasa, dinozavr...?', 
             'answer': 'tirik emas', 'points': 40,
             'hint': 'Dinozavr haqida o\'ylang'},
            {'order': 4, 'title': 'Mantiqiy jumboq 4', 'type': 'logic',
             'question': 'Agar barcha suv suyuq bo\'lsa va muz suv bo\'lsa, muz...?', 
             'answer': 'suyuq emas', 'points': 35,
             'hint': 'Muz qanday holatda?'},
            {'order': 5, 'title': 'Mantiqiy jumboq 5', 'type': 'logic',
             'question': 'Agar barcha hayvonlar nafas olsa va o\'simlik hayvon bo\'lmasa, o\'simlik...?', 
             'answer': 'nafas oladi', 'points': 40,
             'hint': 'O\'simliklar nafas oladimi?'},
            {'order': 6, 'title': 'Mantiqiy jumboq 6', 'type': 'logic',
             'question': 'Agar barcha shaharlar aholiga ega bo\'lsa va qishloq shahar bo\'lmasa, qishloq...?', 
             'answer': 'aholiga ega', 'points': 35,
             'hint': 'Mantiqiy fikrlang'},
            {'order': 7, 'title': 'Mantiqiy jumboq 7', 'type': 'logic',
             'question': 'Agar barcha mashinalar dvigatelga ega bo\'lsa va velosiped mashina bo\'lsa, velosiped...?', 
             'answer': 'dvigatelga ega emas', 'points': 40,
             'hint': 'Velosiped qanday ishlaydi?'},
            {'order': 8, 'title': 'Mantiqiy jumboq 8', 'type': 'logic',
             'question': 'Agar barcha mevalar shirin bo\'lsa va olcha meva bo\'lsa, olcha...?', 
             'answer': 'shirin', 'points': 30,
             'hint': 'Mantiqiy xulosa'},
            {'order': 9, 'title': 'Mantiqiy jumboq 9', 'type': 'logic',
             'question': 'Agar barcha qushlar uchsa va tuya qush bo\'lmasa, tuya...?', 
             'answer': 'uchmaydi', 'points': 30,
             'hint': 'Tuya haqida o\'ylang'},
            {'order': 10, 'title': 'Mantiqiy jumboq 10', 'type': 'logic',
             'question': 'Agar barcha sutemizuvchilar onasi bo\'lsa va baliq sutemizuvchi bo\'lmasa, baliq...?', 
             'answer': 'onasi bor', 'points': 40,
             'hint': 'Baliqning onasi bormi?'},
            {'order': 11, 'title': 'Mantiqiy jumboq 11', 'type': 'logic',
             'question': 'Agar barcha transport vositalari yoqilg\'i ishlatsa va velosiped transport bo\'lsa, velosiped...?', 
             'answer': 'yoqilg\'i ishlatmaydi', 'points': 40,
             'hint': 'Velosiped qanday ishlaydi?'},
            {'order': 12, 'title': 'Mantiqiy jumboq 12', 'type': 'logic',
             'question': 'Agar barcha mevalar o\'simlik bo\'lsa va sabzi meva bo\'lmasa, sabzi...?', 
             'answer': 'o\'simlik', 'points': 35,
             'hint': 'Sabzi nima?'},
            {'order': 13, 'title': 'Mantiqiy jumboq 13', 'type': 'logic',
             'question': 'Agar barcha hayvonlar harakatlansa va o\'simlik hayvon bo\'lmasa, o\'simlik...?', 
             'answer': 'harakatlanadi', 'points': 40,
             'hint': 'O\'simliklar harakatlanadimi?'},
            {'order': 14, 'title': 'Mantiqiy jumboq 14', 'type': 'logic',
             'question': 'Agar barcha qushlar tuxum qo\'ysa va tuya qush bo\'lmasa, tuya...?', 
             'answer': 'tuxum qo\'ymaydi', 'points': 35,
             'hint': 'Mantiqiy fikrlang'},
            {'order': 15, 'title': 'Mantiqiy jumboq 15', 'type': 'logic',
             'question': 'Agar barcha sutemizuvchilar sut beradi va odam sutemizuvchi bo\'lsa, odam...?', 
             'answer': 'sut beradi', 'points': 35,
             'hint': 'Mantiqiy xulosa'},
        ]
        self._create_puzzles(room, puzzles)

    def _create_room4_puzzles(self, room):
        """Juda qiyin xona - Faqat mantiqiy fikrlash"""
        puzzles = [
            {'order': 1, 'title': 'Mantiqiy paradoks 1', 'type': 'logic',
             'question': 'Agar "Bu gap yolg\'on" gapi to\'g\'ri bo\'lsa, u yolg\'onmi yoki to\'g\'rimi?', 
             'answer': 'paradoks', 'points': 50,
             'hint': 'Paradoks haqida o\'ylang'},
            {'order': 2, 'title': 'Mantiqiy jumboq 1', 'type': 'logic',
             'question': 'Agar barcha qushlar uchsa va pingvin qush bo\'lsa, pingvin...?', 
             'answer': 'uchmaydi', 'points': 45,
             'hint': 'Pingvin haqida o\'ylang'},
            {'order': 3, 'title': 'Mantiqiy jumboq 2', 'type': 'logic',
             'question': 'Agar barcha sutemizuvchilar onasi bo\'lsa va tuya sutemizuvchi bo\'lsa, tuya...?', 
             'answer': 'onasi bor', 'points': 45,
             'hint': 'Mantiqiy fikrlang'},
            {'order': 4, 'title': 'Mantiqiy jumboq 3', 'type': 'logic',
             'question': 'Agar barcha transport vositalari yo\'lda harakatlansa va kema transport bo\'lsa, kema...?', 
             'answer': 'yo\'lda harakatlanmaydi', 'points': 45,
             'hint': 'Kema qayerda harakatlanadi?'},
            {'order': 5, 'title': 'Mantiqiy jumboq 4', 'type': 'logic',
             'question': 'Agar barcha mevalar shirin bo\'lsa va limon meva bo\'lsa, limon...?', 
             'answer': 'shirin emas', 'points': 45,
             'hint': 'Limon haqida o\'ylang'},
            {'order': 6, 'title': 'Mantiqiy jumboq 5', 'type': 'logic',
             'question': 'Agar barcha hayvonlar nafas olsa va o\'simlik hayvon bo\'lmasa, o\'simlik...?', 
             'answer': 'nafas oladi', 'points': 45,
             'hint': 'O\'simliklar nafas oladimi?'},
            {'order': 7, 'title': 'Mantiqiy jumboq 6', 'type': 'logic',
             'question': 'Agar barcha qushlar tuxum qo\'ysa va tuya qush bo\'lmasa, tuya...?', 
             'answer': 'tuxum qo\'ymaydi', 'points': 45,
             'hint': 'Mantiqiy fikrlang'},
            {'order': 8, 'title': 'Mantiqiy jumboq 7', 'type': 'logic',
             'question': 'Agar barcha sutemizuvchilar tirik bo\'lsa va dinozavr sutemizuvchi bo\'lmasa, dinozavr...?', 
             'answer': 'tirik emas', 'points': 50,
             'hint': 'Dinozavr haqida o\'ylang'},
            {'order': 9, 'title': 'Mantiqiy jumboq 8', 'type': 'logic',
             'question': 'Agar barcha mashinalar dvigatelga ega bo\'lsa va velosiped mashina bo\'lsa, velosiped...?', 
             'answer': 'dvigatelga ega emas', 'points': 50,
             'hint': 'Velosiped qanday ishlaydi?'},
            {'order': 10, 'title': 'Mantiqiy jumboq 9', 'type': 'logic',
             'question': 'Agar barcha transport vositalari yoqilg\'i ishlatsa va velosiped transport bo\'lsa, velosiped...?', 
             'answer': 'yoqilg\'i ishlatmaydi', 'points': 50,
             'hint': 'Velosiped qanday ishlaydi?'},
            {'order': 11, 'title': 'Mantiqiy jumboq 10', 'type': 'logic',
             'question': 'Agar barcha mevalar o\'simlik bo\'lsa va sabzi meva bo\'lmasa, sabzi...?', 
             'answer': 'o\'simlik', 'points': 45,
             'hint': 'Sabzi nima?'},
            {'order': 12, 'title': 'Mantiqiy jumboq 11', 'type': 'logic',
             'question': 'Agar barcha hayvonlar harakatlansa va o\'simlik hayvon bo\'lmasa, o\'simlik...?', 
             'answer': 'harakatlanadi', 'points': 50,
             'hint': 'O\'simliklar harakatlanadimi?'},
            {'order': 13, 'title': 'Mantiqiy jumboq 12', 'type': 'logic',
             'question': 'Agar barcha qushlar uchsa va tuya qush bo\'lmasa, tuya...?', 
             'answer': 'uchmaydi', 'points': 45,
             'hint': 'Tuya haqida o\'ylang'},
            {'order': 14, 'title': 'Mantiqiy jumboq 13', 'type': 'logic',
             'question': 'Agar barcha sutemizuvchilar sut beradi va odam sutemizuvchi bo\'lsa, odam...?', 
             'answer': 'sut beradi', 'points': 45,
             'hint': 'Mantiqiy xulosa'},
            {'order': 15, 'title': 'Mantiqiy jumboq 14', 'type': 'logic',
             'question': 'Agar barcha odamlar o\'limsiz bo\'lsa va Siz odamsiz, demak Siz...?', 
             'answer': 'o\'limsiz', 'points': 50,
             'hint': 'Mantiqiy xulosa chiqaring'},
        ]
        self._create_puzzles(room, puzzles)

    def _create_puzzles(self, room, puzzles_data):
        """Jumboqlarni yaratish"""
        for puzzle_data in puzzles_data:
            Puzzle.objects.create(
                room=room,
                title=puzzle_data['title'],
                description=f'{puzzle_data["type"]} jumboq',
                puzzle_type=puzzle_data['type'],
                question=puzzle_data['question'],
                correct_answer=puzzle_data['answer'],
                points=puzzle_data['points'],
                order=puzzle_data['order'],
                hint=puzzle_data.get('hint', '')
            )
        self.stdout.write(self.style.SUCCESS(f'{room.title}: {len(puzzles_data)} ta jumboq yaratildi'))

