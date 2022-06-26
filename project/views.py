from django.shortcuts import render, redirect
from .models import Company, TableAnalyzeCompany
from .forms import AddSiteForm, Analyze, TableAnalyzeCompanyForm, AuthUserForm, CompanyForm
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
import json
from django.contrib.auth.views import LoginView
import os
from parsing.parse import parse_and_save
from screenshots.screenshots import get_zip_by_company_name

# Create your views here.

json_sites = {}


def main_page(request):
    if request.method == 'POST':
        form = Analyze(request.POST)
        if form.is_valid():
            if form.cleaned_data["keywords"]:
                ok, comp_name = parse_and_save(form.cleaned_data["URL"], form.cleaned_data["keywords"].split(','))
            else:
                ok, comp_name = parse_and_save(url=form.cleaned_data["URL"])
            if ok:
                company_name = Company.objects.get(name=comp_name)
                zip = get_zip_by_company_name(company_name)
                excel = getTableExcel()
                # return redirect('table')
                return render(request, 'main_page.html',
                              {'user': request.user, 'form': form, 'zip': zip, 'excel': excel})
            else:
                pass
        # TODO err
    else:
        form = Analyze()
    return render(request, 'main_page.html', {'user': request.user, 'form': form, 'zip': '', 'excel': ''})


import pandas as pd
from datetime import datetime

def getTableExcel():
    data_news = [str(x[0]) for x in TableAnalyzeCompany.objects.all().values_list("date_news")]
    name_news = [x[0] for x in TableAnalyzeCompany.objects.all().values_list("name_news")]
    name_title_news = [x[0] for x in TableAnalyzeCompany.objects.all().values_list("name_title_news")]
    url = [x[0] for x in TableAnalyzeCompany.objects.all().values_list("url")]
    category = [x[0] for x in TableAnalyzeCompany.objects.all().values_list("category")]
    company_name = [Company.objects.get(cat_id=x[0]) for x in TableAnalyzeCompany.objects.all().values_list("company_name")]

    data = pd.DataFrame(
        {"Дата": data_news, "Наименвование компании": company_name, "Название ресурса": name_news,
         "Заголовок новости": name_title_news, "Ссылка": url,
         "Категория": category})
    filename = 'files/created' + str(datetime.date(datetime.now())) + '.xlsx'
    data.to_excel(filename, sheet_name='datasheet', index=False)
    return filename

def all_sites(request):
    urlMassive = [i['URL'] for i in json_sites['sites']]
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

        #print(json_sites)
        return redirect('main')

    else:
        form = AddSiteForm()

    return render(request, 'add_site_page.html', {'form': form})


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
