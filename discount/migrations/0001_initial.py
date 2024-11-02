# Generated by Django 5.0.7 on 2024-10-11 10:44

import discount.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('train', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DiscountCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount_of_rides', models.IntegerField(blank=True, default=0, verbose_name='Количество поездок')),
                ('discount', models.DecimalField(decimal_places=2, max_digits=5, validators=[discount.validators.between_0_and_1], verbose_name='Процент скидки')),
                ('duration', models.DurationField(verbose_name='Время действия')),
                ('max_usage', models.IntegerField(blank=True, null=True, verbose_name='Максимальное количество поездок')),
                ('is_active', models.BooleanField(blank=True, default=True, verbose_name='Активна ли карта')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('types_of_trains', models.ManyToManyField(to='train.traintype', verbose_name='Тип поездов')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Скидочная карта',
                'verbose_name_plural': 'Скидочные карты',
            },
        ),
    ]