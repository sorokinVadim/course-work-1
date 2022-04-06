import asyncio
import collections
import sys

from PyQt6.QtWidgets import QApplication
from qasync import QEventLoop

from coursework.models import *
from coursework.storage import Storage
from coursework.ui import *


class Application:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.loop: asyncio.AbstractEventLoop = QEventLoop(self.app)

        self.storage = Storage()
        self.clients_len = len(self.storage.clients)

        self.ui = Ui()
        self.ui.show_without_client.clicked.connect(lambda: self.storage.change_actual(-1))
        self.ui.new_client_btn.clicked.connect(lambda: NewClientDialog(self.storage.add_client, self.ui))

        self.ui.closeEvent = lambda _: self.storage.save()

        asyncio.set_event_loop(self.loop)

    async def update(self):
        await self.ui.watch_clients(self.storage.clients, self.storage.change_actual)
        while True:
            for prod_list in [c.check_products() for c in self.storage.clients]:
                async for p in prod_list:
                    self.storage.products_for_sale.append(p)
            await self.ui.watch_products(self.storage.actual_product_list, self.storage.actual_product_list.pop)
            if self.clients_len != len(self.storage.clients):
                self.clients_len = len(self.storage.clients)
                await self.ui.watch_clients(self.storage.clients, self.storage.change_actual)

    def run(self):
        asyncio.ensure_future(self.update())
        self.loop.run_forever()


if __name__ == '__main__':
    app = Application()
    app.run()
