from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название команды')),
                ('members_list', models.TextField(blank=True, help_text='Укажите имена участников через запятую', verbose_name='Участники команды')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('captain', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='captained_teams', to=settings.AUTH_USER_MODEL, verbose_name='Капитан')),
            ],
            options={
                'verbose_name': 'Команда',
                'verbose_name_plural': 'Команды',
                'ordering': ['-created_at'],
            },
        ),
    ]
