# Mini Quiz App

A web app created with Django and Wagtail.  

## OVERVIEW
- A web app that allows the site visitor to browse an index of quizzes, an index of categories, quizzes inside a category and hide and reveal answers on each quiz page.
- The user can create quizzes, give an introduction to each quiz, assign multiple categories and create and re-order questions inside each quiz,  

## DESIGN FEATURES
- The 'quizzes' app models make use of a combination of the Wagtail page ecosystem and standard Django models.  Quizzes are Wagtail pages, categories are Django models, and quiz questions are 'Orderables' that are created inside a quiz page.

- Quiz categories are displayed in the user admin separately from the 'Pages' directory. This is acheived using the 'modeladmin' classes.

- The site admin uses django views and urls for category detail pages and category list pages.

- Template tags are used to save code re-use.  Different tags are used for different page sidebars. 
A sidebar of quizzes is used in the category list page and a sidebar of categories is used on quiz pages and the quiz index page. 

- JS is used for the quiz page to hide and reveal answers on click.

- The homepage makes use of template tags that are also used in other areas of the site.

- Bootstrap grid is used for the layout of pages and the website color scheme.
