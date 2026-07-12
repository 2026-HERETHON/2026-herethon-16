from django.contrib import admin
from .models import Stage, Lesson, UserLessonProgress, MotivationMessage

admin.site.register(Stage)
admin.site.register(Lesson)
admin.site.register(UserLessonProgress)
admin.site.register(MotivationMessage)