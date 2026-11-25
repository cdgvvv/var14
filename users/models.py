from django.db import models
from django.contrib.auth.models import User


class Team(models.Model):
    name = models.CharField("Название команды", max_length=100)
    captain = models.ForeignKey(User, on_delete=models.CASCADE, related_name="captained_teams", verbose_name="Капитан")
    members_list = models.TextField("Участники команды", help_text="Укажите имена участников через запятую", blank=True)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    class Meta:
        verbose_name = "Команда"
        verbose_name_plural = "Команды"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name
