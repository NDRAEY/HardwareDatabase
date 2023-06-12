def check_data(db, data):
    "Return problematic field if error was occured, None on success"

    if not data["inv_num"]:
        return "inv_num"
    if not (data["inv_num"].isdigit() and db.is_inv_num_free(int(data["inv_num"]))):
        return "inv_num"
    if not data["type"]:
        return "type"
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
    if not data["employee"]:
        return "employee"
    if data["employee"] not in [f"{i['surname']} {i['name']} {i['patronymic']}" for i in db.employees.find({})]:
        return "employee"
    if not data['description']:
        return "description"


def check_data_change(db, old, new):
    "Return problematic field if error was occured, None on success (but with checks for changed inv_num)"

    if (not new["inv_num"]) or (not new["inv_num"].isdigit()):
        return "inv_num"
    if (not db.is_inv_num_free(int(new["inv_num"]))) and new["inv_num"] != old["inv_num"]:
        return "inv_num"
    if not new['vendor']:
        return "vendor"
    if not new["type"]:
        return "type"
    if not new['model']:
        return "model"
    if new["type"] not in list(db.metadata.find({}))[0]['hardware_types']:
        return "type"
    if not new['serial']:
        return "serial"
    if new["status"] not in list(db.metadata.find({}))[0]['statuses']:
        return "status"
    if new["employee"] not in [f"{i['surname']} {i['name']} {i['patronymic']}" for i in db.employees.find({})]:
        return "employee"
    if not new['description']:
        return "description"

def check_employee(db, data):
    if not data["surname"]:
        return "surname"
    if not data["name"]:
        return "name"
    if not data["patronymic"]:
        return "patronymic"
    if (data["hpart_name"] not in [i['name'] for i in db.hparts.find({})]):
        return "hpart_name"

def check_hpart(db, data):
    if (not data["id"]) or (not data["id"].isdigit()):
        return "id"
    if int(data["id"]) in [i['id'] for i in db.hparts.find({})]:
        return "id"
    if not data["name"]:
        return "name"
    