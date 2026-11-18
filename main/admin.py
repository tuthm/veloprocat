from django.contrib import admin

from .models import BikeUnit, Booking, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")


@admin.register(BikeUnit)
class BikeUnitAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price_per_day", "status")
    list_filter = ("category", "status")


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("pk", "user", "unit", "start_date", "end_date", "phone", "email", "total", "status")
    list_filter = ("status",)
