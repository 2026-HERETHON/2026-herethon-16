from django.contrib import admin

# Register your models here.
from .models import (
    Major,
    Question,
    Choice,
    ChoiceScore,
    ScoreRecord,
    Experience,
    ExperienceQuestion,
)

admin.site.register(Major)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(ChoiceScore)
admin.site.register(ScoreRecord)
admin.site.register(Experience)
admin.site.register(ExperienceQuestion)