from django.test import TestCase, Client
from quizzes.models import QuizIndexPage, QuizCategory, QuizPage, QuizQuestion
from django.urls import reverse
from wagtail.core.models import Site
from django.utils import timezone

'''
1. Tests the 'Categories sidebar' which is displayed on a 'Quiz Page', 'Quiz Index Page' 
and the 'Category List View'
2. Tests the 'Quizzes sidebar' which is displayed on the 'Category Detail View'
3. Tests the 'latest_quiz_visited_info' which displays the last quiz visited via a session
'''

class SidebarTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Get 'Quiz Index Page' (or create if doesnt exist)
        quiz_index_page = self.create_quiz_index_page_if_not_exists()
        
        '''
        Create pop_music category
        Create pop_music quiz page
        Assign pop_music quiz page as sub page of quiz index page
        Assign pop_music category to pop_music quiz page
        Add a question to pop_music quiz page
        '''
        pop_music_category = QuizCategory.objects.create(name="Pop Music", slug="pop-music")
        
        pop_music_quiz_page = QuizPage(
            title='Pop Music Quiz',
            intro='A quiz about Pop Music.',
            date=timezone.now(),
        )
        
        quiz_index_page.add_child(instance=pop_music_quiz_page)
        
        pop_music_quiz_page.categories.add(pop_music_category)
        
        QuizQuestion.objects.create(
            page=pop_music_quiz_page,
            question='How many members of the Beatles were there?',
            answer='Four'
        )

    def create_quiz_index_page_if_not_exists(self):
        # Get homepage
        site = Site.objects.get(is_default_site=True)
        home_page = site.root_page

        # If 'Quiz Index Page doesn't exist, create it and add as sub page of home
        if len(home_page.get_children().filter(title='Quiz Index Page')) == 0:
            quiz_index_page=QuizIndexPage(
                title='Quiz Index Page',
                intro='Welcome to our quiz index page.',
                slug='quiz-index-page'
            )
            home_page.add_child(instance=quiz_index_page)
        
        return home_page.get_children().get(title='Quiz Index Page')

    '''
    LATEST QUIZ VISITED INFO TESTS
    Tests 'latest_quiz_visited_info' appears in sidebar (from sessions)
    '''
    def test_latest_quiz_visited_in_category_list_view(self):
        response = self.client.get(reverse('quizzes:quiz_category_list_view'))
        self.assertTrue('latest_quiz_visited_info' in response.context)

    def test_latest_quiz_visited_in_category_detail_view(self):
        pop_music_category = QuizCategory.objects.get(name='Pop Music')
        response = self.client.get(reverse('quizzes:quiz_category_detail_view', args=(pop_music_category.slug,)))
        self.assertTrue('latest_quiz_visited_info' in response.context)

    def test_latest_quiz_visited_in_quiz_index_page(self):
        response = self.client.get('/quiz-index-page/')
        self.assertTrue('latest_quiz_visited_info' in response.context)

    '''
    CATEGORY SIDEBAR TESTS
    '''

    def test_category_sidebar_in_quiz_index_page_context(self):
        response = self.client.get('/quiz-index-page/')
        self.assertTrue('categories_sidebar' in response.context)

    def test_category_link_title_in_quiz_index_page_content(self):
        response = self.client.get('/quiz-index-page/')
        self.assertTrue('Pop Music' in str(response.context))
        self.assertTrue('href="/quizzes/category/pop-music"' in str(response.content))

    def test_category_sidebar_in_quiz_page_context(self):
        response = self.client.get('/quiz-index-page/pop-music-quiz/')
        self.assertTrue('categories_sidebar' in response.context)

    def test_category_link_title_in_quiz_page_content(self):
        response = self.client.get('/quiz-index-page/pop-music-quiz/')
        self.assertTrue('Pop Music' in str(response.context))
        self.assertTrue('href="/quizzes/category/pop-music"' in str(response.content))

    def test_category_sidebar_in_category_detail_view_context(self):
        pop_music_category = QuizCategory.objects.get(name='Pop Music')
        response = self.client.get(reverse('quizzes:quiz_category_detail_view', args=(pop_music_category.slug,)))
        self.assertTrue('categories_sidebar' in response.context)

    def test_category_link_title_in_category_detail_view_content(self):
        pop_music_category = QuizCategory.objects.get(name='Pop Music')
        response = self.client.get(reverse('quizzes:quiz_category_detail_view', args=(pop_music_category.slug,)))
        self.assertTrue('Pop Music' in str(response.context))
        self.assertTrue('href="/quizzes/category/pop-music"' in str(response.content))

    '''
    QUESTION SIDEBAR TESTS
    '''

    def test_quizzes_sidebar_in_category_list_view_context(self):
        response = self.client.get(reverse('quizzes:quiz_category_list_view'))
        self.assertTrue('quizzes_sidebar' in response.context)

    def test_quiz_title_link_in_quizzes_sibebar_category_list_view_content(self):
        response = self.client.get(reverse('quizzes:quiz_category_list_view'))
        self.assertTrue('Pop Music' in str(response.context))
        self.assertTrue('href="/quizzes/category/pop-music"' in str(response.content))





