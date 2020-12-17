from django.shortcuts import render
from django.views import generic
from .models import QuizCategory

# Create your views here.
class QuizCategoryDetailView(generic.DetailView):
    model = QuizCategory
    template_name = 'quizzes/quiz_category_detail_view.html'

    def get_queryset(self):
        return QuizCategory.objects.all()

class QuizCategoryListView(generic.ListView):
    model = QuizCategory
    template_name = 'quizzes/quiz_category_list_view.html'

    def get_queryset(self):
        return QuizCategory.objects.all()

    def get_context_data(self, **kwargs):
       data = super().get_context_data(**kwargs)
       most_recent_quiz_title = self.request.session['most_recent_quiz_title']
       most_recent_quiz_url = self.request.session['most_recent_quiz_url']
       data['most_recent_quiz_title'] = most_recent_quiz_title
       data['most_recent_quiz_url'] = most_recent_quiz_url
       return data

