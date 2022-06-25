from django import forms

class AddSiteForm(forms.Form):
    URL = forms.CharField(label = 'URL')
    news = forms.CharField(label = 'news')
    title = forms.CharField(label = 'title')
    date = forms.CharField(label = 'date')
    text = forms.CharField(label = 'text')