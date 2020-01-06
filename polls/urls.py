from django.urls import path
from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('Votes/<int:question_id>/', views.vote, name="vote"),
    path('Question_detail/<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('results/<int:pk>/', views.ResultsView.as_view(), name="result"),
    path('Dotaznik/', views.PollsView.as_view(), name="dotaznik"),
    path('Dotaznik/hlasovanie/', views.Hlasovanie, name="hlasovanie"),
    path('Dotaznik/koniec/', views.Koniec, name="koniec"),
    path('Dotaznik/vysledky', views.Vysledky.as_view(), name="vysledky")
]