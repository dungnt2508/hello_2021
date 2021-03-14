from pymongo import MongoClient

client = MongoClient(port=27017)
db = client.app_demo

db.settings.insert_many([{
                    "kind_item": "1",
                    "item_name": "Cầm giấy tờ",
                    "rate": "1",
                    "service_charge": "7",
                    "storage_charge": "7",
                    "status": "1"
                }, {
                    "kind_item": "2",
                    "item_name": "Cầm xe máy chính chủ",
                    "rate": "1",
                    "service_charge": "1",
                    "storage_charge": "4",
                    "status": "1"
                }, {
                    "kind_item": "3",
                    "item_name": "Cầm xe máy không chính chủ",
                    "rate": "1",
                    "service_charge": "10",
                    "storage_charge": "4",
                    "status": "1"
                }, {
                    "kind_item": "4",
                    "item_name": "Cầm điện thoại, Ipad, Laptop",
                    "rate": "1",
                    "service_charge": "7",
                    "storage_charge": "4",
                    "status": "1"
                }, {
                    "kind_item": "5",
                    "item_name": "Cầm oto chính chủ",
                    "rate": "1",
                    "service_charge": "1",
                    "storage_charge": '4',
                    "status": "1"
                }, {
                    "kind_item": "6",
                    "item_name": "Cầm oto không chính chủ",
                    "rate": "1",
                    "service_charge": "7",
                    "storage_charge": "7",
                    "status": "1"
                }, {
                    "kind_item": "7",
                    "item_name": "Cầm oto ngân hàng chính chủ",
                    "rate": "1",
                    "service_charge": "5",
                    "storage_charge": "4",
                    "status": "1"
                }, {
                    "kind_item": "8",
                    "item_name": "Cầm nhà đất",
                    "rate": "1",
                    "service_charge": "3",
                    "storage_charge": "0",
                    "status": "1"
                }, {
                    "kind_item": "9",
                    "item_name": "Cầm nhà đất ngân hàng",
                    "rate": "1",
                    "service_charge": "3",
                    "storage_charge": "0",
                    "status": "1"
                }])