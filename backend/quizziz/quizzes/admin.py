from django.contrib import admin

from .models import (
    Quiz,
    QuizFeedback,
    QuizPunctation,
    Question,
    Category,
    PsychologyResults,
    Answer
)


class QuizAdmin(admin.ModelAdmin):
    model = Quiz,
    readonly_fields = ('id', 'slug',)


class QuizPunctationAdmin(admin.ModelAdmin):
    model = QuizPunctation
    readonly_fields = ('id', 'slug',)


class PsychologyResultsAdmin(admin.ModelAdmin):
    model = QuizPunctation
    readonly_fields = ('id', 'slug',)


class AnswerAdmin(admin.ModelAdmin):
    model = Answer
    readonly_fields = ('id', 'slug',)


class QuestionAdmin(admin.ModelAdmin):
    model = Question
    readonly_fields = ('id', 'slug',)


admin.site.register(Quiz, QuizAdmin)
admin.site.register(QuizFeedback)
admin.site.register(QuizPunctation, QuizPunctationAdmin)
admin.site.register(PsychologyResults, PsychologyResultsAdmin)
admin.site.register(Category)


admin.site.register(Question, QuestionAdmin)

admin.site.register(Answer, AnswerAdmin)
