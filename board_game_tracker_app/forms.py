from django import forms

class AddGameForm(forms.Form):
  title = forms.CharField()
  image = forms.ImageField()