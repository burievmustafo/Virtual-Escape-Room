from django.core.management.base import BaseCommand
from django.db import transaction

from game.models import Room, Puzzle


class Command(BaseCommand):
    help = "Seed rooms and puzzles with new content (3 languages)."

    def handle(self, *args, **options):
        rooms_data = [
            {
                "order": 1,
                "title": {"uz": "Detektiv xonasi", "en": "Detective Room", "ja": "探偵の部屋"},
                "description": {
                    "uz": "Jinoyatni oching va begunohni qutqaring.",
                    "en": "Solve the crime and save the innocent.",
                    "ja": "事件を解決して無実の人を救え。",
                },
            },
            {
                "order": 2,
                "title": {"uz": "Piramida", "en": "Pyramid", "ja": "ピラミッド"},
                "description": {
                    "uz": "Qadimiy Misr jumboqlarini yeching.",
                    "en": "Solve ancient Egypt puzzles.",
                    "ja": "古代エジプトの謎を解け。",
                },
            },
            {
                "order": 3,
                "title": {"uz": "Sirli laboratoriya", "en": "Mystery Lab", "ja": "謎の研究所"},
                "description": {
                    "uz": "Xavfli tajriba oldidan kodni toping.",
                    "en": "Find the code before a dangerous experiment.",
                    "ja": "危険な実験の前にコードを見つけよ。",
                },
            },
            {
                "order": 4,
                "title": {"uz": "Junior Developer Room", "en": "Junior Developer Room", "ja": "ジュニア開発者ルーム"},
                "description": {
                    "uz": "Koddagi xatolarni toping va tuzating.",
                    "en": "Find and fix bugs in code.",
                    "ja": "コードのバグを見つけて修正せよ。",
                },
            },
            {
                "order": 5,
                "title": {"uz": "Hacker Server Room", "en": "Hacker Server Room", "ja": "ハッカーサーバールーム"},
                "description": {
                    "uz": "Tizimni himoya qilib, serverni saqlab qoling.",
                    "en": "Protect the system and save the server.",
                    "ja": "システムを守ってサーバーを救え。",
                },
            },
            {
                "order": 6,
                "title": {"uz": "Yapon Ofisi", "en": "Japanese Office", "ja": "日本のオフィス"},
                "description": {
                    "uz": "Ofis vazifalarini bajarib tizimga kiring.",
                    "en": "Complete office tasks to access the system.",
                    "ja": "業務を完了してシステムに入れ。",
                },
            },
        ]

        puzzles_data = [
            {
                "room_order": 1,
                "order": 1,
                "puzzle_type": "logic",
                "points": 25,
                "title": {
                    "uz": "Vaqtni solishtiring",
                    "en": "Compare the Time",
                    "ja": "時間を比較する",
                },
                "description": {
                    "uz": "Gumonlanuvchilarning vaqtini solishtiring.",
                    "en": "Compare suspects' timelines.",
                    "ja": "容疑者の時間を比較する。",
                },
                "question": {
                    "uz": (
                        "Jinoyat vaqti: 20:00\n\n"
                        "Gumonlanuvchilar:\n"
                        "A — 19:00–21:00 kinoda\n"
                        "B — 19:30–20:30 do'konda\n"
                        "C — 20:00 da uyga kelganini aytadi\n\n"
                        "Kamera:\n"
                        "Do'kon kamerasida B 19:40 da ko'rinadi\n"
                        "Kino chiptasi A’da bor\n\n"
                        "Savol: Kim yolg'on gapiryapti?\n"
                        "A) A\nB) B\nC) C"
                    ),
                    "en": (
                        "Crime time: 20:00\n\n"
                        "Suspects:\n"
                        "A — at the cinema 19:00–21:00\n"
                        "B — at the shop 19:30–20:30\n"
                        "C — says arrived home at 20:00\n\n"
                        "Camera:\n"
                        "Shop camera shows B at 19:40\n"
                        "A has a movie ticket\n\n"
                        "Question: Who is lying?\n"
                        "A) A\nB) B\nC) C"
                    ),
                    "ja": (
                        "犯行時刻: 20:00\n\n"
                        "容疑者:\n"
                        "A — 19:00–21:00 に映画館\n"
                        "B — 19:30–20:30 に店\n"
                        "C — 20:00 に帰宅したと言う\n\n"
                        "カメラ:\n"
                        "店のカメラでBが19:40に映っている\n"
                        "Aは映画のチケットを持っている\n\n"
                        "質問: 嘘をついているのは誰？\n"
                        "A) A\nB) B\nC) C"
                    ),
                },
                "correct_answer": {"uz": "C", "en": "C", "ja": "C"},
            },
            {
                "room_order": 1,
                "order": 2,
                "puzzle_type": "logic",
                "points": 25,
                "title": {
                    "uz": "Yamada + vaqt",
                    "en": "Yamada + Time",
                    "ja": "山田＋時間",
                },
                "description": {
                    "uz": "Yamada bo'yicha vaqtni solishtiring.",
                    "en": "Compare timelines with Yamada.",
                    "ja": "山田の時系列を比較する。",
                },
                "question": {
                    "uz": (
                        "Jinoyat: 20:00 – 20:10\n\n"
                        "Dalillar:\n"
                        "A — 19:50–20:30 metroda\n"
                        "B — 19:40–20:05 kafeda\n"
                        "C — 20:15 da uyga kelgan\n\n"
                        "Kameralar:\n"
                        "Metro: A 20:12 da chiqgan\n"
                        "Kafe: B 19:45 da chiqgan\n\n"
                        "Savol: Kim jinoyat qilishi mumkin?\n"
                        "A) A\nB) B\nC) C"
                    ),
                    "en": (
                        "Crime: 20:00 – 20:10\n\n"
                        "Clues:\n"
                        "A — at the metro 19:50–20:30\n"
                        "B — at the cafe 19:40–20:05\n"
                        "C — says arrived home at 20:15\n\n"
                        "Cameras:\n"
                        "Metro: A exits at 20:12\n"
                        "Cafe: B leaves at 19:45\n\n"
                        "Question: Who could have committed the crime?\n"
                        "A) A\nB) B\nC) C"
                    ),
                    "ja": (
                        "犯行: 20:00 – 20:10\n\n"
                        "証言:\n"
                        "A — 19:50–20:30 に地下鉄\n"
                        "B — 19:40–20:05 にカフェ\n"
                        "C — 20:15 に帰宅した\n\n"
                        "カメラ:\n"
                        "地下鉄: Aは20:12に出た\n"
                        "カフェ: Bは19:45に出た\n\n"
                        "質問: 犯行が可能なのは誰？\n"
                        "A) A\nB) B\nC) C"
                    ),
                },
                "correct_answer": {"uz": "B", "en": "B", "ja": "B"},
            },
            {
                "room_order": 1,
                "order": 3,
                "puzzle_type": "logic",
                "points": 25,
                "title": {
                    "uz": "Kim yolg'on gapiryapti?",
                    "en": "Who Is Lying?",
                    "ja": "嘘をついているのは誰？",
                },
                "description": {
                    "uz": "Faqat bittasi rost gapiryapti.",
                    "en": "Only one person is telling the truth.",
                    "ja": "真実は一人だけ。",
                },
                "question": {
                    "uz": (
                        "A: “B qilgan”\n"
                        "B: “A va C yolg'on gapiryapti”\n"
                        "C: “Men qilmaganman”\n\n"
                        "Ma’lumot: Faqat bittasi rost gapiryapti\n\n"
                        "Savol: Kim yolg'on gapiryapti?\n"
                        "A) A\nB) B\nC) C"
                    ),
                    "en": (
                        "A: \"B did it\"\n"
                        "B: \"A and C are lying\"\n"
                        "C: \"I didn't do it\"\n\n"
                        "Info: Only one statement is true.\n\n"
                        "Question: Who is lying?\n"
                        "A) A\nB) B\nC) C"
                    ),
                    "ja": (
                        "A: 「Bがやった」\n"
                        "B: 「AとCは嘘をついている」\n"
                        "C: 「私はやっていない」\n\n"
                        "条件: 真実は1つだけ。\n\n"
                        "質問: 嘘をついているのは誰？\n"
                        "A) A\nB) B\nC) C"
                    ),
                },
                "correct_answer": {"uz": "C", "en": "C", "ja": "C"},
            },
            {
                "room_order": 2,
                "order": 1,
                "puzzle_type": "logic",
                "points": 20,
                "title": {
                    "uz": "Kanji kategoriyasi",
                    "en": "Kanji Category",
                    "ja": "漢字のカテゴリ",
                },
                "description": {
                    "uz": "Kanji belgilarining umumiy kategoriyasini toping.",
                    "en": "Find the common category of kanji.",
                    "ja": "漢字の共通カテゴリを答えよ。",
                },
                "question": {
                    "uz": (
                        "Devor:\n水 → ?\n火 → ?\n木 → ?\n\n"
                        "Pastda:\nUlarning umumiy kategoriyasi nima?\n\n"
                        "Variantlar:\nA) 自然 (tabiat)\nB) 人体 (inson tanasi)\nC) 感情 (his-tuyg'u)"
                    ),
                    "en": (
                        "On the wall:\n水 → ?\n火 → ?\n木 → ?\n\n"
                        "Question:\nWhat is their common category?\n\n"
                        "Options:\nA) 自然 (nature)\nB) 人体 (human body)\nC) 感情 (emotion)"
                    ),
                    "ja": (
                        "壁:\n水 → ?\n火 → ?\n木 → ?\n\n"
                        "質問:\n共通のカテゴリは？\n\n"
                        "選択肢:\nA) 自然\nB) 人体\nC) 感情"
                    ),
                },
                "correct_answer": {"uz": "A", "en": "A", "ja": "A"},
            },
            {
                "room_order": 2,
                "order": 2,
                "puzzle_type": "logic",
                "points": 25,
                "title": {
                    "uz": "Radikal asosida",
                    "en": "By Radical",
                    "ja": "部首ベース",
                },
                "description": {
                    "uz": "Kanji tuzilishiga qarab javob toping.",
                    "en": "Find the answer by kanji structure.",
                    "ja": "漢字の構造から答えを探す。",
                },
                "question": {
                    "uz": (
                        "Devor:\n"
                        "休 = 人 + 木\n"
                        "体 = 人 + 本\n"
                        "信 = 人 + 言\n\n"
                        "Pastda yozilgan:\n"
                        "人 + 心 = ?\n\n"
                        "Variantlar:\nA) 忘\nB) 念\nC) 息"
                    ),
                    "en": (
                        "On the wall:\n"
                        "休 = 人 + 木\n"
                        "体 = 人 + 本\n"
                        "信 = 人 + 言\n\n"
                        "Below:\n"
                        "人 + 心 = ?\n\n"
                        "Options:\nA) 忘\nB) 念\nC) 息"
                    ),
                    "ja": (
                        "壁:\n"
                        "休 = 人 + 木\n"
                        "体 = 人 + 本\n"
                        "信 = 人 + 言\n\n"
                        "下:\n"
                        "人 + 心 = ?\n\n"
                        "選択肢:\nA) 忘\nB) 念\nC) 息"
                    ),
                },
                "correct_answer": {"uz": "C", "en": "C", "ja": "C"},
            },
            {
                "room_order": 2,
                "order": 3,
                "puzzle_type": "logic",
                "points": 25,
                "title": {
                    "uz": "Ma'no zanjiri",
                    "en": "Meaning Chain",
                    "ja": "意味の連鎖",
                },
                "description": {
                    "uz": "Ma'no bo'yicha keyingi kanjini toping.",
                    "en": "Find the next kanji by meaning chain.",
                    "ja": "意味の流れで次の漢字を選ぶ。",
                },
                "question": {
                    "uz": (
                        "Kanji:\n生 → 学 → 校 → ?\n\n"
                        "Qoidasi: ma'no bo‘yicha hayot zanjiri\n\n"
                        "Variantlar:\nA) 友\nB) 先\nC) 試"
                    ),
                    "en": (
                        "Kanji:\n生 → 学 → 校 → ?\n\n"
                        "Rule: meaning chain of life\n\n"
                        "Options:\nA) 友\nB) 先\nC) 試"
                    ),
                    "ja": (
                        "漢字:\n生 → 学 → 校 → ?\n\n"
                        "ルール: 意味の連鎖\n\n"
                        "選択肢:\nA) 友\nB) 先\nC) 試"
                    ),
                },
                "correct_answer": {"uz": "C", "en": "C", "ja": "C"},
            },
            {
                "room_order": 3,
                "order": 1,
                "puzzle_type": "math",
                "points": 20,
                "title": {
                    "uz": "Operator va mantiq",
                    "en": "Operators and Logic",
                    "ja": "演算と論理",
                },
                "description": {
                    "uz": "Formulani hisoblab parolni toping.",
                    "en": "Calculate the formula to find the password.",
                    "ja": "式を計算してパスワードを求めよ。",
                },
                "question": {
                    "uz": (
                        "Ekranda:\nlet x = 2;\nlet y = 3;\nlet z = 4;\n\n"
                        "Password = x + y * z ** 2 - x * y\n\n"
                        "Variantlar:\nA) 42\nB) 44\nC) 46"
                    ),
                    "en": (
                        "On screen:\nlet x = 2;\nlet y = 3;\nlet z = 4;\n\n"
                        "Password = x + y * z ** 2 - x * y\n\n"
                        "Options:\nA) 42\nB) 44\nC) 46"
                    ),
                    "ja": (
                        "画面:\nlet x = 2;\nlet y = 3;\nlet z = 4;\n\n"
                        "Password = x + y * z ** 2 - x * y\n\n"
                        "選択肢:\nA) 42\nB) 44\nC) 46"
                    ),
                },
                "correct_answer": {"uz": "B", "en": "B", "ja": "B"},
            },
            {
                "room_order": 3,
                "order": 2,
                "puzzle_type": "logic",
                "points": 20,
                "title": {
                    "uz": "Murakkab ketma-ketlik",
                    "en": "Complex Sequence",
                    "ja": "複雑な数列",
                },
                "description": {
                    "uz": "Ketma-ketlik qoidasi bo'yicha toping.",
                    "en": "Find the next number by sequence rule.",
                    "ja": "数列の規則から次を答えよ。",
                },
                "question": {
                    "uz": (
                        "3 → 6 → 12 → 24 → 48 → ?\n\n"
                        "Variantlar:\nA) 72\nB) 96\nC) 84"
                    ),
                    "en": (
                        "3 → 6 → 12 → 24 → 48 → ?\n\n"
                        "Options:\nA) 72\nB) 96\nC) 84"
                    ),
                    "ja": (
                        "3 → 6 → 12 → 24 → 48 → ?\n\n"
                        "選択肢:\nA) 72\nB) 96\nC) 84"
                    ),
                },
                "correct_answer": {"uz": "B", "en": "B", "ja": "B"},
            },
            {
                "room_order": 3,
                "order": 3,
                "puzzle_type": "logic",
                "points": 20,
                "title": {
                    "uz": "Kod ishlashi",
                    "en": "Code Execution",
                    "ja": "コード実行",
                },
                "description": {
                    "uz": "Kod natijasini toping.",
                    "en": "Find the result of the code.",
                    "ja": "コードの結果を答えよ。",
                },
                "question": {
                    "uz": (
                        "let x = 1;\n\n"
                        "for (let i = 1; i <= 4; i++) {\n"
                        "  x = x + i;\n"
                        "}\n\n"
                        "Variantlar:\nA) 10\nB) 11\nC) 15"
                    ),
                    "en": (
                        "let x = 1;\n\n"
                        "for (let i = 1; i <= 4; i++) {\n"
                        "  x = x + i;\n"
                        "}\n\n"
                        "Options:\nA) 10\nB) 11\nC) 15"
                    ),
                    "ja": (
                        "let x = 1;\n\n"
                        "for (let i = 1; i <= 4; i++) {\n"
                        "  x = x + i;\n"
                        "}\n\n"
                        "選択肢:\nA) 10\nB) 11\nC) 15"
                    ),
                },
                "correct_answer": {"uz": "B", "en": "B", "ja": "B"},
            },
            {
                "room_order": 4,
                "order": 1,
                "puzzle_type": "logic",
                "points": 15,
                "title": {
                    "uz": "JS massivi",
                    "en": "JS Array",
                    "ja": "JS配列",
                },
                "description": {
                    "uz": "Massivning natijasini toping.",
                    "en": "Find the result of the array.",
                    "ja": "配列の結果を答えよ。",
                },
                "question": {
                    "uz": (
                        "let a = [1,2,3];\n"
                        "a.length = 1;\n"
                        "console.log(a[1]);\n\n"
                        "Variantlar:\nA) 2\nB) undefined\nC) error"
                    ),
                    "en": (
                        "let a = [1,2,3];\n"
                        "a.length = 1;\n"
                        "console.log(a[1]);\n\n"
                        "Options:\nA) 2\nB) undefined\nC) error"
                    ),
                    "ja": (
                        "let a = [1,2,3];\n"
                        "a.length = 1;\n"
                        "console.log(a[1]);\n\n"
                        "選択肢:\nA) 2\nB) undefined\nC) error"
                    ),
                },
                "correct_answer": {"uz": "B", "en": "B", "ja": "B"},
            },
            {
                "room_order": 4,
                "order": 2,
                "puzzle_type": "logic",
                "points": 15,
                "title": {
                    "uz": "Flex markaz",
                    "en": "Flex Center",
                    "ja": "Flex中央寄せ",
                },
                "description": {
                    "uz": "Element nima uchun markazga kelmayapti?",
                    "en": "Why doesn't the element center?",
                    "ja": "なぜ中央に来ない？",
                },
                "question": {
                    "uz": (
                        "Element markazga kelmayapti:\n\n"
                        ".parent {\n  display: flex;\n  justify-content: center;\n  align-items: center;\n}\n\n"
                        ".child {\n  margin: auto;\n}\n\n"
                        "Muammo?\nA) Parent’da height yo‘q\nB) margin noto‘g‘ri\nC) flex ishlamaydi"
                    ),
                    "en": (
                        "Element doesn't center:\n\n"
                        ".parent {\n  display: flex;\n  justify-content: center;\n  align-items: center;\n}\n\n"
                        ".child {\n  margin: auto;\n}\n\n"
                        "Problem?\nA) Parent has no height\nB) margin is wrong\nC) flex doesn't work"
                    ),
                    "ja": (
                        "要素が中央に来ない:\n\n"
                        ".parent {\n  display: flex;\n  justify-content: center;\n  align-items: center;\n}\n\n"
                        ".child {\n  margin: auto;\n}\n\n"
                        "原因は？\nA) 親に高さがない\nB) marginが間違い\nC) flexが動かない"
                    ),
                },
                "correct_answer": {"uz": "A", "en": "A", "ja": "A"},
            },
            {
                "room_order": 4,
                "order": 3,
                "puzzle_type": "logic",
                "points": 15,
                "title": {
                    "uz": "JS type",
                    "en": "JS Type",
                    "ja": "JS型",
                },
                "description": {
                    "uz": "Natijani toping.",
                    "en": "Find the result.",
                    "ja": "結果を答えよ。",
                },
                "question": {
                    "uz": "console.log([] + {});\n\nVariantlar:\nA) {}\nB) [object Object]\nC) error",
                    "en": "console.log([] + {});\n\nOptions:\nA) {}\nB) [object Object]\nC) error",
                    "ja": "console.log([] + {});\n\n選択肢:\nA) {}\nB) [object Object]\nC) error",
                },
                "correct_answer": {"uz": "B", "en": "B", "ja": "B"},
            },
            {
                "room_order": 5,
                "order": 1,
                "puzzle_type": "logic",
                "points": 20,
                "title": {
                    "uz": "Subnet hisob",
                    "en": "Subnet Calculation",
                    "ja": "サブネット計算",
                },
                "description": {
                    "uz": "Network addressni toping.",
                    "en": "Find the network address.",
                    "ja": "ネットワークアドレスを求めよ。",
                },
                "question": {
                    "uz": (
                        "IP: 192.168.1.130\n"
                        "Mask: 255.255.255.128\n\n"
                        "Subnetlar:\n0–127\n128–255\n\n"
                        "Savol: Network address?\n"
                        "A) 192.168.1.0\nB) 192.168.1.128\nC) 192.168.1.255"
                    ),
                    "en": (
                        "IP: 192.168.1.130\n"
                        "Mask: 255.255.255.128\n\n"
                        "Subnets:\n0–127\n128–255\n\n"
                        "Question: Network address?\n"
                        "A) 192.168.1.0\nB) 192.168.1.128\nC) 192.168.1.255"
                    ),
                    "ja": (
                        "IP: 192.168.1.130\n"
                        "Mask: 255.255.255.128\n\n"
                        "サブネット:\n0–127\n128–255\n\n"
                        "質問: ネットワークアドレスは？\n"
                        "A) 192.168.1.0\nB) 192.168.1.128\nC) 192.168.1.255"
                    ),
                },
                "correct_answer": {"uz": "B", "en": "B", "ja": "B"},
            },
            {
                "room_order": 5,
                "order": 2,
                "puzzle_type": "logic",
                "points": 20,
                "title": {
                    "uz": "Port tahlili",
                    "en": "Port Analysis",
                    "ja": "ポート分析",
                },
                "description": {
                    "uz": "Remote terminal orqali kirish portini toping.",
                    "en": "Find the port used for remote terminal access.",
                    "ja": "リモート端末で使うポートを選べ。",
                },
                "question": {
                    "uz": (
                        "Hacker quyidagi portdan kirgan:\n"
                        "A) 22\nB) 80\nC) 443\n\n"
                        "Ma'lumot: “Remote terminal orqali kirilgan”"
                    ),
                    "en": (
                        "Hacker entered through this port:\n"
                        "A) 22\nB) 80\nC) 443\n\n"
                        "Info: 'Remote terminal access'"
                    ),
                    "ja": (
                        "ハッカーは次のポートから侵入:\n"
                        "A) 22\nB) 80\nC) 443\n\n"
                        "情報: 「リモート端末アクセス」"
                    ),
                },
                "correct_answer": {"uz": "A", "en": "A", "ja": "A"},
            },
        ]

        with transaction.atomic():
            Puzzle.objects.all().delete()
            Room.objects.all().delete()

            created_rooms = {}
            for room in rooms_data:
                obj = Room.objects.create(
                    order=room["order"],
                    title=room["title"]["uz"],
                    description=room["description"]["uz"],
                    is_active=True,
                )
                for lang in ("uz", "en", "ja"):
                    setattr(obj, f"title_{lang}", room["title"][lang])
                    setattr(obj, f"description_{lang}", room["description"][lang])
                obj.save()
                created_rooms[room["order"]] = obj

            for puzzle in puzzles_data:
                room = created_rooms[puzzle["room_order"]]
                obj = Puzzle.objects.create(
                    room=room,
                    title=puzzle["title"]["uz"],
                    description=puzzle["description"]["uz"],
                    puzzle_type=puzzle["puzzle_type"],
                    question=puzzle["question"]["uz"],
                    correct_answer=puzzle["correct_answer"]["uz"],
                    points=puzzle["points"],
                    order=puzzle["order"],
                    hint="",
                )
                for lang in ("uz", "en", "ja"):
                    setattr(obj, f"title_{lang}", puzzle["title"][lang])
                    setattr(obj, f"description_{lang}", puzzle["description"][lang])
                    setattr(obj, f"question_{lang}", puzzle["question"][lang])
                    setattr(obj, f"correct_answer_{lang}", puzzle["correct_answer"][lang])
                obj.save()

        self.stdout.write(self.style.SUCCESS("Rooms and puzzles seeded successfully."))
