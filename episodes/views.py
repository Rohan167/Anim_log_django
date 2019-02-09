from django.shortcuts import render
from .models import Item
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, View
from .forms import ItemForm
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


class HomeView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return render(request, 'home.html', {})

        user = request.user
        is_following_user_ids = [x.user.id for x in user.is_following.all()]
        qs = Item.objects.filter(user__id__in=is_following_user_ids, public=True)
        return render(request, 'episodes/home-feed.html', {'object_list':qs})



class ItemListView(LoginRequiredMixin,ListView):

    def get_queryset(self):
        return Item.objects.filter(user=self.request.user)


class ItemDetailView(LoginRequiredMixin,DetailView):

    def get_queryset(self):
        return Item.objects.filter(user=self.request.user)


class ItemCreateView(LoginRequiredMixin, CreateView):
    template_name = 'form.html'
    form_class  = ItemForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        return super(ItemCreateView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(ItemCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_queryset(self):
        return Item.objects.filter(user=self.request.user)

    def get_context_data(self, *args, **kwargs):
        context = super(ItemCreateView, self).get_context_data(*args,**kwargs)
        context['title'] = 'Add Episode'
        return context


class ItemUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'form.html'
    form_class  = ItemForm
    def get_queryset(self):
        return Item.objects.filter(user=self.request.user)

    def get_context_data(self, *args, **kwargs):
        context = super(ItemUpdateView, self).get_context_data(*args,**kwargs)
        context['title'] = 'Update Episode'
        return context

    def get_form_kwargs(self):
        kwargs = super(ItemUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
