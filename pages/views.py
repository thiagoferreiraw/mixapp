from django.utils.translation import gettext as _, gettext
from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, "index.html", {})


def index2(request):
    return render(request, "index2.html", {})


def find(request):
    return render(request, "find.html", {})


def feedback(request):
    return render(request, "feedback.html", {})


def translations_test(request):
    # output = gettext("Welcome to my site.")
    #print(output)
    return render(request, "translations.html", {})
