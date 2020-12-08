from django import forms
from django.db import models

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from modelcluster.fields import ParentalKey, ParentalManyToManyField

# Create your models here.
class QuizCategory(models.Model):
    name = models.CharField(
        max_length=255,
        blank=False,
        null=False, 
        unique=True
    )
    slug = models.SlugField(
        max_length=255, 
        unique=True, 
        help_text='This will be how the category appears in urls eg. sitename/category/slug'
    )

    panels = [
        FieldPanel('name'),
        FieldPanel('slug')
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'quiz categories'

class QuizIndexPage(Page):
    intro = RichTextField(blank=False, null=False, help_text='Enter a short introduction to the index page which lists all quizzes.')

    def get_context(self, request):
        context = super().get_context(request)
        quiz_pages = self.get_children().live().order_by('title')
        context['quiz_pages'] = quiz_pages
        return context

    content_panels = Page.content_panels + [
        FieldPanel('intro')
    ]

class QuizPage(Page):
    intro = models.TextField(
        blank=False,
        null=False,
        help_text='Give a very brief introduction to this quiz.'
    )
    date = models.DateField("Quiz Creation Date")
    categories = ParentalManyToManyField('quizzes.QuizCategory', blank=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('intro'),
        ], heading='General'),
        FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
        InlinePanel('quiz_questions', label='Quiz Questions')
    ]

    def get_context(self, request):
        context = super().get_context(request)
        session = request.session
        request.session['most_recent_quiz_title'] = self.title
        request.session['most_recent_quiz_url'] = self.url
        return context


class QuizQuestion(Orderable):
    page = ParentalKey(QuizPage, on_delete=models.CASCADE, related_name='quiz_questions')
    question = models.CharField(
        max_length=255,
        unique=False,
        blank=False,
        null=False,
        help_text='Enter a question.'
    )
    answer = models.CharField(
        max_length=400,
        unique=False,
        blank=False,
        null=False,
        help_text='Enter the answer.'
    )

    panels = [
        FieldPanel('question'),
        FieldPanel('answer')
    ]

