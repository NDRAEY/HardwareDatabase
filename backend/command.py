from copy import deepcopy
from backend.check import check_data, check_data_change
from django.http import HttpResponse
import database
import json

def command(db, request):
    # Get parameters
    cmd = request.GET.get("cmd", None)
    print("COMMAND", cmd)
    
    # Convert to normal dict
    other_data = dict(request.GET)

    # And delete cmd to select only needed data
    del other_data["cmd"]

    orig_data = deepcopy(other_data)

    # Converting all array values to string values in data
    for i in other_data.keys():
        other_data[i] = other_data[i][0]
    
    # Do something with data we got

    if cmd == "new":
        # Check data, NOTE: None is good
        check = check_data(db, other_data)

        if not (check is None):
            return HttpResponse(json.dumps({
                "ok": False,
                "message": check
            }))

        # Add hardware
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
        # Remove hardware by inventory number.
        db.hardware_table.delete_one({
            "inv_num": int(other_data["inv_num"])
        })

        print(f"Remove: {other_data['inv_num']}")

    elif cmd == "edit":
        "Get old and new data, and update data."
        old_datas = dict((k, v[0]) for k, v in orig_data.items())
        new_datas = dict((k, v[1]) for k, v in orig_data.items())

        # Check data, NOTE: None is good
        check = check_data_change(db, old_datas, new_datas)

        if not (check is None):
            return HttpResponse(json.dumps({
                "ok": False,
                "message": check
            }))

        old_datas['inv_num'] = int(old_datas['inv_num'])
        new_datas['inv_num'] = int(new_datas['inv_num'])

        print("OLD", old_datas)
        print("NEW", new_datas)

        db.hardware_table.update_one(old_datas, {'$set': new_datas})

    # To edit entry we need to use .update() (in MongoDB shell) method what receives query and datas to edit.

    # JSON response
    return HttpResponse(json.dumps({
        "ok": True
    }))
