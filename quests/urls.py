from django.urls import path
from . import views

app_name = "quests"

urlpatterns = [
    path("", views.home, name="home"),
    path("catalog/", views.QuestListView.as_view(), name="catalog"),
    path("quest/<int:pk>/", views.QuestDetailView.as_view(), name="quest_detail"),
    path("quest/<int:pk>/book/", views.book_quest, name="book_quest"),
    path("search/", views.search_view, name="search"),
    path("about/", views.about_view, name="about"),
    path("api/check-slot/", views.check_slot_api, name="check_slot_api"),
]
