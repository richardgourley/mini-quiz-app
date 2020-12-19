# Inherits from django.test.TestCase
from wagtail.tests.utils import WagtailPageTests
from quizzes.models import QuizPage
from home.models import HomePage
from django.utils import timezone

class HomePageTests(WagtailPageTests):
	def test_home_page_exists(self):
		home_page = HomePage.objects.all()[0]
		self.assertEqual(home_page, 'Home')

class QuizPageTests(WagtailPageTests):
    def test_can_create_a_page(self):
        pass