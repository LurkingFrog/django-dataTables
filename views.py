from django.http import HttpResponse

from django.core.context_processors import csrf
from django.shortcuts import render

from data_tables.forms import JQueryDataTable


def ajax_get_records(request):
    """
    Builds the json required by the jquery dataTable
    plugin
    """

    form = JQueryDataTable.get_datatable_form(request.POST)
    if form.is_valid():
        return HttpResponse(
            form.dumps,
            mimetype="application/json"
        )

    else:
        print form.errors
        return HttpResponse(
            form.errors,
            status=500,
            mimetype="text/html"
        )


def ajax_do_action(request):
    """
    This will dynamically handle the buttons that can be added at the bottom
    of the datatable (Add / Edit / Delete)
    """
    pass
