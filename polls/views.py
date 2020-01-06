from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone, datastructures
from .models import Question, Choice, Texts, Integer
import django.core.exceptions
from django.template import loader


def index(request):
    latest_question_list = Question.objects.order_by('pub_date')[:5]
    context = {
        'latest_question_list' : latest_question_list,
    }
    return render(request, 'polls/index.html', context)


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.exclude(choice__isnull=True).filter(pub_date__lte=timezone.now()).order_by('pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        return Question.objects.exclude(choice__isnull=True).filter(pub_date__lte=timezone.now())


class PollsView(generic.ListView):
    model = Question
    template_name = 'polls/pollsview.html'

    def get_queryset(self):
        return Question.objects.exclude(choice__isnull=True).filter(pub_date__lte=timezone.now())\
            .union(Question.objects.filter(pub_date__lte=timezone.now(), question_type="Text"))\
            .union(Question.objects.filter(pub_date__lte=timezone.now(), question_type="Int")).order_by('Order')


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def PrvaStranka(request):
    return render(request, 'polls/prvastranka.html')


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def result(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': 'Nezaskrtol si volbu',
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:result', args=(question_id, )))


def Hlasovanie(request):
    asked_questions = Question.objects.exclude(choice__isnull=True).filter(pub_date__lte=timezone.now())\
        .union(Question.objects.filter(pub_date__lte=timezone.now(), question_type="Text"))\
        .union(Question.objects.filter(pub_date__lte=timezone.now(), question_type="Int")).order_by('Order')
    ids = list(asked_questions.values_list('id', flat=True))
    ids = list(map(str, ids))
    answered_questions = list(request.POST.keys())[1:]
#    unanswered_questions = set(ids).symmetric_difference(set(answered_questions))
    if ids == answered_questions:
        for question in asked_questions:
            if question.question_type == 'Choice':
                choice = question.choice_set.get(pk=request.POST.__getitem__(str(question.id)))
                choice.votes += 1
                choice.save()
            elif question.question_type == 'Text':
                text = request.POST.__getitem__(str(question.id))
                try:
                    choice = question.texts_set.get(text=request.POST.__getitem__(str(question.id)))
                    choice.votes += 1
                    choice.save()
                except (KeyError, Texts.DoesNotExist):
                    newtext = Texts(question=question, text=text, votes=1)
                    newtext.save()
            elif question.question_type == 'Int':
                Int = request.POST.__getitem__(str(question.id))
                try:
                    choice = question.integer_set.get(integer=int(Int))
                    choice.votes += 1
                    choice.save()
                except (KeyError, Texts.DoesNotExist):
                    newint = Integer(question=question, integer=Int, votes=1)
                    newint.save()

    else:
        return render(request, 'polls/pollsview.html', {
            'object_list': asked_questions,
            'error_message': 'Nezaskrtol si volbu',
        })
    return HttpResponseRedirect(reverse('polls:koniec'))


def Koniec(request):
    return render(request, 'polls/koniec.html')


class Vysledky(generic.ListView):
    model = Question
    template_name = 'polls/vysledky.html'

    def get_queryset(self):
        return Question.objects.exclude(choice__isnull=True).filter(pub_date__lte=timezone.now())\
        .union(Question.objects.filter(pub_date__lte=timezone.now(), question_type="Text"))\
        .union(Question.objects.filter(pub_date__lte=timezone.now(), question_type="Int")).order_by('Order')