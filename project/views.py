from django.shortcuts import render, redirect
from .models import Company, TableAnalyzeCompany
from .forms import AddSiteForm, Analyze, TableAnalyzeCompanyForm, AuthUserForm, CompanyForm
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
import json
from django.contrib.auth.views import LoginView
import os
import pandas as pd
from datetime import datetime

# Create your views here.

json_sites = {}


def main_page(request):
    al_company = Company.objects.all().values_list('other_name')
    print(al_company)
    if request.method == 'POST':
        form = Analyze(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            return redirect('main')
    else:
        form = Analyze()
    return render(request, 'main_page.html', {'user': request.user, 'company': al_company, 'form': form})


def all_sites(request):
    urlMassive = [i['URL'] for i in json_sites['sites']]
    print(urlMassive)
    return render(request, 'all_sites.html', {'sites': urlMassive})


def add_site(request):
    if request.method == 'POST':
        form = AddSiteForm(request.POST)
        if form.is_valid():
            for i in json_sites['sites']:
                if i['URL'] == form.cleaned_data['URL']:
                    break
                else:
                    json_sites['sites'].append(form.cleaned_data)
                    with open('static/sites.json', 'w') as j:
                        json.dump(json_sites, j)
                    break

        print(json_sites)
        return redirect('main')

    else:
        form = AddSiteForm()

    return render(request, 'add_site_page.html', {'form': form})

def getTableExcel():
    data_news = TableAnalyzeCompany.objects.raw('select date_news from project_tableanalyzecompany')
    name_news = TableAnalyzeCompany.objects.raw('select name_news from project_tableanalyzecompany')
    name_title_news = TableAnalyzeCompany.objects.raw('select name_title_news from project_tableanalyzecompany')
    url = TableAnalyzeCompany.objects.raw('select url from project_tableanalyzecompany')
    category = TableAnalyzeCompany.objects.raw('select category from project_tableanalyzecompany')

    data = pd.DataFrame({TableAnalyzeCompany.date_news.verbose_name:data_news, TableAnalyzeCompany.name_news.verbose_name:name_news,
                         TableAnalyzeCompany.name_title_news.verbose_name:name_title_news,TableAnalyzeCompany.url.verbose_name:url,
                         TableAnalyzeCompany.category.verbose_name:category})
    data.to_excel('files/created'+str(datetime.now())+'.xlsx', sheet_name='datasheet', index=False)

def table(request):
    tac = TableAnalyzeCompany.objects.all()
    return render(request, 'table_page.html', {'table': tac, 'user': request.user})


class TableAddView(CreateView):
    template_name = 'add_table.html'
    form_class = TableAnalyzeCompanyForm
    model = TableAnalyzeCompany
    success_url = reverse_lazy('table')


class TableUpdateView(UpdateView):
    model = TableAnalyzeCompany
    template_name = 'table_update_page.html'
    fields = ['company_name', 'date_news', 'name_news', 'name_title_news', 'url', 'category']
    success_url = reverse_lazy('table')


def delete_table(request, id):
    if request.user.is_authenticated:
        tac = TableAnalyzeCompany.objects.get(id=id)
        tac.delete()
        return redirect('table')
    else:
        return reverse_lazy('main')


class LoginViews(LoginView):
    template_name = 'registration/login.html'
    form_class = AuthUserForm
    success_url = reverse_lazy('main')


class CompanyAddView(CreateView):
    template_name = 'add_company.html'
    form_class = CompanyForm
    model = Company
    success_url = reverse_lazy('company')


def delete_company(request, pk):
    if request.user.is_authenticated:
        company = Company.objects.get(pk=pk)
        company.delete()
        return redirect('company')
    else:
        return reverse_lazy('main')


class CompanyUpdateView(UpdateView):
    model = Company
    template_name = 'company_update_page.html'
    fields = ['cat_id', 'name', 'phone', 'email', 'about', 'category']
    success_url = reverse_lazy('table')


def company(request):
    al_company = Company.objects.all()
    return render(request, 'company_page.html', {'user': request.user, 'company': al_company})
