from django.test import TestCase
from django.utils import timezone
from quizzes.models import QuizCategory, QuizPage, QuizIndexPage, QuizQuestion
from home.models import HomePage

def create_quiz_category():
	return QuizCategory.objects.create(
        name="Sports",
        slug="sports"
    )

class QuizCategoryModelTests(TestCase):

	def test_str_equal_to_name(self):
	    quiz_category = create_quiz_category()
	    self.assertEqual(str(quiz_category), quiz_category.name) 


