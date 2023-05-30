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

def prepare_table_fields():
    fields = list(db.table_fields.find({}))[0]

    del fields['_id']

    return fields

def report(request):
    keys: list = list(list(db.get_all())[0].keys())[1:]

    return render(request, "report_main.html", context={
        'table_contents': [(n + 1, i) for n, i in enumerate(db.get_all())],
        'fields': prepare_table_fields()
    })


def check_data(data):
    "Return problematic field if error was occured, None on success"

    if not data["inv_num"]:
        return "inv_num"
    if not (data["inv_num"].isdigit() and db.is_inv_num_free(int(data["inv_num"]))):
        return "inv_num"
    if not data['vendor']:
        return "vendor"
    if not data['model']:
        return "model"
    if data["type"] not in list(db.metadata.find({}))[0]['hardware_types']:
        return "type"
    if not data['serial']:
        return "serial"
    if data["status"] not in list(db.metadata.find({}))[0]['statuses']:
        return "status"
    if not data['description']:
        return "description"


def command(request):
    print("=======================GOT A COMMAND")
    print(request.GET)

    # Get parameters
    cmd = request.GET.get("cmd", None)
    
    # COnvert to normal dict
    other_data = dict(request.GET)

    # And delete cmd to select only needed data
    del other_data["cmd"]

    # Converting all array values to string values in data
    for i in other_data.keys():
        other_data[i] = other_data[i][0]

    # Do something with data we got

    if cmd == "new":
        # Check data, NOTE: None is good
        check = check_data(other_data)

        if not (check is None):
            return HttpResponse(json.dumps({
                "ok": False,
                "message": check
            }))

        db.add_hardware(database.Hardware(
            int(other_data['inv_num']),
            other_data['type'],
            other_data['vendor'],
            other_data['model'],
            other_data['serial'],
            other_data['description'],
            other_data['status']
        ))
    elif cmd == "del":
        db.hardware_table.delete_one({
            "inv_num": int(other_data["inv_num"])
        })

        print(f"Remove: {other_data['inv_num']}")

    # To edit entry we need to use .update() method what receives query and datas to edit.

    # JSON response
    return HttpResponse(json.dumps({
        "ok": True
    }))
