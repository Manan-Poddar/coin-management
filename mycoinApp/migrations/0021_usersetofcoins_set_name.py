# Generated by Django 5.1.1 on 2024-12-01 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mycoinApp', '0020_alter_usersetofcoins_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersetofcoins',
            name='set_name',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
    ]
