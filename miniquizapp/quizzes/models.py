from django.db import models

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from modelcluster.fields import ParentalKey, ParentalManyToManyField

# Create your models here.
class QuizIndexPage(Page):
	intro = RichTextField(blank=False, null=False, help_text='Enter a short introduction to the index page which lists all quizzes.')

	def get_context(self, request):
		context = super().get_context(request)
		quiz_pages = self.get_children().live().order_by('title')
		context['quiz_pages'] = quiz_pages
		return context

class QuizPage(Page):
	name = models.CharField(
        max_length=255,
        unique=True,
        blank=False,
        null=False,
        help_text='Give a name for this quiz.'
	)
	intro = models.TextField(
        blank=False,
        null=True,
        help_text='Give a very brief introduction to this quiz.'
	)
	date = models.DateField("Quiz Creation Date")

	content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('name'),
            FieldPanel('date'),
        ], heading='General'),
        FieldPanel('intro'),
        InlineFieldPanel('quiz_questions', label='Quiz Questions')
	]


