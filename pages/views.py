from django.shortcuts import render

def index(request):
      return render(request, "index.html", {})

def index2(request):
      return render(request, "index2.html", {})

def find(request):
      return render(request, "find.html", {})