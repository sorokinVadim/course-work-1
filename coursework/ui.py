from PyQt6.QtWidgets import *
from PyQt6.QtCore import pyqtSignal
from PyQt6 import QtGui
import asyncio
from .models import Product, Client
import sys


class Ui(QMainWindow):
    app = QApplication(sys.argv)

    def __init__(self):
        super(Ui, self).__init__()

        central_widget = QWidget(self)
        central_widget.setLayout(QHBoxLayout())
        self.setCentralWidget(central_widget)

        # Список продуктов
        self.products_list = QWidget()
        self.products_list.setLayout(QVBoxLayout(self.products_list))

        product_scroll_area = QScrollArea(self)
        product_scroll_area.setWidget(self.products_list)
        product_scroll_area.setWidgetResizable(True)

        # Просмотр продуктов на продажу
        self.show_without_client = QPushButton("Простроченные")

        self.products_widget = QWidget(self)
        self.products_widget.setLayout(QVBoxLayout(self.products_widget))
        self.products_widget.layout().addWidget(product_scroll_area)
        self.products_widget.layout().addWidget(self.show_without_client)

        # Список клиентов
        self.client_list = QWidget()
        self.client_list.setLayout(QVBoxLayout(self.client_list))

        client_scroll_area = QScrollArea(self)
        client_scroll_area.setWidget(self.client_list)
        client_scroll_area.setWidgetResizable(True)

        # Новый товар
        self.new_client_btn = QPushButton("New client")

        self.client_widget = QWidget(self)
        self.client_widget.setLayout(QVBoxLayout(self.client_widget))
        self.client_widget.layout().addWidget(client_scroll_area)
        self.client_widget.layout().addWidget(self.new_client_btn)

        self.centralWidget().layout().addWidget(self.products_widget)
        self.centralWidget().layout().addWidget(self.client_widget)

        self.setVisible(True)

    @staticmethod
    def clear_layout(layout):
        while layout.count():
            widget = layout.takeAt(0).widget()
            if widget is not None: widget.deleteLater()

    def add_product(self, product: Product, delete_func):
        product_layout: QVBoxLayout = self.products_list.layout()
        product_layout.insertWidget(0, ProductWidget(product, delete_func))

    def new_products(self, products: list[Product], delete_func):
        self.clear_layout(self.products_list.layout())
        for i, p in enumerate(products):
            self.add_product(p, lambda: delete_func(i))
        self.products_list.layout() \
            .addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

    def add_client(self, client: Client, change_actual_func):
        client_layout: QVBoxLayout = self.client_list.layout()
        client_widget = ClientWidget(client)
        client_widget.change_actual_products.connect(lambda p: change_actual_func(p))
        client_layout.insertWidget(0, client_widget)

    def new_clients(self, clients: list[Client], change_actual_func):
        self.clear_layout(self.client_list.layout())
        for c in clients:
            self.add_client(c, change_actual_func)
        self.products_list.layout() \
            .addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))


    async def watch_products(self, product_list: list[Product], delete_func):
        self.new_products(product_list, delete_func)
        await asyncio.sleep(0.25)

    async def watch_clients(self, client_list: list[Client], change_actual_func):
        self.new_clients(client_list, change_actual_func)
        await asyncio.sleep(1)


class ProductWidget(QWidget):

    def __init__(self, product: Product, delete_func, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        self.product_id = product.id
        # Product name
        self.name = QLabel(product.name)
        layout.addWidget(self.name)

        self.view_info_btn = QPushButton("Info")
        self.view_info_btn.clicked.connect(lambda: self.view_info(product))
        layout.addWidget(self.view_info_btn)

        self.delete_func = delete_func
        self.action_btn = QPushButton("Продати" if product.need_sale else "Повернути")
        self.action_btn.clicked.connect(self.remove_me)
        layout.addWidget(self.action_btn)

        self.setLayout(layout)

    def remove_me(self):
        self.action_btn.setDisabled(True)
        self.delete_func()

    def view_info(self, product: Product):
        info_widget = QDialog(self.parent())
        info_widget.setLayout(QVBoxLayout())
        info_widget.layout().addWidget(QLabel(f"Им'я: {product.name} Прізвище: {product.assessed_value} {product.outpost}"))
        info_widget.layout().addWidget(QLabel(f"Вік {product.outpost_date} Номер паспорта {product.saving_to}"))
        hide_btn = QPushButton("Добре")
        hide_btn.clicked.connect(info_widget.deleteLater)
        info_widget.layout().addWidget(hide_btn)
        info_widget.show()


class ClientWidget(QWidget):
    change_actual_products = pyqtSignal(int)

    def __init__(self, client: Client):
        super(ClientWidget, self).__init__()
        self.client = client

        layout = QHBoxLayout()

        self.name = QLabel(client.name)
        layout.addWidget(self.name)

        self.add_product_btn = QPushButton("Добавить продукт")
        layout.addWidget(self.add_product_btn)

        self.view_products_btn = QPushButton("Продукти")
        self.view_products_btn.clicked.connect(lambda: self.change_actual_products.emit(client.id))
        layout.addWidget(self.view_products_btn)

        self.setLayout(layout)

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.view_info()

    def enterEvent(self, event: QtGui.QEnterEvent) -> None:
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.ColorRole.WindowText, QtGui.QColor().blue())
        self.name.setPalette(palette)

    def leaveEvent(self, a0) -> None:
        self.name.setPalette(QtGui.QPalette())

    def view_info(self):
        info_widget = QDialog(self)
        info_widget.setLayout(QVBoxLayout())
        info_widget.layout().addWidget(QLabel(f"Им'я: {self.client.name} Прізвище: {self.client.surname}"))
        info_widget.layout().addWidget(QLabel(f"Вік {self.client.age} Номер паспорта {self.client.pass_num}"))
        hide_btn = QPushButton("Добре")
        hide_btn.clicked.connect(info_widget.deleteLater)
        info_widget.layout().addWidget(hide_btn)
        info_widget.show()


class NewClientDialog(QDialog):
    def __init__(self, new_client_func, parent=None):
        super(NewClientDialog, self).__init__(parent=parent)
        self.setLayout(QGridLayout(self))
        layout: QGridLayout = self.layout()

        layout.addWidget(QLabel("Ім'я: "), 1, 1)
        self.name = QLineEdit(self)
        layout.addWidget(self.name, 1, 2)

        layout.addWidget(QLabel("Призвище: "), 1, 3)
        self.surname = QLineEdit(self)
        layout.addWidget(self.surname, 1, 4)

        layout.addWidget(QLabel("Вік: "), 2, 1)
        self.age = QSpinBox(self)
        self.age.setMinimum(18)
        self.age.setMaximum(200)
        layout.addWidget(self.age, 2, 2)

        layout.addWidget(QLabel("Номер паспорту: "), 2, 3)
        self.num_pass = QSpinBox(self)
        self.num_pass.setMaximum(100000000)
        layout.addWidget(self.num_pass, 2, 4)

        self.submit = QPushButton("Додати")
        self.submit.clicked.connect(lambda: new_client_func(self.submit_me()))
        layout.addWidget(self.submit, 3, 1, 1, 4)

        self.show()

    def get_client_data(self) -> Client:
        name = self.name.text()
        surname = self.surname.text()

        age = self.age.value()
        num_pass = self.num_pass.value()

        return Client(name, surname, age, num_pass)

    def submit_me(self) -> Client:
        self.deleteLater()
        return self.get_client_data()


class NewProductDialog(QDialog):
    def __init__(self, new_product_func, parent=None):
        super(NewProductDialog, self).__init__(parent=parent)
        self.setLayout(QGridLayout(self))
        layout: QGridLayout = self.layout()

        layout.addWidget(QLabel("Найменування: "), 1, 1)
        self.name = QLineEdit(self)
        layout.addWidget(self.name, 1, 2)

        layout.addWidget(QLabel("Оціночна вартість: "), 1, 3)
        self.assessed_value = QSpinBox(self)
        self.assessed_value.setMinimum(100)
        self.assessed_value.setMaximum(100000)
        layout.addWidget(self.assessed_value, 1, 4)

        layout.addWidget(QLabel("Сума, видана під заставу: "), 2, 1)
        self.outpost = QSpinBox(self)
        self.outpost.setMinimum(100)
        self.outpost.setMaximum(100000)
        layout.addWidget(self.age, 2, 2)

        layout.addWidget(QLabel("Срок сбереження (у днях) : "), 2, 3)
        self.saving_to = QSpinBox(self)
        self.saving_to.setMaximum(90)
        layout.addWidget(self.saving_to, 2, 4)

        self.submit = QPushButton("Додати")
        self.submit.clicked.connect(lambda: new_product_func(self.submit_me()))
        layout.addWidget(self.submit, 3, 1, 1, 4)

        self.show()

    def get_product_data(self) -> Product:
        name = self.name.text()
        assessed_value = self.assessed_value.value()

        outpost = self.outpost.value()
        saving_to = self.saving_to.value()

        return Product(name, assessed_value, outpost, saving_to)

    def submit_me(self) -> Product:
        self.deleteLater()
        return self.get_product_data()
