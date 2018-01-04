from django.shortcuts import render

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

def feedbackdetails(request):
      return render(request, "feedback-details.html", {})