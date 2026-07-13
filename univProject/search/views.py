from django.shortcuts import render, get_object_or_404, redirect
from .models import Question, ScoreRecord, ChoiceScore

# Create your views here.
def intro(request):
    return render(request, "intro.html")

def select1(request):
    question = get_object_or_404(Question, order=1)
    choices = question.choices.all()

    context = {
        "question": question,
        "choices": choices
    }

    return render(request, "select1.html", context)

def select2(request):
    question = get_object_or_404(Question, order=2)
    choices = question.choices.all()

    context = {
        "question": question,
        "choices": choices
    }

    return render(request, "select2.html", context)

def select3(request):
    question = get_object_or_404(Question, order=3)
    choices = question.choices.all()

    context = {
        "question": question,
        "choices": choices
    }

    return render(request, "select3.html", context)

def loading(request):
    return render(request, "loading.html")

def submitAnswer(request):
    if request.method == "POST":
        choice_id = request.POST.get("choice_id")
        scores = ChoiceScore.objects.filter(choice_id=choice_id)

        for s in scores:            
            records = ScoreRecord.objects.filter(user=request.user, major=s.major)
            if records.exists():
                record = records.first()
            else:
                record = ScoreRecord(user=request.user, major=s.major, score=0)
            record.score = record.score + s.score
            record.save()
        next_url = request.POST.get("next_url", "loading")
        return redirect(next_url)


def resultView(request):
    records = ScoreRecord.objects.filter(user=request.user).order_by("-score")
    topMajors = [record.major for record in records[:2]]
    context = {
        'topMajors': topMajors,
        'userName': request.user.username,
    }

    return render(request, "confirm.html", context)