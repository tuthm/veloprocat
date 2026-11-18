from decimal import Decimal

from django.conf import settings
from django.db import models


class Category(models.Model):
    name = models.CharField("Название", max_length=100)
    slug = models.SlugField("Слаг", unique=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]

    def __str__(self):
        return self.name


class BikeUnit(models.Model):
    STATUS_FREE = "free"
    STATUS_RENTED = "rented"
    STATUS_REPAIR = "repair"
    STATUS_CHOICES = [
        (STATUS_FREE, "Свободен"),
        (STATUS_RENTED, "В прокате"),
        (STATUS_REPAIR, "Требуется ремонт"),
    ]

    name = models.CharField("Модель", max_length=150)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="units",
        verbose_name="Категория",
    )
    price_per_day = models.DecimalField("Цена за сутки", max_digits=8, decimal_places=2)
    status = models.CharField("Статус", max_length=20, choices=STATUS_CHOICES, default=STATUS_FREE)
    photo = models.ImageField("Фото", upload_to="units/", blank=True, null=True)

    class Meta:
        verbose_name = "Единица проката"
        verbose_name_plural = "Единицы проката"
        ordering = ["name"]

    def __str__(self):
        return self.name

    @property
    def status_label(self):
        return self.get_status_display()


class Booking(models.Model):
    STATUS_NEW = "new"
    STATUS_ISSUED = "issued"
    STATUS_RETURNED = "returned"
    STATUS_CHOICES = [
        (STATUS_NEW, "Новая"),
        (STATUS_ISSUED, "Выдана"),
        (STATUS_RETURNED, "Возвращена"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bookings",
        verbose_name="Клиент",
    )
    unit = models.ForeignKey(
        BikeUnit,
        on_delete=models.CASCADE,
        related_name="bookings",
        verbose_name="Единица",
    )
    start_date = models.DateField("Начало проката")
    end_date = models.DateField("Конец проката")
    # --- Занятие 9: контакты клиента в брони ---
    phone = models.CharField("Телефон", max_length=12, default="")
    email = models.EmailField("Электронная почта", blank=True, default="")
    total = models.DecimalField("Итого", max_digits=10, decimal_places=2)
    status = models.CharField("Статус", max_length=20, choices=STATUS_CHOICES, default=STATUS_NEW)
    created_at = models.DateTimeField("Создана", auto_now_add=True)

    class Meta:
        verbose_name = "Бронь"
        verbose_name_plural = "Брони"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Бронь №{self.pk}: {self.unit} для {self.user}"
