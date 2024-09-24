import threading
import sys
import yaml
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout
from PyQt5.QtCore import QSize
import time


class BlockButton(QPushButton):
    def __init__(self, name):
        super().__init__(name)
        self.setMinimumSize(200, 100)
        self.part = config.get(name)
        self.running = True
        self.thread = threading.Thread(target=self.ping_verify, daemon=True)
        self.thread.start()

    def ping_verify(self):
        result = True
        while self.running:
            for host in self.part.keys():
                result = True
                try:
                    subprocess.check_output(
                        ["ping", "-c", "1", "-W", "1", self.part[host].get("ip")]
                    )
                except subprocess.CalledProcessError:
                    result = False
            if result:
                self.setStyleSheet("background-color: green;")
            else:
                self.setStyleSheet("background-color: red;")
            time.sleep(5)


class MainWindow(QWidget):
    def __init__(self, config):
        super().__init__()

        self.setWindowTitle("Система Управления Комплексным Авиатренажером")
        self.setMinimumSize(QSize(1000, 1000))

        self.gl = QGridLayout(self)
        self.buttons = {}

        self.blocks = config.keys()
        for i, block in enumerate(self.blocks):
            button = BlockButton(block)
            self.gl.addWidget(button, 0, i)
            self.buttons[block] = button
            button.clicked.connect(self.open_block_menu)

    def open_block_menu(self):
        button = self.sender()
        for i in reversed(range(self.gl.count())):
            widget = self.gl.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)
        QWidget().setLayout(self.gl)
        # print(button.part)
        block_menu_layout = QGridLayout(self)
        hosts = button.part.keys()
        # print(hosts)
        for host in hosts:
            # print(button.part[host])
            host_button = HostButton(host, button.part[host])
            block_menu_layout.addWidget(host_button)
        self.setLayout(block_menu_layout)


class HostButton(QPushButton):
    def __init__(self, host, params):
        super().__init__(host)
        self.setMinimumSize(200, 100)
        # self.part = config.get(name)
        # self.thread = threading.Thread(target=self.ping_verify, daemon=True)
        # self.thread.start()


app = QApplication(sys.argv)
with open("conf.yml", "r") as file:
    config = yaml.safe_load(file)
window = MainWindow(config)
window.show()
app.exec()
