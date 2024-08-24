from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Quiz(models.Model):
    title = models.CharField(max_length=225)
    is_ready_to_publish = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name_plural = "quizzes"

class Question(models.Model):
    text = models.CharField(max_length=225)
    quiz = models.ForeignKey(Quiz, related_name="questions", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.text

class Choice(models.Model):
    text = models.CharField(max_length=225)
    question = models.ForeignKey(Question, related_name="choices", on_delete=models.CASCADE)
    score = models.FloatField(default=0)  # количество баллов за каждый ответ

    def __str__(self) -> str:
        return self.text


class UserResponse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    test_session_id = models.CharField(max_length=50)
    date_attempted = models.DateTimeField(auto_now_add=True, blank=True)
    attempt_number = models.IntegerField(default=0)
    score = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.user.username}, попытка {self.attempt_number}. Ответ на вопрос {self.question.text}, из теста {self.quiz.title}: {self.selected_choice.text}."

    def calculate_score(self):
        total_score = sum(choice.score for choice in self.question.choice.all())
        return total_score

    def local_date_completed(self):
        return timezone.localtime(self.date_completed)

class TestResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    total_score = models.IntegerField()
    date_completed = models.DateTimeField(auto_now_add=True)

    def local_date_completed(self):
        return timezone.localtime(self.date_completed)





