import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from . models import Question, Choice


def create_question(q_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=q_text, pub_date=time)


def create_choice(question, ch_text):
    return Choice.objects.create(question=question, choice_text=ch_text)


class QuestionIndexViewTest(TestCase):
    def test_no_question(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code,200)
        self.assertContains(response, 'No polls are avaiable')
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        question = create_question('Question past', -10)
        create_choice(question, 'choice 1')
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Question past>'])

    def test_future_question(self):
        create_question('Future Question', 10)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, 'No polls are avaiable')
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_past_question(self):
        question = create_question('Question past', -10)
        create_question('Future Question', 10)
        create_choice(question, 'choice 1')
        response=self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Question past>'])

    def test_two_past_question(self):
        question1 = create_question('Question past1', -10)
        question2 = create_question('Question past2', -1)
        create_choice(question1, 'choice 1')
        create_choice(question2, 'choice 1')
        response=self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],
                                 ['<Question: Question past1>', '<Question: Question past2>'])

    def test_question_without_choice(self):
        create_question('Without Choice', -1)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No polls are avaiable')
        self.assertQuerysetEqual(response.context['latest_question_list'], [])


class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_date(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_q(self):
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_q(self):
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), True)


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        question = create_question('Future Question', 10)
        create_choice(question, 'choice 1')
        response = self.client.get(reverse('polls:detail', args=(question.id, )))
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        question=create_question('Past Question', -10)
        create_choice(question, 'choice 1')
        response=self.client.get(reverse('polls:detail', args=(question.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Past Question')

    def test_no_choice_past_question(self):
        question = create_question('Future Question', -10)
        response = self.client.get(reverse('polls:detail', args=(question.id, )))
        self.assertEqual(response.status_code, 404)


