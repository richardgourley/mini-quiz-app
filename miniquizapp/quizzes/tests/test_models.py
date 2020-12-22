from django.test import TestCase
from quizzes.models import QuizCategory

class MyTestClass(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Non modified object used by all classes
        QuizCategory.objects.create(name="Sports", slug="sport")

    def setUp(self):
        pass

    def test_expected_category_str(self):
        quiz_category = QuizCategory.objects.get(id=1)
        self.assertEqual(str(quiz_category), 'Sports') 


