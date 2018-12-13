from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.views.generic import TemplateView, ListView
from django.db.models import Q
from .models import anime


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

class anime_list_view(ListView):
    template_name = 'animes/anime.html'
    def get_queryset(self):
        slug = self.kwargs.get("slug")
        if slug:
            queryset = anime.objects.filter(

            Q(genre__icontains=slug)|
            Q(genre__iexact=slug)

            )
        else:
            return anime.objects.all()
        return queryset
