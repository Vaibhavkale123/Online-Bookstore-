# Generated by Django 5.0.7 on 2024-07-29 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_cartitem_order_alter_order_items'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]