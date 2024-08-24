from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:quiz_id>", views.quiz_detail, name="quiz_detail"),
    path("<int:quiz_id>/submit", views.quiz_submit, name="quiz_submit"),
    path("<int:quiz_id>/submit/detail", views.answers_detail, name='answers_detail'),
    path("python_info", views.python_info, name='python_info'),
    path("knowledge_base", views.knowledge_base, name='knowledge_base'),
]



