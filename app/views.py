import random

from django.shortcuts import render
from django.core.paginator import Paginator

TAGS = [
    {
        'id': 0,
        'tag': "perl"
    },
    {
        'id': 1,
        'tag': "python"
    },
    {
        'id': 2,
        'tag': "TechnoPark"
    },
    {
        'id': 3,
        'tag': "MySQL"
    },
    {
        'id': 4,
        'tag': "django"
    },
    {
        'id': 5,
        'tag': "Mail.ru"
    },
    {
        'id': 6,
        'tag': "Voloshin"
    },
    {
        'id': 7,
        'tag': "Firefox"
    },
]

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

QUESTIONS = [
    {
        'id': i,
        'title': f'Question {i}',
        'content': f'Long lorem ipsum{i}',
        'answers_count': random.randint(1, 400),
        'tags': [
            random.choice(TAGS)['tag'] for _ in range(1, random.randint(2, 5))
        ]

    } for i in range(1, 30)
]

ANSWERS = [
    {
        'id': i,
        'content': f'Long lorem ipsum answer{i}',
    } for i in range(1, 12)
]

IS_AUTHORIZED = False


# Create your views here.

def paginate(objects, request, per_page):
    page = request.GET.get('page', 1)
    paginator = Paginator(objects, per_page)
    p = paginator.get_page(page)
    return p


def index(request):
    return render(request, 'index.html', {'questions': paginate(QUESTIONS, request, 3), 'is_hot': False})


def question(request, question_id):
    item_question = QUESTIONS[question_id - 1]
    return render(request, 'question.html', {'question': item_question, 'answers': paginate(ANSWERS, request, 5)})


def hot(request):
    sorted_questions = sorted(QUESTIONS, key=lambda x: x['answers_count'], reverse=True)
    return render(request, 'index.html', {'questions': paginate(sorted_questions, request, 3), 'is_hot': True})


def tag(request, tag_name):
    filtered_questions = [
        question for question in QUESTIONS if tag_name in question['tags']
    ]
    return render(request, 'index.html', {'questions': paginate(filtered_questions, request, 3), 'is_hot': False})


def ask(request):
    return render(request, 'ask.html')


def login(request):
    return render(request, 'login.html')


def register(request):
    return render(request, 'register.html')


def settings(request):
    return render(settings, 'settings.html')
