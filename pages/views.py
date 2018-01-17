from django.shortcuts import render
from events.models import Category, EventTemplate


def index(request):
    return render(request, "index.html", {})


def index2(request):
    return render(request, "index2.html", {})


def find(request):
    return render(request, "find.html", {})


def mixdetails(request):
    return render(request, "mix-details.html", {})


def feedback(request):
    return render(request, "feedback.html", {})


def translations_test(request):
    return render(request, "translations.html",
                  {'language': request.LANGUAGE_CODE,
                   'categories': Category.objects.all(),
                   'templates': EventTemplate.objects.all()})


def feedbackdetails(request):
    return render(request, "feedback-details.html", {})

