# Generated by Django 5.1.1 on 2024-12-02 05:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mycoinApp', '0023_setnamecoins_universecoinset'),
    ]

    operations = [
        migrations.AlterField(
            model_name='setnamecoins',
            name='coin_list',
            field=models.JSONField(blank=True, null=True),
        ),
    ]