from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView
from django.db.models import Q
from .models import anime
from .forms import anime_form, anime_model_form


# Create your views here.
# def home(request):
#     return HttpResponse("Welcome!")
    # return render(request,"home.html",{})  #response
# def anime_list(request):
#     template_name = 'animes/anime_list.html'
#     queryset = anime.objects.all()
#     context = {
#                 "object_list":queryset
#               }
#     return render(request, template_name, context)

@login_required(login_url='/login/')
def anime_create_view(request):
    template_name = 'animes/anime_form.html'
    form = anime_model_form(request.POST or None)
    errors = None
        # title =   request.POST.get('title')
        # genre =   request.POST.get('genre')
        # review =   request.POST.get('review')
    if form.is_valid():
        if request.user.is_authenticated():
            instance = form.save(commit=False)
            instance.owner = request.user
            instance.save()
            # obj = anime.objects.create(
            #             name = form.cleaned_data.get('name'),
            #             genre = form.cleaned_data.get('genre'),
            #             review = form.cleaned_data.get('review'),
            #
            # )
            return HttpResponseRedirect('/animes/')
        else:
            return HttpResponseRedirect('/login/')
    else:
        errors = form.errors
    context = {"form":form, "errors":errors}
    return render(request, template_name, context)



class anime_list_view(LoginRequiredMixin,ListView):
    template_name = 'animes/anime.html'
    def get_queryset(self):
        return anime.objects.filter(owner=self.request.user)



class anime_detail_view(LoginRequiredMixin,DetailView):
    template_name = 'animes/anime_detail.html'
    def get_queryset(self):
        return anime.objects.filter (owner=self.request.user)


    # def get_object(self, *args, **kwargs):
    #     anime_id = self.kwargs.get('anime_id')
    #     obj = get_object_or_404(anime, id=anime_id)
    #     return obj


class anime_createview_class(LoginRequiredMixin,CreateView):
    form_class = anime_model_form
    template_name = 'form.html'
    login_url = '/login/'
    success_url = '/animes/'

    def form_valid(form,self):
        instance = form.save(commit=False)
        instance.owner = self.request.user
        return super(anime_createview_class, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(anime_createview_class, self).get_context_data(*args,**kwargs)
        context['title'] = 'Add Anime'
        return context


class anime_updateview_class(LoginRequiredMixin,UpdateView):
    form_class = anime_model_form
    template_name = 'form.html'
    login_url = '/login/'
    # success_url = '/animes/'

    def get_context_data(self, *args, **kwargs):
        context = super(anime_updateview_class, self).get_context_data(*args,**kwargs)
        name    = self.get_object().name
        context['title'] = f'Update Anime: {name}'
        return context

    def get_queryset(self):
        return anime.objects.filter (owner=self.request.user)
