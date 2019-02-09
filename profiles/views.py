from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, View, CreateView
from django.http import Http404
from django.contrib.auth import get_user_model
from animes.models import anime
from episodes.models import Item
from .models import Profile
from .forms import RegisterForm
# Create your views here.

User    = get_user_model()



class RegisterView(CreateView):
    form_class      = RegisterForm
    template_name   = 'registration/register.html'
    success_url = '/'

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            return redirect('/logout')
        return super(RegisterView, self).dispatch(*args, **kwargs)

class ProfileFollowToggle(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        # print(request.data)
        username_to_toggle  = request.POST.get('username')
        print(username_to_toggle)
        profile_p, is_following = Profile.objects.toggle_follow(request.user, username_to_toggle)
        print(is_following)
        # profile_p = Profile.objects.get(user__username__iexact=user_to_toggle)
        # user    = request.user
        # if user in profile_p.followers.all():
        #     profile_p.followers.remove(user)
        # else:
        #     profile_p.followers.add(user)

        return redirect(f'/profiles/{profile_p.user.username }/')


class ProfileDetail(DetailView):
    template_name   = 'profiles/user.html'

    def get_object(self):
        username        = self.kwargs.get("username")
        if username is None:
            raise Http404
        return get_object_or_404(User, username__iexact=username, is_active=True)

    def get_context_data(self,*args, **kwargs):
        context = super(ProfileDetail, self).get_context_data(*args, **kwargs)
        user = context['user']
        is_following = False
        if user.profile in self.request.user.is_following.all():
            is_following = True
        context['is_following'] = is_following
        query = self.request.GET.get('q')
        item_exists = Item.objects.filter(user=user).exists()
        qs = anime.objects.filter(owner=user)
        if query:
            qs = qs.search(query)

        if item_exists and qs.exists():
            context['anime'] = qs
        return context
