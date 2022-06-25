from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import TableAnalyzeCompany,Company


class AddSiteForm(forms.Form):
    URL = forms.URLField(label='URL')
    news = forms.URLField(label='news')
    title = forms.CharField(label='title')
    date = forms.CharField(label='date')
    text = forms.CharField(label='text')


class Analyze(forms.Form):
    URL = forms.URLField(label='URL')
    keywords = forms.CharField(label='keywords')


class TableAnalyzeCompanyForm(ModelForm):
    class Meta:
        model = TableAnalyzeCompany
        fields = ('company_name', 'date_news', 'name_news', 'name_title_news', 'url', 'category')

class AuthUserForm(AuthenticationForm, forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')

class CompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = ('cat_id', 'name', 'phone', 'email', 'about', 'category')