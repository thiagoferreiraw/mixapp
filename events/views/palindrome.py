from django.shortcuts import render, redirect
from django.views.generic import View
from django.forms import ModelForm, HiddenInput
from events.models import Palindrome
from django.contrib import messages


class PalindromeForm(ModelForm):
    class Meta:
        model = Palindrome
        fields = ['word', 'is_palindrome']

    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields['is_palindrome'].widget = HiddenInput()

class PalindromeView(View):
    template_name = "events/palindrome.html"

    def get(self, request):
        return render(request, self.template_name, {'form': PalindromeForm(), 'records': Palindrome.objects.all().order_by('-id')})

    def post(self, request):
        form = PalindromeForm(self.check(request.POST))
        form.save()
        if form.cleaned_data['is_palindrome']:
            messages.success(request, f'The word "{form.cleaned_data["word"]}" is a palidrome!')
        else:
            messages.error(request, f'The word "{form.cleaned_data["word"]}" isn\'t a palidrome!')

        return redirect("palindrome")

    @staticmethod
    def check(post):
        post._mutable = True
        word = post['word'].lower().replace(" ", "")
        post['is_palindrome'] = str(word == word[::-1])
        return post




