from django.test import TestCase
from quizzes.models import QuizCategory, QuizPage
from wagtail.core.models import Site

from django.utils import timezone
import datetime

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

    def test_intro_null_is_false(self):
        quiz_page = QuizPage.objects.get(title='Tennis Quiz')
        intro_null = quiz_page._meta.get_field('intro').null
        self.assertFalse(intro_null)

    def test_intro_blank_is_false(self):
        quiz_page = QuizPage.objects.get(title='Tennis Quiz')
        intro_blank = quiz_page._meta.get_field('intro').blank
        self.assertFalse(intro_blank)

    def test_date_field_is_date(self):
        quiz_page = QuizPage.objects.get(title='Tennis Quiz')
        self.assertEqual(type(quiz_page.date), datetime.date)

    def test_date_field_year_length(self):
        quiz_page = QuizPage.objects.get(title='Tennis Quiz')
        year = quiz_page.date.year
        self.assertEqual(len(str(year)), 4)

class QuizQuestionTests(TestCase):
    @classmethod
    def setUpTestDate(cls):
        site = Site.objects.get(is_default_site=True)
        home_page = site.root_page
        #Create 'quiz_page' and add as sub page of 'home_page'
        quiz_page = QuizPage(
            title='Tennis Quiz',
            intro='An introduction to Quiz Test 1',
            date=timezone.now(),
        )
        home_page.add_child(instance=quiz_page)

        QuizQuestion.objects.create(
            page=quiz_page, 
            question='Who is a famous tennis player called Roger?', 
            answer='Roger Federer'
        )

    def test_quiz_question_page_is_type_quiz_page(self):
        quiz_question = QuizQuestion.objects.all()[0]
        self.assertEqual(quiz_question.page, QuizPage)

    def test_quiz_question_parental_key_title(self):
        # Get only quiz question
        quiz_question = QuizQuestion.objects.all()[0]
        self.assertEqual(quiz_question.page.title, 'Tennis Quiz')


        