from django import template
from quizzes.models import QuizCategory

register = template.Library()

@register.inclusion_tag("tags/get_latest_categories.html")
def get_latest_categories():
	latest_categories = QuizCategory.objects.all()[:50]
	return {
	    'latest_categories': latest_categories
	}

@register.inclusion_tag("tags/get_all_categories.html")
def get_all_categories():
	all_categories = QuizCategory.objects.all()
	return {
	    'all_categories': all_categories
	}