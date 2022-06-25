from django.shortcuts import render, redirect
from .models import Company
from .forms import AddSiteForm

import json
import os

# Create your views here.

json_sites = {}


def main_page(request):
    al_company = Company.objects.all()

    return render(request, 'main_page.html', {'user': request.user, 'company': al_company})


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
