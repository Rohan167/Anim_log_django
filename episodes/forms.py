from django import forms
from .models import Item
from animes.models import anime

class ItemForm(forms.ModelForm):
    class Meta:
        model   = Item
        fields  = [
                'anime',
                'name',
                'contents',
                ]

    def __init__(self,user=None,*args,**kwargs):
        # print(kwargs.pop('user'))
        print(user)
        super(ItemForm,self).__init__(*args,**kwargs)
        self.fields['anime'].queryset = anime.objects.filter(owner=user)    
