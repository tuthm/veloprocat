from django.contrib import admin
from .models import Category, BikeUnit, Booking

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")

@admin.register(BikeUnit)
class BikeUnitAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price_per_day", "status", "is_popular")
    list_filter = ("category", "status")
    search_fields = ("name",)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "unit", "date_start", "date_end", "total_price", "status")
    list_filter = ("status",)
