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
    'type': {'type': 'dropdown', 'show': 'Тип', 'elements': DEFAULT_HARDWARE_TYPES},
    'vendor': {'type': 'input', 'show': 'Производитель'},
    'model': {'type': 'input', 'show': 'Модель'},
    'serial': {'type': 'input', 'show': 'Серийный номер'},
    'status': {'type': 'dropdown', 'show': 'Статус', 'elements': DEFAULT_STATUSES},
    'description': {'type': 'textbox', 'show': 'Описание'},
}

metadata = {
    'statuses': DEFAULT_STATUSES,
    'hardware_types': DEFAULT_HARDWARE_TYPES
}

class Hardware:
    def __init__(self, inv_num, type_, vendor, model, serial, description, status = "Нет"):
        self.inv_num = inv_num
        self.type = type_
        self.vendor = vendor
        self.model = model
        self.serial = serial

        if status not in table_fields['status']['elements']:
            raise ValueError(f"Status does not exist: '{status}'")

        self.status = status
        self.description = description

class Database:
    def __init__(self) -> None:
        try:
            self.config = toml.load("../config.toml")['server']
        except:
            self.config = toml.load("config.toml")['server']


        self.addr = self.config['address']

        self.connection = pymongo.MongoClient(self.addr)

        self.db = self.connection.hardware

        self.hardware_table = self.db.hwtable
        self.table_fields = self.db.table_fields
        self.metadata = self.db.metadata

    def setup(self):
        self.table_fields.insert_one(table_fields)
        self.metadata.insert_one(metadata)

    # For debugging
    def clean_db(self):
        "Remove every collection data to make a clean DB"
        self.table_fields.delete_many({})
        self.hardware_table.delete_many({})
        self.metadata.delete_many({})

    def is_inv_num_free(self, num: int):
        return not (num in [i['inv_num'] for i in self.get_all()])

    def add_hardware(self, hardware: Hardware):
        # INV NUMS should not repeat!

        print("Add hw")

        invs = [i['inv_num'] for i in self.get_all()]

        if hardware.inv_num in invs:
            raise ValueError("Inventory number should not repeat! (Hint: Delete device and add device again)")

        self.hardware_table.insert_one(hardware.__dict__)

    def get_all(self):
        return self.hardware_table.find()

    def get_by_vendor(self, vendor: str):
        return [i for i in self.hardware_table.find() if i['vendor'].lower() == vendor.lower()]
    
    def get_by_name(self, name: str):
        return [i for i in self.hardware_table.find() if i['name'].lower() == name.lower()]
    
    def get_by_model(self, model: str):
        return [i for i in self.hardware_table.find() if i['model'].lower() == model.lower()]
    
    def get_by_serial(self, serial: str):
        return [i for i in self.hardware_table.find() if i['serial'].lower() == serial.lower()]
    
    def get_by_status(self, status: int):
        return [i for i in self.hardware_table.find() if i['status'] == status]

    def get_by_inv_num(self, inv_num: int):
        return [i for i in self.hardware_table.find() if i['inv_num'] == inv_num]

    def get_by_type(self, type_: str):
        return [i for i in self.hardware_table.find() if i['type'].lower() == type_.lower()]


if __name__ == "__main__":
    db = Database()

    db.clean_db()
    db.setup()

    hw =  Hardware(800, "ПК", "Rammer", "PowerBook Zeraora V2", "MZ0000001", "CPU: Intel Core i3")
    hw2 = Hardware(801, "Маршрутизатор", "Besk", "Lannive QA Plus", "AWN-100566632", "WiFi 6 included!")
    hw3 = Hardware(802, "Монитор", "Overture", "Emix A2", "XSPN-111111111", "4K resuolution in 60 fps!")
    hw4 = Hardware(803, "Проектор", "Overture", "Avenue 2", "XSPN-367293224", "Projector with high resolution and strong light")
    hw5 = Hardware(804, "ПК", "Rammer", "Woundhealer E1", "MZ847284364", "With water cooling!")
    hw6 = Hardware(805, "Жесткий диск", "ByteSaver", "LAVI-W", "UT0102223", "2 TB Hard Drive 100 MB/s")

    for i in (hw, hw2, hw3, hw4, hw5, hw6):
        db.add_hardware(i)
