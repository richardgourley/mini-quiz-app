from django.test import TestCase, Client
from quizzes.models import QuizIndexPage, QuizCategory, QuizPage, QuizQuestion
from django.urls import reverse
from wagtail.core.models import Site
from django.utils import timezone

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

    # TESTS THE LAST QUIZ USER VISITED IN CONTEXT (FROM SESSIONS)
    def test_latest_quiz_in_context(self):
        response = self.client.get(reverse('quizzes:quiz_category_list_view'))
        self.assertTrue('latest_quiz_visited_info' in response.context)

class QuizCategoryDetailViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Get 'Quiz Index Page' (or create if doesnt exist)
        quiz_index_page = self.create_quiz_index_page_if_not_exists()
        
        '''
        Create geography category
        Create geography quiz page
        Assign geography quiz page as sub page of quiz index page
        Assign geography category to geography quiz page
        '''
        geography_category = QuizCategory.objects.create(name="Geography", slug="geography")

        geography_quiz_page = QuizPage(
            title='Capital Cities',
            intro='A quiz about capital cities.',
            date=timezone.now(),
        )
        quiz_index_page.add_child(instance=geography_quiz_page)

        geography_quiz_page.categories.add(geography_category)

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


    def test_detail_view_string_returns_200(self):
        # Client already exists in TestCase
        response = self.client.get('/quizzes/category/geography')
        self.assertTrue(response.status_code == 200)

    def test_detail_view_reverse_returns_200(self):
        geography = QuizCategory.objects.get(name='Geography')
        response = self.client.get(reverse('quizzes:quiz_category_detail_view', args=(geography.slug,)))
        self.assertTrue(response.status_code == 200)

    # Test Context

    def test_length_quiz_page_queryset_in_context(self):
        geography = QuizCategory.objects.get(name='Geography')
        response = self.client.get(reverse('quizzes:quiz_category_detail_view', args=(geography.slug,)))
        quiz_pages = response.context['quizcategory'].quizpage_set.all()
        self.assertTrue(len(quiz_page) == 1)

    def test_quiz_page_appears_in_quiz_page_queryset_context(self):
        geography = QuizCategory.objects.get(name='Geography')
        response = self.client.get(reverse('quizzes:quiz_category_detail_view', args=(geography.slug,)))
        quiz_pages = response.context['quizcategory'].quizpage_set.all()
        self.assertEqual(quiz_pages.first.title, 'Capital Cities')

    # TESTS THE LAST QUIZ USER VISITED IS IN CONTEXT (FROM SESSIONS)
    def test_latest_quiz_in_context(self):
        geography = QuizCategory.objects.get(name='Geography')
        response = self.client.get(reverse('quizzes:quiz_category_detail_view', args=(geography.slug,)))
        self.assertTrue('latest_quiz_visited_info' in response.context)

    # Test content

    def test_capital_cities_title_appears_in_detail_view(self):
        geography = QuizCategory.objects.get(name='Geography')
        response = self.client.get(reverse('quizzes:quiz_category_detail_view', args=(geography.slug,)))
        self.assertTrue('Capital Cities' in str(response.content))

    def test_capital_cities_intro_appears_in_detail_view(self):
        geography = QuizCategory.objects.get(name='Geography')
        response = self.client.get(reverse('quizzes:quiz_category_detail_view', args=(geography.slug,)))
        self.assertTrue('A quiz about capital cities.' in str(response.content))

    def test_capital_cities_link_appears_in_detail_view(self):
        geography = QuizCategory.objects.get(name='Geography')
        response = self.client.get(reverse('quizzes:quiz_category_detail_view', args=(geography.slug,)))
        self.assertTrue('<a href="/quiz-index-page/capital-cities/">' in str(response.content))

class QuizPageTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Get 'Quiz Index Page' (or create if doesnt exist)
        quiz_index_page = self.create_quiz_index_page_if_not_exists()
        
        '''
        Create film category
        Create film quiz page
        Assign film quiz page as sub page of quiz index page
        Assign film category to film quiz page
        Add a question to film quiz page
        '''
        film_category = QuizCategory.objects.create(name="Films", slug="films")

        film_quiz_page = QuizPage(
            title='Films from 1980-1990',
            intro='A quiz about films between 1980 and 1990.',
            date=timezone.now(),
        )
        quiz_index_page.add_child(instance=film_quiz_page)

        film_quiz_page.categories.add(film_category)

        QuizQuestion.objects.create(
            page=film_quiz_page,
            question='Who directed the 1981 film the Raiders of the Lost Ark?',
            answer='Steven Spielberg'
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

    def test_film_quiz_page_200(self):
        response = self.client.get('/quiz-index-page/films-from-1980-1990/')
        self.assertTrue(response.status_code == 200)

    # CONTENT TESTS (CATEGORIES, BUTTONS, JS FILES)

    def test_categories_appear(self):
        response = self.client.get('/quiz-index-page/films-from-1980-1990/')
        # test href appears for films category
        self.assertTrue('href="/quizzes/category/films"' in str(response.content))
        self.assertTrue('Films' in str(response.content))

    def test_reveal_answers_button_appears(self):
        response = self.client.get('/quiz-index-page/films-from-1980-1990/')
        self.assertTrue('REVEAL ANSWERS!</button>' in str(response.content))

    def test_js_quiz_page_loaded(self):
        response = self.client.get('/quiz-index-page/films-from-1980-1990/')
        self.assertTrue('<script type="text/javascript" src="/static/quizzes/js/quizzes.js"></script>' in str(response.content))

    # CONTENT TESTS (QUESTION APPEARS TESTS)
    
    def test_film_quiz_page_title_appears(self):
        response = self.client.get('/quiz-index-page/films-from-1980-1990/')
        self.assertTrue('<h2>Films from 1980-1990</h2>' in str(response.content))

    def test_quiz_intro_appears(self):
        response = self.client.get('/quiz-index-page/films-from-1980-1990/')
        self.assertTrue('A quiz about films between 1980 and 1990.' in str(response.content))

    def test_question_appears(self):
        response = self.client.get('/quiz-index-page/films-from-1980-1990/')
        self.assertTrue('Who directed the 1981 film the Raiders of the Lost Ark?' in str(response.content))

    def test_answer_appears(self):
        response = self.client.get('/quiz-index-page/films-from-1980-1990/')
        self.assertTrue('Steven Spielberg' in str(response.content))
    
    # CONTEXT TESTS ()

    def test_page_exists_in_context(self):
        response = self.client.get('/quiz-index-page/films-from-1980-1990/')
        self.assertTrue('page' in response.context)
    
    def test_page_title(self):
        response = self.client.get('/quiz-index-page/films-from-1980-1990/')
        page = response.content['page']
        self.assertEqual(page.title, 'Films from 1980-1990')

    def test_page_slug(self):
        response = self.client.get('/quiz-index-page/films-from-1980-1990/')
        page = response.content['page']
        self.assertEqual(page.slug, 'films-from-1980-1990')


class QuizIndexPageTests(self):
    @classmethod
    def setUpTestData(cls):
        # Get 'Quiz Index Page' (or create if doesnt exist)
        quiz_index_page = self.create_quiz_index_page_if_not_exists()
        
        '''
        Create food category
        Create food quiz page
        Assign food quiz page as sub page of quiz index page
        Assign food category to food quiz page
        Add a question to food quiz page
        '''
        food_category = QuizCategory.objects.create(name="Food", slug="food")
        
        food_quiz_page = QuizPage(
            title='Italian Food',
            intro='A quiz about Italian Food.',
            date=timezone.now(),
        )
        
        quiz_index_page.add_child(instance=food_quiz_page)
        
        food_quiz_page.categories.add(food_category)
        
        QuizQuestion.objects.create(
            page=food_quiz_page,
            question='Which famous Italian cheese is produced in the Italian regions of Emilia-Romagna and Lombardy?',
            answer='Parmesan (Parmigiano-Reggiano)'
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

    def test_quiz_index_page_200(self):
        response = self.client.get('/quiz-index-page/')
        self.assertEqual(response.status_code, 200)

    # CONTENT TESTS

    def test_food_quiz_appears(self):
        response = self.client.get('/quiz-index-page/')
        self.assertTrue('Italian Food' in str(response.content))
        self.assertTrue('A quiz about Italian Food.' in str(response.content))

    def test_food_quiz_link_appears(self):
        response = self.client.get('/quiz-index-page/')
        self.assertTrue('/quiz-index-page/italian-food/' in str(response.content))

    def test_category_appears_sidebar(self):
        response = self.client.get('/quiz-index-page/')
        self.assertTrue('href="/quizzes/category/food">Food</a>' in str(response.content))


    # CONTEXT TESTS

    def test_quiz_pages_in_context(self):
        response = self.client.get('/quiz-index-page/')
        self.assertTrue('quiz_pages' in response.context)

    def test_length_quiz_pages_in_context(self):
        response = self.client.get('/quiz-index-page/')
        self.assertTrue(len(response.context['quiz_pages']) == 1)

    def test_quiz_pages_first_object_is_food_quiz(self):
        response = self.client.get('/quiz-index-page/')
        first = response.context['quiz_pages'].first()
        self.assertTrue(first.title == 'Italian Food')
        self.assertTrue(first.url == '/quiz-index-page/italian-food/')

    def test_categories_sidebar_in_context(self):
        response = self.client.get('/quiz-index-page/')
        self.assertTrue('categories_sidebar' in response.context)

    # TESTS THE LATEST QUIZ VISITED IS IN CONTEXT (FROM SESSIONS)
    def test_latest_quiz_in_context(self):
        response = self.client.get('/quiz-index-page/')
        self.assertTrue('latest_quiz_visited_info' in response.context)


