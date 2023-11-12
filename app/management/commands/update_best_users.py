from django.db.models import Q, F, Sum, Case, When, Value, Subquery, OuterRef
from datetime import timedelta
from django.utils import timezone
from app.models import QuestionInstance, AnswerInstance, Tag, Rating, Reaction, Profile, BestUser
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Updates the list of best users'

    def get_best_users(self):
        one_week_ago = timezone.now() - timedelta(weeks=1)

        question_ratings = Rating.objects.filter(
            questioninstance__created_at__gte=one_week_ago
        ).annotate(
            total_rating=Sum('reaction__reaction')
        )

        answer_ratings = Rating.objects.filter(
            answerinstance__created_at__gte=one_week_ago
        ).annotate(
            total_rating=Sum('reaction__reaction')
        )

        # Связываем рейтинги с пользователями
        top_authors = Profile.objects.annotate(
            total_rating=Subquery(
                question_ratings.filter(questioninstance__question_author=OuterRef('pk')).values('total_rating')[:1]
            ) + Subquery(
                answer_ratings.filter(answerinstance__answer_author=OuterRef('pk')).values('total_rating')[:1]
            )
        ).order_by('-total_rating')[:10]
        return top_authors

    def handle(self, *args, **kwargs):
        best_users = self.get_best_users()
        BestUser.objects.all().delete()
        BestUser.objects.bulk_create([
            BestUser(profile=user, total_rating=user.total_rating) for user in best_users
        ])

        self.stdout.write(self.style.SUCCESS('Successfully updated best users'))
