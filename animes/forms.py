from django import forms
from .models import anime


class anime_form(forms.Form):
        name        = forms.CharField()
        genre       = forms.CharField(required=False)
        review      = forms.CharField(required=False)

        # def clean_name(self):
        #     name = self.cleaned_data.get('name')
        #     if len(name) < 4:
        #         raise forms.ValidationError("Minimum Length 4 for name field")
        #     return name


class anime_model_form(forms.ModelForm):
    # email = forms.EmailField()
    class Meta:
        model = anime
        fields = [
                    'name',
                    'genre',
                    'review',
                ]
    # def clean_name(self):
    #     name = self.cleaned_data.get('name')
    #     if len(name) < 4:
    #         raise forms.ValidationError("Minimum Length 4 for name field")
    #     return self.name
