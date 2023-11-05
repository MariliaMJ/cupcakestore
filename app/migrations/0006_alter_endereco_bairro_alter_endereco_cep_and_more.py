# Generated by Django 4.2.6 on 2023-11-03 19:59

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0005_cupcake_estoque"),
    ]

    operations = [
        migrations.AlterField(
            model_name="endereco",
            name="bairro",
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name="endereco",
            name="cep",
            field=models.CharField(max_length=9),
        ),
        migrations.AlterField(
            model_name="endereco",
            name="cidade",
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name="endereco",
            name="estado",
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name="endereco",
            name="rua",
            field=models.CharField(max_length=255),
        ),
    ]
