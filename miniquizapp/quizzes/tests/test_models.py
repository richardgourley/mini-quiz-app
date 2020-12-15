from django.test import TestCase
from django.utils import timezone
from quizzes.models import QuizCategory, QuizPage, QuizIndexPage, QuizQuestion
from home.models import HomePage

class QuizCategoryTests(TestCase):
	@classmethod
	def setUpTestData(cls):
		cls.quiz_category1 = QuizCategory.objects.create(
                name="Food and drink",
                slug="food_and_drink"
			)

	def test_str(self):
		self.assertEqual(str(quiz_category1), "Food and drink")


