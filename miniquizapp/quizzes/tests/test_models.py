from django.test import TestCase
from quizzes.models import QuizCategory

class MyTestClass(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Non modified object used by all classes
        QuizCategory.objects.create(name="Sports", slug="sport")

    def setUp(self):
        pass

    def test_quiz_category_str(self):
        quiz_category = QuizCategory.objects.get(id=1)
        self.assertEqual(str(quiz_category), 'Sports')

    def test_quiz_category_name_max_length(self):
        quiz_category = QuizCategory.objects.get(id=1)
        max_length = quiz_category._meta.get_field('name').max_length
        self.assertEqual(max_length, 255) 


