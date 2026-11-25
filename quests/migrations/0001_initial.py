from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Quest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
                ('genre', models.CharField(max_length=50, verbose_name='Жанр')),
                ('fear_level', models.IntegerField(default=3, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='Уровень страха')),
                ('difficulty', models.IntegerField(default=3, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='Сложность')),
                ('duration_minutes', models.IntegerField(default=60, verbose_name='Длительность (мин)')),
                ('max_players', models.IntegerField(default=6, verbose_name='Макс. игроков')),
                ('price', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Цена')),
                ('image', models.ImageField(blank=True, null=True, upload_to='quests/', verbose_name='Постер')),
            ],
            options={
                'verbose_name': 'Квест',
                'verbose_name_plural': 'Квесты',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Дата')),
                ('time', models.TimeField(verbose_name='Время')),
                ('is_available', models.BooleanField(default=True, verbose_name='Свободно')),
                ('quest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sessions', to='quests.quest', verbose_name='Квест')),
            ],
            options={
                'verbose_name': 'Сеанс',
                'verbose_name_plural': 'Сеансы',
                'ordering': ['date', 'time'],
            },
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_name', models.CharField(default='Гость', max_length=100, verbose_name='Имя контактного лица')),
                ('customer_phone', models.CharField(default='+7 (999) 000-00-00', max_length=25, verbose_name='Телефон')),
                ('customer_email', models.EmailField(blank=True, default='', max_length=254, verbose_name='Email')),
                ('players_count', models.IntegerField(validators=[django.core.validators.MinValueValidator(2), django.core.validators.MaxValueValidator(12)], verbose_name='Количество игроков')),
                ('add_actor', models.BooleanField(default=False, verbose_name='Доп. аниматор (+500₽)')),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Итоговая стоимость')),
                ('status', models.CharField(choices=[('confirmed', 'Подтверждена'), ('pending', 'Ожидает подтверждения'), ('cancelled', 'Отменена')], default='confirmed', max_length=20, verbose_name='Статус')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('quest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='quests.quest', verbose_name='Квест')),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='quests.session', verbose_name='Сеанс')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bookings', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Бронирование',
                'verbose_name_plural': 'Бронирования',
                'ordering': ['-created_at'],
            },
        ),
    ]
