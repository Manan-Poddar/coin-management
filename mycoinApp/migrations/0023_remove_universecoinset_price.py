# Generated by Django 5.1.1 on 2024-12-14 17:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mycoinApp', '0022_setnamecoins_price_alter_universecoinset_price_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='universecoinset',
            name='price',
        ),
    ]