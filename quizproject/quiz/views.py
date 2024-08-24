from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib import messages
from datetime import datetime
from django.utils import timezone
from random import randint
from .models import Quiz, Choice, UserResponse, TestResult
import uuid
import pytz
import os

def index(request):
    quizzes = Quiz.objects.filter(is_ready_to_publish = True)
    context = {"quizzes":quizzes, }
    return render(request, "index.html", context=context)

@login_required(login_url='login')
def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()
    context = {"quiz":quiz, "questions":questions}
    return render(request, "quiz_detail.html", context)

@login_required(login_url='login')
def quiz_submit(request, quiz_id):

    if request.method == "POST":
        quiz = get_object_or_404(Quiz, id=quiz_id)
        questions = quiz.questions.all()
        error_message = None
        test_session_id = randint(1000, 9999)
        utc_now = datetime.utcnow()
        utc_now = utc_now.replace(tzinfo=pytz.UTC)
        moscow_timezone = pytz.timezone('Europe/Moscow')
        moscow_time = utc_now.astimezone(moscow_timezone)
        date_attempted = moscow_time

        for question in questions:
            answer = request.POST.get(str(question.id))
            choice_id = request.POST.get(f"question_{question.id}", None)
            if choice_id:
                choice = get_object_or_404(Choice, id=choice_id)
                UserResponse.objects.create(
                    user=request.user,
                    quiz=quiz,
                    question=question,
                    selected_choice=choice,
                    test_session_id=test_session_id,
                    date_attempted=date_attempted,
                    attempt_number=test_session_id,
                )
            else:
                error_message = "Необходимо выбрать ответ для каждого вопроса!"

        if error_message:
            messages.error(request, error_message)
            context={"quiz":quiz, "questions":questions}
            return render(request, "quiz_detail.html", context)

        messages.success(request, "ТЕСТ ПРОЙДЕН")
        total_score = 0
        response_info = []
        user_responses = UserResponse.objects.filter(user=request.user,quiz_id=quiz_id, attempt_number=test_session_id,)
        i = 0
        for user_response in user_responses:
            response = {
                "quiz": user_response.quiz.title,
                "question": user_response.question.text,
                "question_id": user_response.question.id,
                "selected_choice": user_response.selected_choice.text,
                "score": user_response.selected_choice.score,
                "date_time": user_response.date_attempted,

            }
            i = i + 1
            total_score += user_response.selected_choice.score
            response_info.append(response)

        test_result = TestResult.objects.create(user=request.user, quiz=quiz, total_score=total_score)

        context = {
            "response_info": response_info,
            "total_score": total_score,
            "test_session_id": test_session_id,
            "date_attempted": date_attempted,
            "i": i,
        }

        return render(request, "results_info.html", context)

@login_required(login_url='login')
def answers_detail(request,quiz_id):
    user_responses = UserResponse.objects.filter(user=request.user,quiz_id=quiz_id)
    total_score = 0
    total_questions = 0
    response_info = []
    i = 0
    for user_response in user_responses:
        response = {
            "quiz": user_response.quiz.title,
            "question": user_response.question.text,
            "question_id": user_response.question.id,
            "selected_choice": user_response.selected_choice.text,
            "score": user_response.selected_choice.score,
            "date_time": user_response.date_attempted,

        }
        i = i + 1
    total_score += user_response.selected_choice.score
    response_info.append(response)
    test_result = TestResult.objects.create(user=request.user, quiz=quiz,)

    context = {
        "response_info": response_info,
        "total_score": total_score,
        "test_session_id": test_session_id,
        "date_attempted": date_attempted,
        "i": i,
    }

    return render(request, "results_info.html", context)



def python_info(request):
    return render(request, "python_info.html")



def knowledge_base(request):
    return render(request, "knowledge_base.html")


