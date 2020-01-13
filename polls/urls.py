from django.urls import path
from . import views

app_name = "polls"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("Votes/<int:question_id>/", views.vote, name="vote"),
    path("Question_detail/<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("results/<int:pk>/", views.ResultsView.as_view(), name="result"),
    path("Dotaznik/", views.PollsView.as_view(), name="dotaznik"),
    path("Dotaznik/hlasovanie/", views.answers, name="answer"),
    path("Dotaznik/koniec/", views.thanks, name="thanks"),
    path("Dotaznik/vysledky", views.Results.as_view(), name="form_results"),
]
