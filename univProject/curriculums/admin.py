from django.contrib import admin
from .models import (
    Stage, Lesson, LessonScreen, LessonQuestion, LessonAnswer,
    LessonProgress, LessonReflection)


class LessonQuestionInline(admin.TabularInline):
    model = LessonQuestion
    extra = 1


class LessonScreenInline(admin.StackedInline):
    model = LessonScreen
    fk_name = 'lesson' 
    extra = 0


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('lesson_id', 'stage', 'order', 'title', 'is_experiential')
    inlines = [LessonQuestionInline, LessonScreenInline]


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1


@admin.register(Stage)
class StageAdmin(admin.ModelAdmin):
    list_display = ('stage_id', 'major', 'order', 'title', 'deliverable_name')
    inlines = [LessonInline]


admin.site.register(LessonAnswer)
admin.site.register(LessonProgress)
admin.site.register(LessonReflection)