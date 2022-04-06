import json
from coursework.models import *
import os


STORAGE_FILENAME = "storage.json"


class Storage:
    def __init__(self):
        self.clients: list[Client] = []
        self.products_for_sale: list[Product] = []

        if STORAGE_FILENAME in os.listdir():
            self.load()
        else:
            self.save()

        self.actual_client_id = -1
        self.actual_product_list = self.products_for_sale

    def save(self):
        saved_data = {"clients": [c.to_json() for c in self.clients],
                      "products_for_sale": [p.to_json() for p in self.products_for_sale]}
        with open(STORAGE_FILENAME, 'w') as file:
            json.dump(saved_data, file, indent=4)

    def load(self):
        loaded_data = {"clients": [], "products_for_sale": []}
        with open(STORAGE_FILENAME, 'r') as file:
            loaded_data = json.load(file)
        self.clients = [Client.from_json(c) for c in loaded_data["clients"]]
        self.products_for_sale = [Product.from_json(p) for p in loaded_data["products_for_sale"]]

    def add_client(self, client: Client):
        if client.is_valid(): self.clients.append(client)

    def change_actual(self, client_id):
        self.actual_client_id = client_id
        if client_id == -1:
            self.actual_product_list = self.products_for_sale
        else:
            self.actual_product_list = self.clients[client_id].products

    def remove_by_id(self, id: int):
        if self.actual_client_id == -1:
            self.products_for_sale.pop(id)
            self.actual_product_list = self.products_for_sale
        else:
            self.clients[self.actual_client_id].products.pop(id)
            self.actual_product_list = self.clients[self.actual_client_id]
