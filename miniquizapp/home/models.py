from django.db import models

from wagtail.core.models import Page


class HomePage(Page):
    def get_context(self, request):
    	context = super().get_context(request)
    	if 'most_recent_quiz_title' in request.session:
    		context['most_recent_quiz_title'] = request.session['most_recent_quiz_title']
    		context['most_recent_quiz_url'] = request.session['most_recent_quiz_url']
    	return context


