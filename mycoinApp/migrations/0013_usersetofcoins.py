# Generated by Django 5.1.1 on 2024-11-25 15:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0005_remove_user_last_login'),
        ('mycoinApp', '0012_coinstatecondition_inclusion_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserSetOfCoins',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coin_set', models.CharField(max_length=64)),
                ('coin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mycoinApp.coin')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.user')),
            ],
        ),
    ]
