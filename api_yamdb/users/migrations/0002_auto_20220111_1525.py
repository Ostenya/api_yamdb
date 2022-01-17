# Generated by Django 2.2.16 on 2022-01-11 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='bio',
            field=models.TextField(blank=True, verbose_name='Биография'),
        ),
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(default='user', max_length=50, verbose_name='Роль'),
            preserve_default=False,
        ),
    ]