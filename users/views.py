from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from quests.models import Booking
from .models import Team
from .forms import RegisterForm, TeamForm


def register_view(request):
    if request.user.is_authenticated:
        return redirect("users:profile")
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Добро пожаловать в QuestDark, {user.username}!")
            return redirect("users:profile")
    else:
        form = RegisterForm()
    return render(request, "users/register.html", {"form": form})


@login_required
def profile_view(request):
    if request.method == "POST":
        team_form = TeamForm(request.POST)
        if team_form.is_valid():
            team = team_form.save(commit=False)
            team.captain = request.user
            team.save()
            messages.success(request, f"Команда «{team.name}» создана!")
            return redirect("users:profile")
        else:
            messages.error(request, "Проверьте поля формы команды.")
    else:
        team_form = TeamForm()

    bookings = Booking.objects.filter(user=request.user).select_related("quest", "session")
    teams = Team.objects.filter(captain=request.user)
    return render(
        request,
        "users/profile.html",
        {"bookings": bookings, "teams": teams, "team_form": team_form},
    )


@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if request.method == "POST" and booking.status != "cancelled":
        booking.status = "cancelled"
        booking.save(update_fields=["status"])
        booking.session.is_available = True
        booking.session.save(update_fields=["is_available"])
        messages.info(request, f"Бронирование #{booking.id} отменено, слот снова свободен.")
    return redirect("users:profile")
