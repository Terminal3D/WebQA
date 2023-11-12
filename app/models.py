from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum, F, Count, Case, When, Q
from django.utils import timezone


# Create your models here.
def sort_by_rating(queryset):
    return queryset.order_by('-question_rating__get_rating', '-created_at')


class QuestionManager(models.Manager):

    def get_hot_questions(self):
        return sort_by_rating(self.get_queryset())

    def get_new_questions(self):
        return self.get_queryset().order_by('-created_at')

    def get_questions_by_tag(self, tag_name):
        return sort_by_rating(self.get_queryset().filter(tags__tag_name=tag_name))


class TagManager(models.Manager):
    def get_top_tags(self):
        return self.get_queryset().annotate(num_questions=Count('questioninstance')).order_by('-num_questions')


class AnswerManager(models.Manager):

    def get_answers(self):
        return self.get_queryset().order_by('-answer_rating__get_rating', '-created_at')


class Tag(models.Model):
    tag_name = models.CharField(max_length=256)
    objects = TagManager()

    def __str__(self):
        return self.tag_name


class Rating(models.Model):
    get_rating = models.IntegerField(default=0)

    def __str__(self):
        return str(self.get_rating)


class Reaction(models.Model):
    reaction = models.IntegerField(default=0, help_text='-1 = dislike, 0 = no reaction, 1 = like')
    user = models.ForeignKey('Profile', on_delete=models.CASCADE)
    rating = models.ForeignKey('Rating', on_delete=models.CASCADE, related_name='reaction', null=True)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='profile_pics', default='profile_pics/default.png')

    def __str__(self):
        return self.user.get_username()


class AnswerInstance(models.Model):
    answer_body = models.TextField(blank=True, null=True)
    objects = AnswerManager()

    created_at = models.DateTimeField(default=timezone.now)
    answer_author = models.ForeignKey(Profile, on_delete=models.RESTRICT)
    answer_rating = models.OneToOneField(Rating, on_delete=models.CASCADE)
    question = models.ForeignKey('QuestionInstance', on_delete=models.CASCADE, related_name='answers')
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return 'Answer for ' + self.question.title


class QuestionInstance(models.Model):
    title = models.CharField(max_length=256, blank=True, null=True)
    question_body = models.TextField(blank=True, null=True)
    objects = QuestionManager()
    created_at = models.DateTimeField(default=timezone.now)
    question_rating = models.OneToOneField(Rating, on_delete=models.CASCADE)
    question_author = models.ForeignKey(Profile, on_delete=models.RESTRICT)
    tags = models.ManyToManyField(Tag)
    num_answers = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class BestUser(models.Model):
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    total_rating = models.IntegerField(default=0)

    def __str__(self):
        return self.profile.user.get_username() + ' (' + str(self.total_rating) + ')'
