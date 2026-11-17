from django.db import models
from django.conf import settings

class Category(models.Model):
    name = models.CharField("Название", max_length=50)
    slug = models.SlugField(unique=True)
    description = models.TextField("Описание", blank=True)

    def __str__(self):
        return self.name

class BikeUnit(models.Model):
    STATUS_FREE = "free"
    STATUS_RENTED = "rented"
    STATUS_REPAIR = "repair"
    STATUS_CHOICES = [(STATUS_FREE, "Свободен"), (STATUS_RENTED, "В прокате"), (STATUS_REPAIR, "Требуется ремонт")]

    name = models.CharField("Модель", max_length=60)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="units", verbose_name="Категория")
    price_per_day = models.PositiveIntegerField("Цена в сутки")
    status = models.CharField("Статус", max_length=10, choices=STATUS_CHOICES, default=STATUS_FREE)
    is_popular = models.BooleanField("Показывать на главной", default=False)
    photo = models.ImageField("Фото", upload_to="units/", blank=True)
    description = models.TextField("Описание", blank=True)
    created_at = models.DateTimeField("Добавлена", auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.category.name})"

class Booking(models.Model):
    STATUS_NEW = "new"
    STATUS_ISSUED = "issued"
    STATUS_RETURNED = "returned"
    STATUS_CANCELLED = "cancelled"
    STATUS_CHOICES = [(STATUS_NEW, "Новая"), (STATUS_ISSUED, "Выдана"), (STATUS_RETURNED, "Возвращена"), (STATUS_CANCELLED, "Отменена")]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookings", verbose_name="Клиент")
    unit = models.ForeignKey(BikeUnit, on_delete=models.CASCADE, related_name="bookings", verbose_name="Единица")
    date_start = models.DateField("Дата начала")
    date_end = models.DateField("Дата окончания")
    total_price = models.DecimalField("Итого", max_digits=8, decimal_places=2)
    status = models.CharField("Статус", max_length=10, choices=STATUS_CHOICES, default=STATUS_NEW)
    created_at = models.DateTimeField("Создана", auto_now_add=True)

    def __str__(self):
        return f"Бронь №{self.pk} — {self.unit.name}"
