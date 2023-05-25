from pprint import pprint
from django.shortcuts import render

import sys

sys.path.insert(0, ".")
sys.path.insert(0, "..")
sys.path.insert(0, "../..")
sys.path.insert(0, "../../..")

import database

# Create your views here.

db = database.Database()

def report(request):
    keys: list = list(list(db.get_all())[0].keys())[1:]

    pprint({
        'table_contents': [(n + 1, i) for n, i in enumerate(db.get_all())],
        'rus_names': list(db.field_table_names.find({}))[0],
        'input_fields': keys[:-1],
        'dropdown_menu_fields': [
            [keys[-1], enumerate(list(db.hardware_statuses.find({}))[0]['labels'])]
        ]
    })

    return render(request, "report_main.html", context={
        'table_contents': [(n + 1, i) for n, i in enumerate(db.get_all())],
        'rus_names': list(db.field_table_names.find({}))[0],
        'input_fields': keys[:-1],
        'dropdown_menu_fields': [
            [keys[-1], enumerate(list(db.hardware_statuses.find({}))[0]['labels'])]
        ]
    })


def form_fill(request):
    keys: list = list(list(db.get_all())[0].keys())[1:]

    return render(request, "form_fill.html", context={
        'rus_names': list(db.field_table_names.find({}))[0],
        'input_fields': keys[:-1],
        'dropdown_menu_fields': [
            [keys[-1], enumerate(list(db.hardware_statuses.find({}))[0]['labels'])]
        ]
    })