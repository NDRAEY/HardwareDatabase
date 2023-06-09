import json
from pprint import pprint
from django.http import HttpResponse
from django.shortcuts import render

import sys

sys.path.insert(0, ".")
sys.path.insert(0, "..")
sys.path.insert(0, "../..")
sys.path.insert(0, "../../..")

import database

# Create your views here.

db = database.Database()

pprint(list(db.table_fields.find({}))[0])

from backend import command as command_main
from backend.data import prepare_table_fields

def report(request):
    keys: list = list(list(db.get_all())[0].keys())[1:]

    page = int(request.GET.get("p", 0))
    pagesize = int(request.GET.get("pagesize", 20))

    return render(request, "report_main.html", context={
        'table_contents': [(n + 1 + page * pagesize, i) for n, i in enumerate(db.get_from_length(page * pagesize, pagesize))],
        'page': page,
        'pagesize': pagesize,
        'page_count': db.hardware_table.count_documents({}) // pagesize,
        'fields': prepare_table_fields(db)
    })

def print_version(request):
    keys: list = list(list(db.get_all())[0].keys())[1:]

    page = int(request.GET.get("p", 0))
    pagesize = int(request.GET.get("pagesize", 20))

    return render(request, "print_version.html", context={
        'table_contents': [(n + 1 + page * pagesize, i) for n, i in enumerate(db.get_from_length(page * pagesize, pagesize))],
        'page': page,
        'pagesize': pagesize,
        'page_count': db.hardware_table.count_documents({}) // pagesize,
        'fields': prepare_table_fields(db)
    })

def command(request):
    return command_main.command(db, request)