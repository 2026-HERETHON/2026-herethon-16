from django.shortcuts import render

# Create your views here.
def intro(request):
    return render(request, "intro.html")

def select1(request):
    return render(request, "select1.html")

def select2(request):
    return render(request, "select2.html")

def select3(request):
    return render(request, "select3.html")

def loading(request):
    return render(request, "loading.html")