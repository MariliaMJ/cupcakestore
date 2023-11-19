# Generated by Django 4.2.6 on 2023-11-15 19:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("app", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="customer",
            name="email",
        ),
        migrations.RemoveField(
            model_name="customer",
            name="name",
        ),
        migrations.RemoveField(
            model_name="customer",
            name="username",
        ),
        migrations.AddField(
            model_name="customer",
            name="user",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]