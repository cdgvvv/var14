from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Quest(models.Model):
    title = models.CharField("Название", max_length=150)
    description = models.TextField("Описание")
    genre = models.CharField("Жанр", max_length=50)
    fear_level = models.IntegerField(
        "Уровень страха",
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=3,
    )
    difficulty = models.IntegerField(
        "Сложность",
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=3,
    )
    duration_minutes = models.IntegerField("Длительность (мин)", default=60)
    max_players = models.IntegerField("Макс. игроков", default=6)
    price = models.DecimalField("Цена", max_digits=8, decimal_places=2)
    image = models.ImageField("Постер", upload_to="quests/", blank=True, null=True)

    class Meta:
        verbose_name = "Квест"
        verbose_name_plural = "Квесты"
        ordering = ["id"]

    def __str__(self):
        return self.title


class Session(models.Model):
    quest = models.ForeignKey(Quest, on_delete=models.CASCADE, related_name="sessions", verbose_name="Квест")
    date = models.DateField("Дата")
    time = models.TimeField("Время")
    is_available = models.BooleanField("Свободно", default=True)

    class Meta:
        verbose_name = "Сеанс"
        verbose_name_plural = "Сеансы"
        ordering = ["date", "time"]

    def __str__(self):
        return f"{self.quest.title} - {self.date} {self.time.strftime('%H:%M')}"


class Booking(models.Model):
    STATUS_CHOICES = [
        ("confirmed", "Подтверждена"),
        ("pending", "Ожидает подтверждения"),
        ("cancelled", "Отменена"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="bookings",
        verbose_name="Пользователь",
    )
    quest = models.ForeignKey(Quest, on_delete=models.CASCADE, related_name="bookings", verbose_name="Квест")
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name="bookings", verbose_name="Сеанс")
    customer_name = models.CharField("Имя контактного лица", max_length=100, default="Гость")
    customer_phone = models.CharField("Телефон", max_length=25, default="+7 (999) 000-00-00")
    customer_email = models.EmailField("Email", blank=True, default="")
    players_count = models.IntegerField("Количество игроков", validators=[MinValueValidator(2), MaxValueValidator(12)])
    add_actor = models.BooleanField("Доп. аниматор (+500₽)", default=False)
    total_price = models.DecimalField("Итоговая стоимость", max_digits=9, decimal_places=2)
    status = models.CharField("Статус", max_length=20, choices=STATUS_CHOICES, default="confirmed")
    created_at = models.DateTimeField("Создано", auto_now_add=True)

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Бронь #{self.id}: {self.quest.title} ({self.session.date} {self.session.time.strftime('%H:%M')})"
