from datetime import timedelta, time
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.utils import timezone
from quests.models import Quest, Session


class Command(BaseCommand):
    help = "Загружает фикстуру initial_quests.json и создает свободные сеансы для всех квестов"

    def handle(self, *args, **options):
        call_command("loaddata", "initial_quests.json")

        today = timezone.now().date()
        times = [time(12, 0), time(14, 30), time(17, 0), time(19, 30), time(21, 30)]

        quests = Quest.objects.all()
        for quest in quests:
            for day_offset in range(0, 7):
                session_date = today + timedelta(days=day_offset)
                for t in times:
                    Session.objects.get_or_create(
                        quest=quest,
                        date=session_date,
                        time=t,
                        defaults={"is_available": True},
                    )

        self.stdout.write(
            self.style.SUCCESS(f"Каталог заполнен! Квестов в каталоге: {quests.count()}. Сеансы сформированы.")
        )
