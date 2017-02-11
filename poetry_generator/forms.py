from django import forms

from .models import Inspiration, Poem

#
# class PoemForm(forms.Form):
#     inspiration_text = forms.CharField(label='Inspiration text', max_length=1000)


class InspirationForm(forms.ModelForm):

    class Meta:
        model = Inspiration
        fields = ('input_text', 'template')