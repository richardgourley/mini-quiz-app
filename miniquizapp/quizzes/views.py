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
       context = super().get_context_data(**kwargs)
       context['most_recent_quiz_info'] = get_most_recent_quiz_info(self)
       return context

def get_most_recent_quiz_info(self):
    test_dict1 = dict()
    test_dict1['title'] = self.request.session['most_recent_quiz_title']
    test_dict1['url'] = self.request.session['most_recent_quiz_url']
    return test_dict1

