from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db.models import F

from app.models import QuestionInstance, AnswerInstance, Tag, QuestionReaction, AnswerReaction, Profile
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
        self.update_ratings()

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
                question_author=question_author,
                title=f'Question Title{i + 1}',
                question_body=f'Question number: {i + 1} , from user: {question_author}.',
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
                answer_body=f'Answer for question with id: {question.id}, from user: {answer_author}. Answer num: {i}'
            ))
            QuestionInstance.objects.filter(id=question.id).update(num_answers=F('num_answers') + 1)
        AnswerInstance.objects.bulk_create(answer_objects)

    def create_tags(self, num_tags):
        tag_objects = [Tag(tag_name=f'Tag {i}') for i in range(num_tags) if
                       not Tag.objects.filter(tag_name=f'Tag {i}').exists()]
        Tag.objects.bulk_create(tag_objects)

    def create_ratings(self, num_ratings):
        profiles = list(Profile.objects.all())
        questions = list(QuestionInstance.objects.all())
        answers = list(AnswerInstance.objects.all())

        question_reactions_set = set()
        answer_reactions_set = set()
        question_reactions = []
        answer_reactions = []

        for _ in range(num_ratings):
            profile = random.choice(profiles)
            if random.choice(['question', 'answer']) == 'question':
                question = random.choice(questions)
                if (profile.id, question.id) not in question_reactions_set:
                    reaction_value = random.choice([-1, 1, 1, 1, 1])
                    question_reactions.append(QuestionReaction(
                        user=profile,
                        question=question,
                        reaction=reaction_value
                    ))
                    question_reactions_set.add((profile.id, question.id))
            else:
                answer = random.choice(answers)
                if (profile.id, answer.id) not in answer_reactions_set:
                    reaction_value = random.choice([-1, 1, 1, 1, 1])
                    answer_reactions.append(AnswerReaction(
                        user=profile,
                        answer=answer,
                        reaction=reaction_value
                    ))
                    answer_reactions_set.add((profile.id, answer.id))

        QuestionReaction.objects.bulk_create(question_reactions)
        AnswerReaction.objects.bulk_create(answer_reactions)

    def update_ratings(self):
        for question in QuestionInstance.objects.all():
            likes = QuestionReaction.objects.filter(question=question, reaction=1).count()
            dislikes = QuestionReaction.objects.filter(question=question, reaction=-1).count()
            question.question_rating = likes - dislikes
            question.save()

        for answer in AnswerInstance.objects.all():
            likes = AnswerReaction.objects.filter(answer=answer, reaction=1).count()
            dislikes = AnswerReaction.objects.filter(answer=answer, reaction=-1).count()
            answer.answer_rating = likes - dislikes
            answer.save()
