from django.contrib import admin
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from .admin_forms import OptionsForm, DataImportOptionForm, DataImportForm


class CanteenAdminSite(admin.AdminSite):
    site_header = '站点设置'

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
        return render_to_response('admin/base.html',
                                  {'adminform': form},
                                  RequestContext(request, {}))

    def data_import_options(self, request):
        if request.method == 'POST':
            form = DataImportOptionForm(request.POST)
            if form.is_valid():
                return HttpResponse("Data Import Options")
        else:
            form = DataImportOptionForm()
        return render_to_response('admin/change_form.html',
                                  {'adminform': form},
                                  RequestContext(request, {}))

    def data_import(self, request):
        if request.method == 'POST':
            form = DataImportForm(request.POST)
            if form.is_valid():
                return HttpResponse("Data Import")
        else:
            form = DataImportForm()
        return render_to_response('admin/change_form.html',
                                  {'adminform': form},
                                  RequestContext(request, {}))


canteen_admin_site = CanteenAdminSite()
