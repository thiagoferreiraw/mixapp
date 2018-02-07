from django.shortcuts import render
from events.models import Language
from django.views.generic import View

from users.models import UserLanguage


class ModeratorSetupView(View):
    template_name = "moderator_flow/moderator_setup.html"

    def get(self, request):
        return render(request, self.template_name, {'languages': Language.objects.all(),})

    def post(self, request):
        languages = request.POST.getlist('languages')

        if len(languages) < 2:
            raise Exception("You need to speak more than one language")

        UserLanguage.objects.filter(user_id=request.user.id).delete()
        for language in request.POST.getlist('languages'):
            user_language = UserLanguage(user_id_id=request.user.id, language_id_id=language)
            user_language.save()

        #return render(request, self.template_name, {'languages': Language.objects.all(),})



