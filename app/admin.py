from django.contrib import admin

# Register your models here.

from .models import AnswerInstance, QuestionInstance, Rating, Profile, Tag, Reaction, BestUser


class ReactionInline(admin.TabularInline):
    model = Reaction
    extra = 1


class AnswerInstanceInline(admin.TabularInline):
    model = AnswerInstance
    extra = 1


class QuestionInstanceAdmin(admin.ModelAdmin):
    inlines = [AnswerInstanceInline]


class RatingAdmin(admin.ModelAdmin):
    inlines = [ReactionInline]


admin.site.register(AnswerInstance)
admin.site.register(QuestionInstance, QuestionInstanceAdmin)
admin.site.register(Rating, RatingAdmin)
admin.site.register(Profile)
admin.site.register(Tag)
admin.site.register(Reaction)
admin.site.register(BestUser)
