# Generated by Django 5.1.1 on 2024-12-05 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mycoinApp', '0012_setnamecoins_coinstatecondition_inclusion_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='universecoinset',
            name='coin_set',
            field=models.JSONField(blank=True, null=True),
        ),
    ]