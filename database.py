import pymongo
import toml

DEFAULT_STATUSES = ["Нет", "Списано", "Утилизировано"]
DEFAULT_HARDWARE_TYPES = [
    "ПК",
    "Принтер",
    "Камера видеонаблюдения",
    "Монитор",
    "Аудиосистема",
    "Монитор",
    "Проектор",
    "Маршрутизатор"
]

table_fields = {
    'inv_num': {'type': 'input', 'show': 'Инвертарный номер'},
    'type': {'type': 'dropdown', 'show': 'Тип', 'elements': "metadata.hardware_types"},
    'vendor': {'type': 'input', 'show': 'Производитель'},
    'model': {'type': 'input', 'show': 'Модель'},
    'serial': {'type': 'input', 'show': 'Серийный номер'},
    'status': {'type': 'dropdown', 'show': 'Статус', 'elements': "metadata.statuses"},
    'employee': {'type': 'dropdown', 'show': 'Отвественный', 'elements': "employees"},
    'description': {'type': 'textbox', 'show': 'Описание'},
}

employees_table_fields = {
    'surname': {'type': 'input', 'show': 'Фамилия'},
    'name': {'type': 'input', 'show': 'Имя'},
    'patronymic': {'type': 'input', 'show': 'Отчество'},
    'hpart_name': {'type': 'dropdown', 'show': 'Отдел', 'elements': "hparts.name"}
}

hparts_table_fields = {
    'id': {'type': 'input', 'show': 'ID'},
    'name': {'type': 'input', 'show': 'Название'},
}

metadata = {
    'statuses': DEFAULT_STATUSES,
    'hardware_types': DEFAULT_HARDWARE_TYPES
}

class Hardware:
    def __init__(self, inv_num, type_, vendor, model, serial, description, employee, status = "Нет"):
        self.inv_num = inv_num
        self.type = type_
        self.vendor = vendor
        self.model = model
        self.serial = serial
        self.status = status
        self.employee = employee
        self.description = description

class HPart:
    def __init__(self, id, name):
        self.id = id
        self.name = name

class Employee:
    def __init__(self, id, surname, name, patronymic, hpart_id):
        self.id = id
        self.surname = surname
        self.name = name
        self.patronymic = patronymic
        self.hpart_id = hpart_id

class Database:
    def __init__(self) -> None:
        try:
            self.config = toml.load("../config.toml")['server']
        except:
            self.config = toml.load("config.toml")['server']


        self.addr = self.config['address']

        self.connection = pymongo.MongoClient(self.addr)

        self.db = self.connection.hardware

        self.hardware_table = self.db.hwtable  # Устройства
        self.table_fields = self.db.table_fields  # Описание полей таблиц
        self.metadata = self.db.metadata  # Дополнительные данные

        self.employees = self.db.employees  # Сотрудники
        self.employees_table_fields = self.db.employees_table_fields  # Сотрудники
        
        self.hparts = self.db.hparts  # Отделы
        self.hparts_table_fields = self.db.hparts_table_fields  # Сотрудники

    # Настройка
    def setup(self):
        self.table_fields.insert_one(table_fields)
        self.employees_table_fields.insert_one(employees_table_fields)
        self.hparts_table_fields.insert_one(hparts_table_fields)
        self.metadata.insert_one(metadata)

    # Очистка всей БД
    def clean_db(self):
        "Remove every collection data to make a clean DB"
        self.table_fields.delete_many({})
        self.employees_table_fields.delete_many({})
        self.hparts_table_fields.delete_many({})

        self.hardware_table.delete_many({})
        self.metadata.delete_many({})
        
        self.employees.delete_many({})
        self.hparts.delete_many({})

    def is_inv_num_free(self, num: int):
        return not (num in [i['inv_num'] for i in self.get_all()])

    def get_hpart_id_by_name(self, name: str):
        for i in self.hparts.find({}):
            if i["name"] == name:
                return i["id"]

    def evaluate_fields(self, fields_name):
        "Evaluate links in values"

        if not list(self.db[fields_name].find({})):
            return {}

        # Get data from `fields_name`
        data: dict = list(self.db[fields_name].find({}))[0]

        # Go through data and if we get string in `elements` key, get following field (by string) from db.
        for k, v in data.items():
            if type(v) is dict and v['type'] == "dropdown":
                # FIXME
                if k == "hpart_name":
                    data[k]['elements'] = [i['name'] for i in self.hparts.find({})]
                    continue
                elif k == "employee":
                    data[k]["elements"] = [f"{i['surname']} {i['name']} {i['patronymic']}" for i in self.employees.find({})]
                    continue

                keys = v['elements'].split(".")

                temp = list(self.db[keys[0]].find({}))[0]
                del keys[0]

                for i in keys:
                    temp = temp[i]
                
                data[k]['elements'] = temp
        
        del data['_id']

        return data

    def add_hardware(self, hardware: Hardware):
        # INV NUMS should not repeat!

        invs = [i['inv_num'] for i in self.get_all()]

        if hardware.inv_num in invs:
            raise ValueError(f"Inventory number should not repeat! (Hint: Delete device and add device again) [{hardware.inv_num}]")

        self.hardware_table.insert_one(hardware.__dict__)

    def add_hpart(self, hpart: HPart):
        self.hparts.insert_one(hpart.__dict__)

    def add_employee(self, employee: Employee):
        if employee.id in [i['id'] for i in self.employees.find()]:
            raise ValueError(f"Employee ID should not repeat! ({employee.id})")
            
        self.employees.insert_one(employee.__dict__)

    def get_all(self):
        return self.hardware_table.find()

    def get_from_length(self, start, length):
        return self.hardware_table.find().skip(start).limit(length)

    # def get_by_vendor(self, vendor: str):
    #     return [i for i in self.hardware_table.find() if i['vendor'].lower() == vendor.lower()]
    
    # def get_by_name(self, name: str):
    #     return [i for i in self.hardware_table.find() if i['name'].lower() == name.lower()]
    
    # def get_by_model(self, model: str):
    #     return [i for i in self.hardware_table.find() if i['model'].lower() == model.lower()]
    
    # def get_by_serial(self, serial: str):
    #     return [i for i in self.hardware_table.find() if i['serial'].lower() == serial.lower()]
    
    # def get_by_status(self, status: int):
    #     return [i for i in self.hardware_table.find() if i['status'] == status]

    # def get_by_inv_num(self, inv_num: int):
    #     return [i for i in self.hardware_table.find() if i['inv_num'] == inv_num]

    # def get_by_type(self, type_: str):
    #     return [i for i in self.hardware_table.find() if i['type'].lower() == type_.lower()]


if __name__ == "__main__":
    db = Database()

    db.clean_db()
    db.setup()

    # for n, i in enumerate(("ABC", "DEF", "GHI")):
    #     db.add_hpart(HPart(n, i))

    # for n, i in enumerate(("Clark", "Max", "Drew", "Eric", "Mark", "David")):
    #     db.add_employee(Employee(n, "Markin", i, "Eduardovich", 0))

    # db.add_employee(Employee(99, "Thunder", "Zeraora", "-----------", 1))

    # for i in range(15):
    #     hw_ = Hardware(800 + i, "Аудиосистема", "ByteSaver", "LAVI-W", "UT0" + str(i), "2 TB Hard Drive 100 MB/s", "Thunder Zeraora ------------")

    #     db.add_hardware(hw_)
