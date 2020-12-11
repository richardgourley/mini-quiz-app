from django import template
from quizzes.models import QuizCategory, QuizPage

register = template.Library()

@register.inclusion_tag("tags/get_all_categories.html")
def get_all_categories():
	all_categories = QuizCategory.objects.all()
	return {
	    'all_categories': all_categories
	}

@register.inclusion_tag("tags/get_categories_sidebar.html")
def get_categories_sidebar():
	categories_sidebar = QuizCategory.objects.all()
	return {
	    'categories_sidebar': categories_sidebar
	}

@register.inclusion_tag("tags/get_questions_sidebar.html")
def get_questions_sidebar():
	questions_sidebar = QuizPage.objects.live()
	return {
	    'questions_sidebar': questions_sidebar
	}

@register.inclusion_tag("tags/get_latest_quizzes.html")
def get_latest_quizzes():
	latest_quizzes = QuizPage.objects.live()[:8]
	return {
	    'latest_quizzes': latest_quizzes
	}