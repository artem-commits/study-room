# Generated by Django 4.2.21 on 2025-05-23 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, default='static/images/default_avatar/default_avatar.png', null=True, upload_to='users/%Y/%m/%d/', verbose_name='Пользовательский аватар'),
        ),
    ]
