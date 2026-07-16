from django import template
from django.utils import timezone

register = template.Library()

@register.filter
def simple_timesince(value):
    now = timezone.now()
    diff = now - value

    seconds = diff.total_seconds()
    hours = int(seconds // 3600)
    days = diff.days

    if days >= 1:
        return f"{days}일 전"
    elif hours >= 1:
        return f"{hours}시간 전"
    else:
        minutes = int(seconds // 60)
        if minutes >= 1:
            return f"{minutes}분 전"
        return "방금 전"