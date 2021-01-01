from django.urls import path
from . import views

app_name = 'quizzes'
urlpatterns = [
    path('category/<slug:slug>', views.QuizCategoryDetailView.as_view(), name="quiz_category_detail_view"),
    path('categories/', views.QuizCategoryListView.as_view(), name="quiz_category_list_view"),
]
