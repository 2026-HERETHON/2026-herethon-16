from django.shortcuts import render, get_object_or_404, redirect
from .models import Question, ScoreRecord, ChoiceScore, Experience, ExperienceQuestion

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



# "추천 전공 - 1"
def recommend1(request):
    record = ScoreRecord.objects.filter(user=request.user).order_by("-score").first()
    major = record.major
    experience = major.experiences.first()
    context = {
        "recommendation": {
            "userName": request.user.username,
            "majorName": major.name,
            "shortDescription": major.description,
            "iconAssetKey": "/static/assets/major1.svg",
            "tags": [major.tag1, major.tag2, major.tag3],
            "reasons": [major.reason],
            "trial": {
                "title": experience.title,
                "image": "/static/assets/experience1.svg",
                "taskSummary": experience.taskSummary,
                "durationMin": experience.durationMin,
                "deliverableName": experience.deliverableName,
                "id": experience.order,
            },
        }
    }
    return render(request, "recommend1.html", context)


# "체험수업 - 1"
def experience1(request):
    record = ScoreRecord.objects.filter(user=request.user).order_by("-score").first()
    major = record.major
    experience = major.experiences.first()
    questions = experience.questions.order_by("order")
    context = {
        "experience": {
            "title": experience.title,
            "description":experience.introText
        },
        "questions": questions,
    }
    return render(request, "experience1.html", context)

# "추천 전공 - 2"
def recommend2(request):
    records = ScoreRecord.objects.filter(user=request.user).order_by("-score")
    major = records[1].major
    experience = major.experiences.first()
    context = {
        "recommendation": {
            "userName": request.user.username,
            "majorName": major.name,
            "shortDescription": major.description,
            "iconAssetKey": "/static/assets/major2.svg",
            "tags": [major.tag1, major.tag2, major.tag3],
            "reasons": [major.reason],
            "trial": {
                "title": experience.title,
                "image": "/static/assets/experience2.svg",
                "taskSummary": experience.taskSummary,
                "durationMin": experience.durationMin,
                "deliverableName": experience.deliverableName,
                "id": experience.order,
            },
        }
    }
    return render(request, "recommend2.html", context)

# "체험수업 - 2"
def experience2(request):
    records = ScoreRecord.objects.filter(user=request.user).order_by("-score")
    major = records[1].major
    experience = major.experiences.first()
    questions = experience.questions.order_by("order")
    context = {
        "experience": {
            "title": experience.title,
            "description":experience.introText
        },
        "questions": questions,
    }
    return render(request, "experience2.html", context)

# "전공 선택하기 (비교 선택)"
def confirm(request):
    records = ScoreRecord.objects.filter(user=request.user).order_by("-score")[:2]
    majors = [
        {
            "name": records[0].major.name,
            "className": records[0].major.experiences.first().title
        },
        {
            "name": records[1].major.name,
            "className": records[1].major.experiences.first().title
        }
    ]
    
    context = {
        "steps": ["첫번째 전공 체험", "두번째 전공 체험", "비교·선택"],
        "majors": majors,
    }

    return render(request, "confirm.html", context)
