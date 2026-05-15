# -*- coding: utf-8 -*-
from dataclasses import dataclass, field
import datetime, pickle
from typing import List
from flask import request


# ─── Models ──────────────────────────────────────────────────────────────────

@dataclass
class Quest:
    id: int
    name: str
    duration: int
    min_players: int
    max_players: int
    description: str = ""
    price: int = 5000
    difficulty: int = 3
    fear: int = 3
    image: str = ""
    age_limit: int = 18


all_quests: List[Quest] = [
    Quest(1, "Слепые", 90, 2, 8,
          "Несколько лет назад в пригороде исчезали люди. Ни следов, ни требований выкупа. "
          "Только одна деталь — перед исчезновением каждый получал конверт с одним словом: «Прозрей».\n\n"
          "Полиция нашла убежище секты в старом бомбоубежище. Но внутри не было никого. Только стены, "
          "исписанные именами, и комнаты, похожие на кельи. В каждой — личное дело человека, который здесь жил… и умер.\n\n"
          "Секта называла себя «Слепые». Они верили, что истина открывается только тем, кто потерял зрение. Буквально.\n\n"
          "Жертвам завязывали глаза в последний день. Говорили: «Теперь ты видишь». А потом — тишина.\n\n"
          "Вы пришли сюда, чтобы найти того, кто пропал недавно. Или чтобы понять, что случилось с теми, кто вошёл до вас. "
          "Но двери захлопнулись. И свет погас. Вы не одни. Они всё ещё здесь. Они ждут, когда вы прозреете.",
          5000, 4, 3, "quest_1.jpg", 18),
    Quest(2, "Живая коллекция", 90, 4, 6,
          "Ты открываешь глаза. Стекло. Холод. Рядом — лица тех, кто был с тобой.\n\n"
          "Вы видите друг друга. Вы слышите друг друга. Но клетки не дают коснуться. Где‑то за стеной — шаги. Медленные. Тяжёлые.\n\n"
          "Здесь уже были другие. Их вещи до сих пор разбросаны по комнатам. Их имена выцарапаны на стенах. "
          "Их голоса всё ещё звучат в старых записях. Он собирает не мёртвых. Он собирает живых. "
          "Каждому — своё место. Каждому — своя история. И ты уже в ней. "
          "Вы не знаете, кто следующий. Не знаете, сколько вас осталось.\n\n"
          "Знаете только одно: Если потеряешь друг друга из виду — можете не встретиться больше никогда.",
          6000, 3, 4, "quest_2.jpg", 16),
    Quest(3, "Карантин", 60, 2, 8,
          "Выжившие говорят: если успеешь добраться до старой больницы, есть шанс.\n\n"
          "Под ней — военный бункер. Там ещё держат оборону. Там есть связь. Там можно остаться.\n\n"
          "Но больница встретила вас тишиной. Коридоры завалены каталками. В палатах — спёкшиеся простыни. "
          "В морге — свет всё ещё горит. И кто-то забыл закрыть холодильники. "
          "Вы не знаете, кто ещё бродит по этим этажам. "
          "Знаете только: вход в бункер — где‑то в подвале. А подвал — это морг. "
          "Операционные. Комнаты, где не успели вывезти тела.\n\n"
          "Здесь до сих пор пахнет формалином. Здесь до сих пор слышны шаги за стеной. "
          "Здесь до сих пор есть те, кто не хочет, чтобы вы ушли.\n\n"
          "У вас нет оружия. Только фонари и друг друг. "
          "Если потеряетесь в этих коридорах — можете не найтись.",
          4500, 2, 5, "quest_3.jpg", 14),
]


@dataclass
class User:
    id: int = 0
    first_name: str = ""
    second_name: str = ""
    phone: str = ""
    password: str = ""
    confirm_password: str = ""
    email: str = ""
    time: datetime.datetime = field(default_factory=datetime.datetime.now)

    def validate_name(self, value):
        if not value or len(value) < 2:
            return "Имя должно содержать минимум 2 символа"
        if any(c.isdigit() for c in value):
            return "Имя не должно содержать цифры"
        if any(c in "!@#$%^&*()_+=[]{}|;':,./<>?~" for c in value):
            return "Имя не должно содержать спецсимволы"
        return None

    def validate_second_name(self, value):
        if not value or len(value) < 2:
            return "Фамилия должна содержать минимум 2 символа"
        if any(c.isdigit() for c in value):
            return "Фамилия не должна содержать цифры"
        if any(c in "!@#$%^&*()_+=[]{}|;':,./<>?~" for c in value):
            return "Фамилия не должна содержать спецсимволы"
        return None

    def validate_phone(self, value):
        if not value:
            return "Номер телефона обязателен"
        if any(c in "!@#$%^&*()_-+=[]{}|;':,./<>?~" for c in value):
            return "Номер телефона не должен содержать спецсимволы"
        if not value.isdigit():
            return "Номер телефона должен содержать только цифры"
        if value[0] != '7':
            return "Номер телефона должен начинаться с 7"
        if len(value) != 11:
            return "Номер телефона должен содержать ровно 11 цифр"
        return None

    def validate_password(self, value):
        if not value:
            return "Пароль обязателен"
        if len(value) < 8:
            return "Пароль должен содержать не менее 8 символов"
        if len(value) > 16:
            return "Пароль должен содержать не более 16 символов"
        if not any(c.isalpha() and c.isascii() for c in value):
            return "Пароль должен содержать хотя бы одну латинскую букву"
        return None

    def validate_email(self, value):
        if not value:
            return None
        if "@" not in value or "." not in value or len(value) < 5:
            return "Некорректный формат email"
        return None


@dataclass
class Booking:
    id: int = 0
    user_id: int = 0
    quest_id: int = 0
    slot: str = ""
    player_count: int = 1


@dataclass
class Review:
    id: int = 0
    user_id: int = 0
    quest_id: int = 0
    overall: int = 5
    acting: int = 5
    logic: int = 5
    text: str = ""


# ─── Storage ──────────────────────────────────────────────────────────────────

class PickleStorage:
    def __init__(self, book, filepath='quest_data.dat'):
        self.book = book
        self.filepath = filepath

    def Store(self):
        with open(self.filepath, 'wb') as f:
            pickle.dump({
                'maxID': self.book.maxID,
                'items': self.book.items,
                'bookings': self.book.bookings,
                'reviews': self.book.reviews,
                'available_slots': self.book.available_slots,
                'maxBookingID': self.book.maxBookingID,
                'maxReviewID': self.book.maxReviewID,
            }, f)

    def Load(self):
        with open(self.filepath, 'rb') as f:
            data = pickle.load(f)
        self.book.maxID = data.get('maxID', 0)
        self.book.items = data.get('items', {})
        self.book.bookings = data.get('bookings', [])
        self.book.reviews = data.get('reviews', [])
        self.book.available_slots = data.get('available_slots', self.book._default_slots())
        self.book.maxBookingID = data.get('maxBookingID', 0)
        self.book.maxReviewID = data.get('maxReviewID', 0)


# ─── Book ─────────────────────────────────────────────────────────────────────

class Book:
    def __init__(self):
        self.items = {}
        self.bookings = []
        self.reviews = []
        self.available_slots = self._default_slots()
        self.maxID = 0
        self.maxBookingID = 0
        self.maxReviewID = 0
        self.storage = PickleStorage(self)
        try:
            self.storage.Load()
        except Exception:
            pass

    def _default_slots(self):
        return [
            "19.06.2025 15:30", "19.06.2025 17:00", "19.06.2025 20:00",
            "20.06.2025 15:30", "20.06.2025 17:00", "20.06.2025 20:00",
            "21.06.2025 15:30", "21.06.2025 17:00", "21.06.2025 20:00",
            "22.06.2025 15:30", "22.06.2025 17:00", "22.06.2025 20:00",
        ]

    # ── Users ──────────────────────────────────────────────────────────────

    def GetUser(self, user_id):
        return self.items.get(user_id)

    def Login(self, phone, password):
        normalized = ("+" + phone) if not phone.startswith("+") else phone
        for user in self.items.values():
            if user.phone == normalized and user.password == password:
                return user
        return None

    def Register(self, form):
        errors = []
        user = User()

        err = user.validate_name(form.get('first_name', ''))
        if err: errors.append(err)
        else: user.first_name = form['first_name']

        err = user.validate_second_name(form.get('second_name', ''))
        if err: errors.append(err)
        else: user.second_name = form['second_name']

        phone = form.get('phone', '')
        err = user.validate_phone(phone)
        if err:
            errors.append(err)
        else:
            user.phone = "+" + phone
            if any(u.phone == user.phone for u in self.items.values()):
                errors.append("Пользователь с таким телефоном уже существует")

        err = user.validate_email(form.get('email', ''))
        if err: errors.append(err)
        else: user.email = form.get('email', '')

        password = form.get('password', '')
        err = user.validate_password(password)
        if err: errors.append(err)
        else: user.password = password

        if form.get('confirm_password', '') != password:
            errors.append("Пароли не совпадают")
        else:
            user.confirm_password = password

        if not errors:
            self.maxID += 1
            user.id = self.maxID
            self.items[user.id] = user
            self.storage.Store()

        return errors

    def UpdateProfile(self, user, form):
        errors = []
        if form.get('first_name'):
            err = user.validate_name(form['first_name'])
            if err: errors.append(err)
            else: user.first_name = form['first_name']
        if form.get('second_name'):
            err = user.validate_second_name(form['second_name'])
            if err: errors.append(err)
            else: user.second_name = form['second_name']
        err = user.validate_email(form.get('email', ''))
        if err: errors.append(err)
        else: user.email = form.get('email', '')
        if form.get('password'):
            err = user.validate_password(form['password'])
            if err: errors.append(err)
            elif form.get('confirm_password') != form['password']:
                errors.append("Пароли не совпадают")
            else:
                user.password = form['password']
        if not errors:
            self.storage.Store()
        return errors

    def ResetPassword(self, form):
        errors = []
        phone = form.get('phone', '')
        err = User().validate_phone(phone)
        if err:
            errors.append(err)
            return errors
        normalized = "+" + phone
        user = next((u for u in self.items.values() if u.phone == normalized), None)
        if not user:
            errors.append("Пользователь с таким номером не найден")
            return errors
        password = form.get('password', '')
        err = User().validate_password(password)
        if err:
            errors.append(err)
        elif form.get('confirm_password') != password:
            errors.append("Пароли не совпадают")
        if not errors:
            user.password = password
            self.storage.Store()
        return errors

    # ── Quests ─────────────────────────────────────────────────────────────

    def GetQuests(self):
        return all_quests

    def GetQuest(self, quest_id):
        return next((q for q in all_quests if q.id == quest_id), None)

    def GetSlotsGrouped(self):
        from collections import OrderedDict
        grouped = OrderedDict()
        for slot in sorted(self.available_slots):
            date, time = slot.split(' ')
            grouped.setdefault(date, []).append(time)
        return grouped

    def QuestsMap(self):
        return {q.id: q for q in all_quests}

    # ── Bookings ───────────────────────────────────────────────────────────

    def GetUserBookings(self, user_id):
        return [b for b in self.bookings if b.user_id == user_id]

    def GetBooking(self, booking_id):
        return next((b for b in self.bookings if b.id == booking_id), None)

    def AddBooking(self, user_id, form):
        errors = []
        try:
            quest_id = int(form.get('quest_id', 0))
        except ValueError:
            return ["Некорректный квест"]
        quest = self.GetQuest(quest_id)
        if not quest:
            return ["Квест не найден"]
        slot = form.get('slot', '')
        if slot not in self.available_slots:
            return ["Выбранный слот недоступен"]
        try:
            player_count = int(form.get('player_count', 0))
        except ValueError:
            return ["Некорректное количество игроков"]
        if not (quest.min_players <= player_count <= quest.max_players):
            errors.append(f"Количество игроков: от {quest.min_players} до {quest.max_players}")
        if not errors:
            self.maxBookingID += 1
            self.bookings.append(Booking(
                id=self.maxBookingID, user_id=user_id,
                quest_id=quest_id, slot=slot, player_count=player_count,
            ))
            self.available_slots.remove(slot)
            self.storage.Store()
        return errors

    def UpdateBooking(self, user_id, booking_id, form):
        booking = self.GetBooking(booking_id)
        if not booking or booking.user_id != user_id:
            return ["Бронирование не найдено"]
        quest = self.GetQuest(booking.quest_id)
        try:
            player_count = int(form.get('player_count', 0))
        except ValueError:
            return ["Некорректное количество игроков"]
        if not (quest.min_players <= player_count <= quest.max_players):
            return [f"Количество игроков: от {quest.min_players} до {quest.max_players}"]
        booking.player_count = player_count
        self.storage.Store()
        return []

    def DeleteBooking(self, user_id, booking_id):
        booking = self.GetBooking(booking_id)
        if booking and booking.user_id == user_id:
            self.available_slots.append(booking.slot)
            self.available_slots.sort()
            self.bookings.remove(booking)
            self.storage.Store()

    # ── Reviews ────────────────────────────────────────────────────────────

    def GetUserReviews(self, user_id):
        return [r for r in self.reviews if r.user_id == user_id]

    def GetReview(self, review_id):
        return next((r for r in self.reviews if r.id == review_id), None)

    def AddReview(self, user_id, form):
        errors = []
        try:
            quest_id = int(form.get('quest_id', 0))
        except ValueError:
            return ["Некорректный квест"]
        if not self.GetQuest(quest_id):
            return ["Квест не найден"]
        if any(r.user_id == user_id and r.quest_id == quest_id for r in self.reviews):
            return ["Вы уже оставляли отзыв на этот квест"]
        text = form.get('text', '')
        if len(text) < 10:
            errors.append("Отзыв слишком короткий (минимум 10 символов)")
        elif len(text) > 500:
            errors.append("Отзыв слишком длинный (максимум 500 символов)")
        try:
            overall = int(form.get('overall', 0))
            acting  = int(form.get('acting', 0))
            logic   = int(form.get('logic', 0))
            if not all(1 <= v <= 5 for v in [overall, acting, logic]):
                errors.append("Оценки должны быть от 1 до 5")
        except ValueError:
            errors.append("Некорректные оценки")
            overall = acting = logic = 5
        if not errors:
            self.maxReviewID += 1
            self.reviews.append(Review(
                id=self.maxReviewID, user_id=user_id, quest_id=quest_id,
                overall=overall, acting=acting, logic=logic, text=text,
            ))
            self.storage.Store()
        return errors

    def UpdateReview(self, user_id, review_id, form):
        review = self.GetReview(review_id)
        if not review or review.user_id != user_id:
            return ["Отзыв не найден"]
        text = form.get('text', '')
        if len(text) < 10:
            return ["Отзыв слишком короткий (минимум 10 символов)"]
        if len(text) > 500:
            return ["Отзыв слишком длинный (максимум 500 символов)"]
        try:
            overall = int(form.get('overall', review.overall))
            acting  = int(form.get('acting',  review.acting))
            logic   = int(form.get('logic',   review.logic))
            if not all(1 <= v <= 5 for v in [overall, acting, logic]):
                return ["Оценки должны быть от 1 до 5"]
        except ValueError:
            return ["Некорректные оценки"]
        review.text    = text
        review.overall = overall
        review.acting  = acting
        review.logic   = logic
        self.storage.Store()
        return []

    def DeleteReview(self, user_id, review_id):
        review = self.GetReview(review_id)
        if review and review.user_id == user_id:
            self.reviews.remove(review)
            self.storage.Store()
