# Inherits from django.test.TestCase
from wagtail.tests.utils import WagtailPageTests
from quizzes.models import QuizPage


class QuizPageTests(WagtailPageTests):
    def test_can_create_a_page(self):
        pass