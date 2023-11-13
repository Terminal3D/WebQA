from django.contrib import admin

# Register your models here.

from .models import AnswerInstance, QuestionInstance, Profile, Tag, BestUser, QuestionReaction, AnswerReaction


class QuestionReactionInline(admin.TabularInline):
    model = QuestionReaction
    extra = 1


class AnswerReactionInline(admin.TabularInline):
    model = AnswerReaction
    extra = 1


class AnswerInstanceInline(admin.TabularInline):
    model = AnswerInstance
    extra = 1


class QuestionInstanceAdmin(admin.ModelAdmin):
    inlines = [QuestionReactionInline, AnswerInstanceInline]


class AnswerInstanceAdmin(admin.ModelAdmin):
    inlines = [AnswerReactionInline]


admin.site.register(AnswerInstance, AnswerInstanceAdmin)
admin.site.register(QuestionInstance, QuestionInstanceAdmin)
admin.site.register(Profile)
admin.site.register(Tag)
admin.site.register(BestUser)
admin.site.register(QuestionReaction)
admin.site.register(AnswerReaction)
