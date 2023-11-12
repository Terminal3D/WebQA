import random

from django.core.paginator import Paginator
from django.shortcuts import render
from app.models import QuestionInstance, AnswerInstance, Tag

BEST_MEMBERS = [
    {
        'id': 0,
        'name': "Mr. Freeman"
    },
    {
        'id': 1,
        'name': "Dr. House"
    },
    {
        'id': 2,
        'name': "Bender"
    },
    {
        'id': 3,
        'name': "Queen Victoria"
    },
    {
        'id': 4,
        'name': "V. Pupkin"
    },
]


# Create your views here.

def paginate(objects, request, per_page):
    page = request.GET.get('page', 1)
    paginator = Paginator(objects, per_page)
    return paginator.get_page(page)


def index(request):
    new_questions = QuestionInstance.objects.get_new_questions()
    return render(request, 'index.html', {'questions': paginate(new_questions, request, 20), 'is_hot': False})


def question(request, question_id):
    item_question = QuestionInstance.objects.get(id=question_id)
    answers = item_question.answers.all()
    return render(request, 'question.html', {'question': item_question, 'answers': paginate(answers, request, 30)})


def hot(request):
    hot_questions = QuestionInstance.objects.get_hot_questions()
    return render(request, 'index.html', {'questions': paginate(hot_questions, request, 20), 'is_hot': True})


def tag(request, tag_name):
    filtered_questions = QuestionInstance.objects.get_questions_by_tag(tag_name)
    return render(request, 'index.html', {'questions': paginate(filtered_questions, request, 20), 'is_hot': False})


def ask(request):
    return render(request, 'ask.html')


def login(request):
    return render(request, 'login.html')


def register(request):
    return render(request, 'register.html')


def settings(request):
    return render(request, 'settings.html')
