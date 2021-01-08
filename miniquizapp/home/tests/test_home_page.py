from django.test import TestCase, Client
from quizzes.models import QuizIndexPage, QuizCategory, QuizPage, QuizQuestion
from django.urls import reverse
from wagtail.core.models import Site
from django.utils import timezone

class HomePageTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Get homepage
        site = Site.objects.get(is_default_site=True)
        home_page = site.root_page
        
        # Create a quiz index page
        quiz_index_page=QuizIndexPage(
            title='Quiz Index Page',
            intro='Welcome to our quiz index page.',
            slug='quiz-index-page'
        )
        home_page.add_child(instance=quiz_index_page)

        # Create a space category
        space_category = QuizCategory.objects.create(name="Space", slug="space")
        
        # Create a space quiz
        space_quiz_page = QuizPage(
            title='Space Quiz',
            intro='A quiz about our solar system.',
            date=timezone.now(),
        )
        
        # Assign space quiz as sub page of quiz index page
        quiz_index_page.add_child(instance=space_quiz_page)
        
        # Assign space category to the space quiz page
        space_quiz_page.categories.add(space_category)
        space_quiz_page.save()

    '''
    TEST HOME PAGE STATUS CODE
    '''

    def test_home_page_200(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    '''
    CONTEXT TESTS
    '''

    def test_latest_quizzes_appears_in_context(self):
        response = self.client.get('/')
        self.assertTrue('latest_quizzes' in response.context)

    def test_latest_quizzes_length_one(self):
        response = self.client.get('/')
        self.assertTrue(len(response.context['latest_quizzes']) == 1)

    def test_all_categories_appears_in_context(self):
        response = self.client.get('/')
        self.assertTrue('all_categories' in response.context)

    def test_all_categories_length_one(self):
        response = self.client.get('/')
        self.assertTrue(len(response.context['all_categories']) == 1)

    '''
    CONTENT TESTS
    '''

    def test_home_title(self):
        response = self.client.get('/')
        self.assertTrue('Mini Quiz App' in str(response.content))

    def test_navbar_home_link(self):
        response = self.client.get('/')
        self.assertTrue('href="/">Home' in str(response.content))

    def test_navbar_quiz_categories_link(self):
        response = self.client.get('/')
        self.assertTrue('href="/quizzes/categories/">Quiz Categories</a>' in str(response.content))

    def test_navbar_quiz_index_page_link(self):
        response = self.client.get('/')
        self.assertTrue('href="/quiz-index-page/">Quiz Index</a>' in str(response.content))

    def test_quiz_page_appears(self):
        response = self.client.get('/')
        self.assertTrue('<a href="/quiz-index-page/space-quiz/">' in str(response.content))
        self.assertTrue('Space Quiz' in str(response.content))
        self.assertTrue('A quiz about our solar system.' in str(response.content))

    def test_quiz_category_appears(self):
        response = self.client.get('/')
        self.assertTrue('<a href="/quizzes/category/space">' in str(response.content))
        self.assertTrue('Space' in str(response.content))

    def test_call_to_action_link(self):
        response = self.client.get('/')
        self.assertTrue('<a href="/quiz-index-page/">' in str(response.content))
