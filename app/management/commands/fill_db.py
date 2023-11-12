from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import QuestionInstance, AnswerInstance, Tag, Rating, Reaction, Profile
import random


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int)

    def handle(self, *args, **kwargs):
        ratio = kwargs.get('ratio')
        num_users = ratio
        num_questions = ratio * 10
        num_answers = ratio * 100
        num_tags = ratio
        num_ratings = ratio * 200
        self.create_tags(num_tags)
        self.create_users(num_users)
        self.create_questions(num_questions)
        self.create_answers(num_answers)
        self.create_ratings(num_ratings)

    def create_users(self, num_users):
        user_objects = []
        for i in range(num_users):
            username = f'profile{i}'
            if not User.objects.filter(username=username).exists():
                user = User(username=username)
                user.set_password(f'password{i}')
                user_objects.append(user)

        created_users = User.objects.bulk_create(user_objects)
        Profile.objects.bulk_create([Profile(user=user) for user in created_users])

    def create_questions(self, num_questions):
        profiles = list(Profile.objects.all())
        tags = list(Tag.objects.all())
        question_objects = []
        for i in range(num_questions):
            question_author = random.choice(profiles)
            tmpQuestion = QuestionInstance(
                question_rating=Rating.objects.create(),
                question_author=question_author,
                title=f'Question Title{i}',
                question_body=f'Question number: {i}, from user: {question_author}.',
            )
            question_objects.append(tmpQuestion)
        created_questions = QuestionInstance.objects.bulk_create(question_objects)

        for question in created_questions:
            selected_tags = random.sample(tags, random.randint(1, 3))
            question.tags.set(selected_tags)

    def create_answers(self, num_answers):
        questions = list(QuestionInstance.objects.all())
        profiles = list(Profile.objects.all())
        answer_objects = []
        for i in range(num_answers):
            question = random.choice(questions)
            answer_author = random.choice(profiles)
            answer_objects.append(AnswerInstance(
                question=question,
                answer_author=answer_author,
                answer_rating=Rating.objects.create(),
                answer_body=f'Answer for question with id: {question.id}, from user: {answer_author}. Answer num: {i}'
            ))
        AnswerInstance.objects.bulk_create(answer_objects)

    def create_tags(self, num_tags):
        tag_objects = [Tag(tag_name=f'Tag {i}') for i in range(num_tags) if
                       not Tag.objects.filter(tag_name=f'Tag {i}').exists()]
        Tag.objects.bulk_create(tag_objects)

    def create_ratings(self, num_ratings):
        profiles = list(Profile.objects.all())
        ratings = list(Rating.objects.all())
        reaction_objects = []
        for i in range(num_ratings):
            reaction_objects.append(Reaction(
                user=random.choice(profiles),
                reaction=random.choice([-1, 1, 1, 1, 1]),
                rating=random.choice(ratings)
            ))
        Reaction.objects.bulk_create(reaction_objects)
