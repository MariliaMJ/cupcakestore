# Generated by Django 4.2.6 on 2023-10-25 01:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0004_cupcake_nome"),
    ]

    operations = [
        migrations.AddField(
            model_name="cupcake",
            name="estoque",
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]