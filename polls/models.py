from django.db import models
from django.utils import timezone
import datetime


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    Order = models.IntegerField()

    class Que_type(models.TextChoices):
        Choice = 'Choice', 'Choice'
        Text = 'Text', 'Text Field'
        Integer = 'Int', 'Integer Field'

    question_type=models.CharField(max_length=200, choices=Que_type.choices, default= Que_type.Choice)

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return timezone.now() >= self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.short_description = 'Published Recently?'
    was_published_recently.boolean = True

    def extra_fields_by_type(self):
        extra_inline_model=''
        if self.question_type == 'Choice':
            extra_inline_model = 'ChoiceInline'
        elif self.question_type == 'Text':
            extra_inline_model = 'TextInline'
        elif self.question_type == 'Int':
            extra_inline_model = 'IntInline'
        return extra_inline_model


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


class Texts(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.text


class Integer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    integer = models.IntegerField()
    votes = models.IntegerField(default=0)




