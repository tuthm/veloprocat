
from datetime import date, timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import BikeUnit, Booking, Category


class BookingSecurityTests(TestCase):

    def test_cannot_replace_bike_id(self):
        user = User.objects.create_user(
            username="test_user",
            password="TestPassword123!"
        )

        category = Category.objects.create(
            name="Тестовая категория",
            slug="test-category"
        )

        bike1 = BikeUnit.objects.create(
            name="Велосипед 1",
            category=category,
            price_per_day=750
        )

        bike2 = BikeUnit.objects.create(
            name="Велосипед 2",
            category=category,
            price_per_day=900
        )

        self.client.force_login(user)

        start = date.today() + timedelta(days=3)
        end = start + timedelta(days=2)

        response = self.client.post(
            reverse("main:unit_detail", args=[bike1.pk]),
            {
                "unit": bike2.pk,
                "start_date": start.isoformat(),
                "end_date": end.isoformat(),
                "phone": "+79991234567",
                "email": "test@example.com",
            }
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Booking.objects.count(), 1)

        booking = Booking.objects.get()

        self.assertEqual(booking.unit_id, bike1.pk)
        self.assertEqual(booking.total, 1500)
        self.assertEqual(booking.status, Booking.STATUS_NEW)
