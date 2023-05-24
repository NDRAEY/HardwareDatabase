import pymongo
import toml

field_to_name_dict = {
    'inv_num': 'Инвертарный номер',
    'vendor': 'Производитель',
    'model': 'Модель',
    'type': 'Тип',
    'serial': 'Серийный номер',
    'status': 'Статус'
}

out_of_service_labels = ["Нет", "Списано", "Утилизировано"]

class DeviceStatus:
    NORMAL = 0
    OUT_OF_SERVICE = 1
    UTILIZED = 2
    
    def __init__(self, status):
        self.status = status


class Hardware:
    def __init__(self, inv_num, type_, vendor, model, serial, status = DeviceStatus.NORMAL):
        self.inv_num = inv_num
        self.type = type_
        self.vendor = vendor
        self.model = model
        self.serial = serial
        self.status = status


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
        self.hardware_statuses = self.db.statuses
        self.field_table_names = self.db.field_db_names

    def setup(self):
        self.field_table_names.delete_many({}) # Delete all
        self.field_table_names.insert_one(field_to_name_dict)

        self.hardware_statuses.delete_many({}) # Delete all
        self.hardware_statuses.insert_one({"labels": out_of_service_labels})

    def add_hardware(self, hardware: Hardware):
        # INV NUMS should not repeat!

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

    db.setup()

    hw =  Hardware(800, "Ноутбук", "Rammer", "PowerBook Zeraora V2", "MZ0000001")
    hw2 = Hardware(801, "Маршрутизатор", "Besk", "Lannive QA Plus", "AWN-100566632")
    hw3 = Hardware(802, "Монитор", "Overture", "Emix A2", "XSPN-111111111")
    hw4 = Hardware(803, "Проектор", "Overture", "Avenue 2", "XSPN-367293224")
    hw5 = Hardware(804, "Системный блок", "Rammer", "Woundhealer E1", "MZ847284364")
    hw6 = Hardware(805, "Жесткий диск", "ByteSaver", "LAVI-W", "UT0102223")

    for i in (hw, hw2, hw3, hw4, hw5, hw6):
        db.add_hardware(i)
