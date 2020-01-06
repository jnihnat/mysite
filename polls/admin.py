from django.contrib import admin
from .models import Question, Choice, Texts, Integer


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class TextInline(admin.TabularInline):
    model = Texts
    extra = 0


class IntInline(admin.TabularInline):
    model = Integer
    extra = 0


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['question_text', 'Order', 'question_type']}),
        ('Date Information', {'fields': ['pub_date']}),

    ]
    inlines = [ChoiceInline, TextInline, IntInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently','Order')
    list_filter = ['pub_date']
    search_fields = ['question_text']
    readonly_fields = ['question_type']

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ["question_type"]
        else:
            return []

    def get_formsets_with_inlines(self, request, obj=None):
        for inline in self.get_inline_instances(request, obj):
            # hide/show market-specific inlines based on market name
            if obj and obj.extra_fields_by_type() == inline.__class__.__name__:
                yield inline.get_formset(request, obj), inline


admin.site.register(Question, QuestionAdmin)

# Register your models here.
