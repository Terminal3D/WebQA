import random

from django.core.paginator import Paginator, EmptyPage
from django.http import Http404, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from app.models import QuestionInstance, AnswerInstance, Tag


# Create your views here.

def paginate(objects, request, per_page):
    page = request.GET.get('page', 1)
    paginator = Paginator(objects, per_page)
    try:
        return paginator.page(page)
    except EmptyPage:
        return None


def handle_not_found(request):
    return HttpResponseNotFound(render(request, '404.html'))


def index(request):
    new_questions = QuestionInstance.objects.get_new_questions()
    paginated_questions = paginate(new_questions, request, 20)
    if paginated_questions is None:
        return handle_not_found(request)
    return render(request, 'index.html', {'questions': paginated_questions, 'is_hot': False})


def question(request, question_id):
    try:
        item_question = QuestionInstance.objects.get(id=question_id)
    except QuestionInstance.DoesNotExist:
        return handle_not_found(request)
    answers = item_question.answers.get_answers()
    paginated_answers = paginate(answers, request, 30)
    if paginated_answers is None:
        return handle_not_found(request)
    return render(request, 'question.html', {'question': item_question, 'answers': paginate(answers, request, 30)})


def hot(request):
    hot_questions = QuestionInstance.objects.get_hot_questions()
    paginated_questions = paginate(hot_questions, request, 20)
    if paginated_questions is None:
        return handle_not_found(request)
    return render(request, 'index.html', {'questions': paginated_questions, 'is_hot': True})


def tag(request, tag_name):
    filtered_questions = QuestionInstance.objects.get_questions_by_tag(tag_name)
    paginated_questions = paginate(filtered_questions, request, 20)
    if paginated_questions is None:
        return handle_not_found(request)
    return render(request, 'index.html', {'questions': paginated_questions, 'is_hot': False})


def ask(request):
    return render(request, 'ask.html')


def login(request):
    return render(request, 'login.html')


def register(request):
    return render(request, 'register.html')


def settings(request):
    return render(request, 'settings.html')
