from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register)
from .models import QuizCategory

class QuizCategoryAdmin(ModelAdmin):
	model = QuizCategory
	menu_label = 'Quiz Category'
	menu_icon = 'folder-open-inverse'
	menu_order = 200
	add_to_settings_menu = False
	exclude_from_explorer = False
	list_display = ('name',)
	list_filter = ('name',)
	search_field = ('name')

modeladmin_register(QuizCategoryAdmin)