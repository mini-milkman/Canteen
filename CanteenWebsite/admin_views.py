from django.template import RequestContext
from django.shortcuts import render_to_response
from CanteenWebsite.utils.functions import setting_get, setting_set
from CanteenWebsite.utils.functions import setting_get_json, setting_set_json
from django.contrib.admin.views.decorators import staff_member_required
from .admin_forms import OptionsForm, DataImportForm


@staff_member_required
def general_options(request):
    if request.method == 'POST':
        form = OptionsForm(request.POST)
        if form.is_valid():
            pass
    else:
        form = OptionsForm()
    return render_to_response('admin/general_options.html',
                              {'form': form})


@staff_member_required
def data_import_options(request):
    if request.method == 'POST':
        form = DataImportForm(request.POST)
        if form.is_valid():
            pass
    else:
        form = DataImportForm()
    return render_to_response('admin/data_import_options.html',
                              {'form': form})
