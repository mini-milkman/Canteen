from django.template import RequestContext
from django.shortcuts import render_to_response
from CanteenWebsite.utils.functions import setting_get, setting_set
from CanteenWebsite.utils.functions import setting_get_json, setting_set_json
from django.contrib.admin.views.decorators import staff_member_required
from .admin_forms import OptionsForm, DataImportOptionForm, DataImportForm
from django.contrib import admin
from django.contrib.admin import AdminSite
from django.http import HttpResponse
from .models import Category
from .models import Goods
from .models import Setting


class CanteenAdminSite(AdminSite):
    site_header = 'Monty Python administration'

    def get_urls(self):
        from django.conf.urls import url
        urls = super(CanteenAdminSite, self).get_urls()
        urls += [
            url(r'^general_options/$', self.admin_view(self.general_options), name="general_options"),
            url(r'^data_import_options/$', self.admin_view(self.data_import_options), name="data_import_options"),
            url(r'^data_import/$', self.admin_view(self.data_import), name="data_import")
        ]
        return urls

    def general_options(self, request):
        if request.method == 'POST':
            form = OptionsForm(request.POST)
            if form.is_valid():
                return HttpResponse("General Options")
        else:
            form = OptionsForm()
        return render_to_response('admin/change_form.html',
                                  {'form': form},
                                  request)

    def data_import_options(self, request):
        if request.method == 'POST':
            form = DataImportOptionForm(request.POST)
            if form.is_valid():
                return HttpResponse("Data Import Options")
        else:
            form = DataImportOptionForm()
        return render_to_response('admin/change_form.html',
                                  {'form': form},
                                  request)

    def data_import(self, request):
        if request.method == 'POST':
            form = DataImportOptionForm(request.POST)
            if form.is_valid():
                return HttpResponse("Data Import")
        else:
            form = DataImportOptionForm()
        return render_to_response('admin/change_form.html',
                                  {'form': form},
                                  request
                                  )


canteen_admin_site = CanteenAdminSite()
