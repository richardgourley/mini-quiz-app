from django.test import TestCase, Client
from quizzes.models import QuizIndexPage, QuizCategory, QuizPage
from django.urls import reverse

class QuizCategoryListViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Non modified object used by all classes
        QuizCategory.objects.create(name="Sports", slug="sport")

    def test_quiz_category_list_view_200(self):
        response = self.client.get(reverse('quizzes:quiz_category_list_view'))
        self.assertEqual(response.status_code, 200)

    # Content tests

    def test_sports_category_title_appears(self):
    	response = self.client.get(reverse('quizzes:quiz_category_list_view'))
    	title = 'Sports'
    	self.assertTrue(title in str(response.content))

    def test_sports_category_link_appears(self):
    	response = self.client.get(reverse('quizzes:quiz_category_list_view'))
    	link = '<a href="/quizzes/category/sport">'
    	self.assertTrue(link in str(response.content))

    # Context tests

    def test_all_categories_appears_in_context(self):
    	response = self.client.get(reverse('quizzes:quiz_category_list_view'))
    	self.assertTrue('all_categories' in response.context)

    def test_length_all_categories_is_one(self):
    	response = self.client.get(reverse('quizzes:quiz_category_list_view'))
    	all_categories = response.context['all_categories']
    	self.assertTrue(len(all_categories) == 1)

    def test_sports_appears_in_all_categories(self):
    	response = self.client.get(reverse('quizzes:quiz_category_list_view'))
    	all_categories = response.context['all_categories']
    	sports = all_categories.get(name='Sports')
    	self.assertTrue(sports.slug == 'sports')

class QuizCategoryDetailViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Non modified object used by all classes
        category = QuizCategory.objects.create(name="Geography", slug="geography")

        '''
        Get HOME page
        '''
        site = Site.objects.get(is_default_site=True)
        home_page = site.root_page
        '''
        Create and add QUIZPAGE as sub page of HOME page
        '''
        quiz_page = QuizPage(
            title='Capital Cities',
            intro='A quiz about capital cities.',
            date=timezone.now(),
        )
        home_page.add_child(instance=quiz_page)

        # assign 'geography' category
        quiz_page.categories.add(category)

        # In shell, need to save the quiz_page to affect updated category change
        # quiz_page.save()




