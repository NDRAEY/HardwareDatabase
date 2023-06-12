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

from backend import command as command_main

def report(request):
    page = int(request.GET.get("p", 0))
    pagesize = int(request.GET.get("pagesize", 20))

    return render(request, "report_main.html", context={
        'table_contents': [(n + 1 + page * pagesize, i) for n, i in enumerate(db.get_from_length(page * pagesize, pagesize))],
        'page': page,
        'pagesize': pagesize,
        'page_count': db.hardware_table.count_documents({}) // pagesize,
        'fields': db.evaluate_fields('table_fields')
    })

def print_version(request):
    page = int(request.GET.get("p", 0))
    pagesize = int(request.GET.get("pagesize", 20))

    return render(request, "print_version.html", context={
        'table_contents': [(n + 1 + page * pagesize, i) for n, i in enumerate(db.get_from_length(page * pagesize, pagesize))],
        'page': page,
        'pagesize': pagesize,
        'page_count': db.hardware_table.count_documents({}) // pagesize,
        'fields': db.evaluate_fields('table_fields')
    })

def employees(request):
    employees = list(db.employees.find({}))
    hparts = list(db.hparts.find({}))

    # Set name of HPart for every employee based on HPart's ID
    for n, _ in enumerate(employees):
        for i in hparts:
            if i['id'] == employees[n]['hpart_id']:
                employees[n]['hpart_name'] = i['name']
                break

    return render(request, "employees.html", context={
        'table_contents': employees,
        'fields': db.evaluate_fields('employees_table_fields')
    })

def hparts(request):
    hp = list(db.hparts.find({}))

    return render(request, "hparts.html", context={
        'table_contents': hp,
        'fields': db.evaluate_fields('hparts_table_fields')
    })

def command(request):
    return command_main.command(db, request)