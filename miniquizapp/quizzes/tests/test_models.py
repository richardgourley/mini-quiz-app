from django.test import TestCase
from quizzes.models import QuizCategory, QuizPage
from wagtail.core.models import Site

from django.utils import timezone

class QuizCategoryTests(TestCase):
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

    def test_quiz_category_slug_max_length(self):
        quiz_category = QuizCategory.objects.get(id=1)
        max_length = quiz_category._meta.get_field('slug').max_length
        self.assertEqual(max_length, 255)

    def test_quiz_category_slug_is_unique(self):
        quiz_category = QuizCategory.objects.get(id=1)
        unique = quiz_category._meta.get_field('slug').unique
        self.assertTrue(unique)

class QuizPageTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        '''
        Get HOME page
        '''
        site = Site.objects.get(is_default_site=True)
        home_page = site.root_page
        '''
        Create and add QUIZPAGE as sub page of HOME page
        '''
        quiz_page = QuizPage(
            title='Tennis Quiz',
            intro='An introduction to Quiz Test 1',
            date=timezone.now(),
        )
        home_page.add_child(instance=quiz_page)

    def test_slug_created(self):
        quiz_page = QuizPage.objects.get(title='Tennis Quiz')
        self.assertEqual(quiz_page.slug, 'tennis-quiz')
        