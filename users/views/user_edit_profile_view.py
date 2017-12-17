from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from users.forms import UserEditProfileForm, ProfileForm
from django.views.generic import View
from users.models import Category, UserCategory, Profile


class UserEditProfileView(View):
    template_name = "user_profile/profile.html"

    def get(self, request):
        categories = self._get_user_categories(request.user.id)
        form = UserEditProfileForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
        user = User.objects.filter(id=request.user.id).select_related('profile')
        return render(request, self.template_name, {
            'form': form, 
            'profile_form': profile_form,
            'categories': categories, 
            'user': request.user
        })

    def post(self, request):
        form = UserEditProfileForm(request.POST, instance=User.objects.get(pk=request.user.id))
        profile_form =ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid() and profile_form.is_valid():
            form.save(chosen_categories=request.POST.getlist('categories'))
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully')
            return redirect("edit_profile")

        categories = self._get_user_categories(request.user.id)

        return render(request, self.template_name, {
                'form': form,
                'profile_form': profile_form,
                'categories': categories,
                'user': request.user
            })

    @staticmethod
    def _get_user_categories(user_id):
        categories = Category.objects.all()
        categories = map(lambda cat: {'id': cat.id, 'name': cat.name, 'selected': False}, categories)

        user_categories = UserCategory.objects.filter(user_id_id=user_id)

        if user_categories:
            categories_ids = [cat.category_id_id for cat in user_categories]
            categories = list(
                map(lambda cat: {'id': cat['id'], 'name': cat['name'], 'selected': cat['id'] in categories_ids},
                    categories))

        return categories