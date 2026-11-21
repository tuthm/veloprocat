from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0002_booking_contact"),
    ]

    operations = [
        migrations.RenameField(
            model_name="booking",
            old_name="date_start",
            new_name="start_date",
        ),
        migrations.RenameField(
            model_name="booking",
            old_name="date_end",
            new_name="end_date",
        ),
        migrations.RenameField(
            model_name="booking",
            old_name="total_price",
            new_name="total",
        ),
    ]