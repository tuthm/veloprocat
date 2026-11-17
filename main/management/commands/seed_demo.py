import random
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from main.models import Category, BikeUnit, Booking

CATS = [
    ("city", "Городские", "Для ровных дорог и прогулок по центру."),
    ("mountain", "Горные", "Крепкие рамы и амортизация для леса и грунтов."),
    ("electric", "Электровелосипеды", "До 60 км на одном заряде, assistance при подъёме."),
]
NAMES = [
    ("city", "Stels Navigator 300", 700, "Городской"),
    ("city", "Forward Sporting", 700, "Городской"),
    ("city", "Stels Navigator 500", 750, "Городской"),
    ("city", "Forward Charity 4.1", 750, "Городской"),
    ("city", "Stels Navigator 700", 800, "Городской"),
    ("city", "Forward Cufo 1.0", 800, "Городской"),
    ("city", "Stels Navigator 900", 850, "Городской"),
    ("city", "Forward City 2.2", 850, "Городской"),
    ("city", "Stels Navigator 1000", 900, "Городской"),
    ("city", "Forward Delia 8.1", 900, "Городской"),
    ("mountain", "Merida Big Nine 20", 900, "Горный"),
    ("mountain", "Merida Big Nine 40", 950, "Горный"),
    ("mountain", "Merida Big Seven 15", 1000, "Горный"),
    ("mountain", "Giant Talon 3", 1000, "Горный"),
    ("mountain", "Giant Talon 2", 1050, "Горный"),
    ("mountain", "Merida Big Nine 60", 1100, "Горный"),
    ("mountain", "Giant Talon 1", 1100, "Горный"),
    ("mountain", "Merida One-Twenty 7.10", 1150, "Горный"),
    ("mountain", "Giant Fathom 2", 1150, "Горный"),
    ("mountain", "Merida One-Twenty 7.20", 1200, "Горный"),
    ("electric", "Volteco Metropol", 1200, "Электро"),
    ("electric", "Volteco Courier", 1300, "Электро"),
    ("electric", "X-mob X250", 1300, "Электро"),
    ("electric", "Volteco Meridian", 1400, "Электро"),
    ("electric", "X-mob X350", 1400, "Электро"),
    ("electric", "Volteco Meridian+", 1500, "Электро"),
    ("electric", "X-mob X500", 1500, "Электро"),
    ("electric", "Volteco Courier+", 1600, "Электро"),
    ("electric", "X-mob X600", 1600, "Электро"),
    ("electric", "Volteco Meridian Max", 1700, "Электро"),
    ("electric", "X-mob X700", 1700, "Электро"),
]

class Command(BaseCommand):
    help = "Наполняет базу демо-данными: 3 категории, 31 единица, демо-клиент с бронями"

    def handle(self, *args, **options):
        if BikeUnit.objects.exists():
            self.stdout.write("База уже заполнена — seed пропущен.")
            return
        cats = {slug: Category.objects.create(name=name, slug=slug, description=desc)
                for slug, name, desc in CATS}
        popular_slugs = {"Stels Navigator 300", "Merida Big Nine 20", "Volteco Metropol", "Forward Sporting"}
        statuses = {12: "rented", 17: "repair", 25: "rented"}
        for i, (slug, name, price, _desc) in enumerate(NAMES, start=1):
            BikeUnit.objects.create(
                name=name, category=cats[slug], price_per_day=price,
                status=statuses.get(i, "free"), is_popular=name in popular_slugs,
                photo=f"units/unit{i:02d}.png",
                description=f"{name}: {_desc.lower()} велосипед, обслужен, готовы к выдаче.",
            )
        demo, created = User.objects.get_or_create(username="demo")
        if created:
            demo.set_password("demo12345")
            demo.save()
        today = date.today()
        samples = [
            (today + timedelta(days=3), today + timedelta(days=6), "new", "Stels Navigator 300"),
            (today - timedelta(days=10), today - timedelta(days=7), "returned", "Merida Big Nine 20"),
            (today - timedelta(days=2), today + timedelta(days=2), "issued", "Volteco Metropol"),
        ]
        for start, end, status, unit_name in samples:
            unit = BikeUnit.objects.get(name=unit_name)
            total = (end - start).days * unit.price_per_day
            Booking.objects.create(user=demo, unit=unit, date_start=start,
                                   date_end=end, total_price=total, status=status)
        self.stdout.write(self.style.SUCCESS("Создано: 3 категории, 31 единица, клиент demo/demo12345, 3 брони."))
