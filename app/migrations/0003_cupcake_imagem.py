# Generated by Django 4.2.6 on 2023-10-22 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0002_endereco_item_alter_cupcake_id_usuario_pedido_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="cupcake",
            name="imagem",
            field=models.URLField(
                default="https://www.receitasnestle.com.br/sites/default/files/srh_recipes/0fff5f03afb90bb990364a480f294cd7.jpg"
            ),
            preserve_default=False,
        ),
    ]
