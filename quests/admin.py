from django.contrib import admin
from .models import Quest, Session, Booking


class SessionInline(admin.TabularInline):
    model = Session
    extra = 3


@admin.register(Quest)
class QuestAdmin(admin.ModelAdmin):
    list_display = ("title", "genre", "difficulty", "fear_level", "max_players", "price")
    list_filter = ("genre", "difficulty", "fear_level")
    search_fields = ("title", "description")
    inlines = [SessionInline]


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ("quest", "date", "time", "is_available")
    list_filter = ("is_available", "date", "quest")


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("id", "quest", "session", "customer_name", "customer_phone", "players_count", "total_price", "status", "created_at")
    list_filter = ("status", "add_actor", "created_at")
    search_fields = ("customer_name", "customer_phone", "customer_email", "quest__title")
