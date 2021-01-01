from django.test import TestCase, Client
from quizzes.models import QuizIndexPage, QuizCategory
from django.urls import reverse

class QuizCategoryListViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Non modified object used by all classes
        QuizCategory.objects.create(name="Sports", slug="sport")

    def test_quiz_category_list_view_200(self):
        self.client = Client()
        response = self.client.get(reverse('quizzes:quiz_category_list_view'))
        self.assertEqual(response.status_code, 200)
