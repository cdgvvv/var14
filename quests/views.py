from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Q

from .models import Quest, Session, Booking
from .forms import BookingForm


def home(request):
    top_quests = Quest.objects.all()[:4]
    genres = Quest.objects.values_list("genre", flat=True).distinct()
    return render(request, "quests/home.html", {"top_quests": top_quests, "genres": genres})


def about_view(request):
    sample_quests = Quest.objects.all()[:3]
    return render(request, "quests/about.html", {"sample_quests": sample_quests})


class QuestListView(ListView):
    model = Quest
    template_name = "quests/catalog.html"
    context_object_name = "quests"
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset()
        genre = self.request.GET.get("genre")
        difficulty = self.request.GET.get("difficulty")
        if genre:
            qs = qs.filter(genre=genre)
        if difficulty:
            qs = qs.filter(difficulty=difficulty)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["genres"] = Quest.objects.values_list("genre", flat=True).distinct()
        context["selected_genre"] = self.request.GET.get("genre", "")
        context["selected_difficulty"] = self.request.GET.get("difficulty", "")
        return context


class QuestDetailView(DetailView):
    model = Quest
    template_name = "quests/quest_detail.html"
    context_object_name = "quest"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sessions"] = Session.objects.filter(
            quest=self.object,
            date__gte=timezone.now().date(),
            is_available=True,
        )
        return context


def book_quest(request, pk):
    quest = get_object_or_404(Quest, pk=pk)
    sessions = Session.objects.filter(
        quest=quest,
        date__gte=timezone.now().date(),
        is_available=True,
    )

    initial_data = {}
    if request.user.is_authenticated:
        initial_data["customer_name"] = request.user.get_full_name() or request.user.username
        initial_data["customer_email"] = request.user.email or ""
    preselected_session = request.GET.get("session")
    if preselected_session:
        initial_data["session_id"] = preselected_session

    if request.method == "POST":
        form = BookingForm(request.POST, quest=quest)
        if form.is_valid():
            session = form.cleaned_data["session_obj"]
            add_actor = form.cleaned_data.get("add_actor", False)
            total_price = quest.price + (Decimal("500.00") if add_actor else Decimal("0.00"))

            Booking.objects.create(
                user=request.user if request.user.is_authenticated else None,
                quest=quest,
                session=session,
                customer_name=form.cleaned_data["customer_name"],
                customer_phone=form.cleaned_data["customer_phone"],
                customer_email=form.cleaned_data["customer_email"],
                players_count=form.cleaned_data["players_count"],
                add_actor=add_actor,
                total_price=total_price,
                status="confirmed",
            )
            session.is_available = False
            session.save(update_fields=["is_available"])

            messages.success(
                request,
                f"Бронь на квест «{quest.title}» ({session.date.strftime('%d.%m.%Y')} в {session.time.strftime('%H:%M')}) успешно оформлена!",
            )
            if request.user.is_authenticated:
                return redirect("users:profile")
            return redirect("quests:quest_detail", pk=quest.pk)
        else:
            messages.error(request, "Проверьте правильность заполнения формы.")
    else:
        form = BookingForm(quest=quest, initial=initial_data)

    return render(
        request,
        "quests/booking.html",
        {"form": form, "quest": quest, "sessions": sessions},
    )


def search_view(request):
    query = request.GET.get("q", "").strip()
    if query:
        results = Quest.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query) | Q(genre__icontains=query)
        )
    else:
        results = Quest.objects.all()
    return render(request, "quests/search.html", {"results": results, "query": query})


def check_slot_api(request):
    session_id = request.GET.get("session_id")
    if session_id:
        try:
            session = Session.objects.get(id=session_id)
            return JsonResponse(
                {
                    "available": session.is_available,
                    "time": session.time.strftime("%H:%M"),
                    "date": session.date.strftime("%d.%m.%Y"),
                }
            )
        except (Session.DoesNotExist, ValueError):
            return JsonResponse({"available": False, "error": "Сеанс не найден"})
    return JsonResponse({"available": False, "error": "Не передан ID"})
