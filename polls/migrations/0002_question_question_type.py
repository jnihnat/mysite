# Generated by Django 3.0 on 2020-01-02 22:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='question_type',
            field=models.CharField(choices=[('Choice', 'Chooice'), ('Text', 'Text Field')], default='Choice', max_length=200),
        ),
    ]
