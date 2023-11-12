from django.contrib import admin

# Register your models here.

from .models import AnswerInstance, QuestionInstance, Rating, Profile, Tag, Reaction, BestUser

admin.site.register(AnswerInstance)
admin.site.register(QuestionInstance)
admin.site.register(Rating)
admin.site.register(Profile)
admin.site.register(Tag)
admin.site.register(Reaction)
admin.site.register(BestUser)
