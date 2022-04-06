import collections
import datetime
from datetime import date, timedelta

TIME_FORMAT = "%Y-%m-%d"


class Client:
    next_id = 0

    def __init__(self, name: str, surname: str, age: int, pass_num: int):
        self.id = Client.next_id
        Client.next_id += 1

        self.name = name.strip()
        self.surname = surname.strip()
        self.age = age
        self.pass_num = pass_num
        self.products: list[Product] = []

    def is_valid(self) -> bool:
        return len(self.name) > 0 \
               and len(self.surname) > 0 \
               and self.age > 17 \
               and len(str(self.pass_num)) < 8

    def to_json(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "surname": self.surname,
            "age": self.age,
            "pass_num": self.pass_num,
            "products": [p.to_json() for p in self.products]
        }

    @staticmethod
    def from_json(jsoned_client: dict):
        client = Client(
            name=jsoned_client["name"],
            surname=jsoned_client["surname"],
            age=jsoned_client["age"],
            pass_num=jsoned_client["pass_num"],
        )
        client.id = jsoned_client["id"]
        client.next_id = client.id if client.id > client.next_id else client.next_id
        client.products = [Product.from_json(p) for p in jsoned_client["products"]]
        return client

    async def check_products(self):
        for i, p in enumerate(self.products):
            if p.need_sale: yield self.products.pop(i)


class Product:
    next_id = 0

    def __init__(self, name: str, assessed_value: int, outpost: int, saving_days: int):
        self.id = Product.next_id
        Product.next_id += 1

        self.name = name
        self.assessed_value = assessed_value
        self.outpost = outpost
        self.outpost_date = date.today()
        self.saving_to = self.outpost_date + timedelta(days=saving_days)

    @property
    def need_sale(self) -> bool:
        return self.saving_to < date.today()

    def to_json(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "assessed_value": self.assessed_value,
            "outpost": self.outpost,
            "outpost_date": self.outpost_date.strftime(TIME_FORMAT),
            "saving_to": self.saving_to.strftime(TIME_FORMAT)
        }

    @staticmethod
    def from_json(jsoned_product: dict):
        product = Product(
            name=jsoned_product["name"],
            assessed_value=jsoned_product["assessed_value"],
            outpost=jsoned_product["outpost"],
            saving_days=0
        )
        product.id = jsoned_product["id"]
        product.next_id = product.id if product.id > product.next_id else product.next_id
        product.outpost_date = datetime.datetime.strptime(jsoned_product["outpost_date"], TIME_FORMAT).date()
        product.saving_to = datetime.datetime.strptime(jsoned_product["saving_to"], TIME_FORMAT).date()
        return product
