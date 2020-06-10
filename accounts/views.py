from django.shortcuts import render, redirect
from django.views.generic import (
    UpdateView,
    DetailView,
    DeleteView
)
from django.contrib.auth.models import User

from guardian.mixins import PermissionRequiredMixin, LoginRequiredMixin

from accounts.forms import SignUpForm, UserForm
from accounts.models import Profile


# Create your views here.
def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    elif request.POST:
        form = SignUpForm(request.POST)

        if form.is_valid():
            form.save()

        return redirect('home')
    else:
        form = SignUpForm()

    return render(request, 'accounts/register.html', {'form': form})


class ProfileDetails(DetailView):
    template_name = 'accounts/profile.html'
    model = User
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(pk=self.kwargs.get('pk'))
        published_article_count = user.article_set.filter(
            published=True).count()
        context['published_articles'] = published_article_count
        return context


class UpdateProfile(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'accounts.change_profile'

    template_name = 'accounts/update_profile.html'
    model = User
    form_class = UserForm


class DeleteProfile(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'accounts.delete_profile'
    accept_global_perms = True

    model = Profile
