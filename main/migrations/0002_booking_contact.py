from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="booking",
            name="phone",
            field=models.CharField(default="", max_length=12, verbose_name="Телефон"),
        ),
        migrations.AddField(
            model_name="booking",
            name="email",
            field=models.EmailField(blank=True, default="", verbose_name="Электронная почта"),
        ),
    ]
