"""forHIHITON URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LogoutView
from project.views import table, main_page, add_site, TableUpdateView, delete_table, LoginViews, delete_company, \
    TableAddView, CompanyAddView,company,all_sites

urlpatterns = [
    path('admin/', admin.site.urls, ),
    path('home/', main_page, name='main'),
    path('add_site/', add_site, name='add_site'),
    path('update_table/<int:pk>', TableUpdateView.as_view(), name='update_table'),
    path('table/', table, name='table'),
    path('table/add/', TableAddView.as_view(), name='add_table'),
    path('table/del/<int:id>', delete_table, name='del_table'),
    path('log/', LoginViews.as_view(), name='log'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('update_company/<int:pk>', TableUpdateView.as_view(), name='update_company'),
    path('company/', company, name='company'),
    path('company/del/<int:pk>', delete_company, name='del_company'),
    path('company/add/', CompanyAddView.as_view(), name='add_company'),
    path('all_site',all_sites,name='all_sites')
]
