from django.shortcuts import render
from django.views import generic
from .models import QuizCategory

# Create your views here.
class QuizCategoryDetailView(generic.DetailView):
	model = QuizCategory
	template_name = 'quizzes/quiz_category_detail_view.html'

	def get_queryset(self):
		return QuizCategory.objects.all()