from nicegui import ui
import yaml
import sys
from iws_functions import IWS
from group_classes import Group
from group_classes import host_item
from group_classes import SCS_Group
from group_classes import IWS_Group


with open("conf.yml", "r") as file:
    config = yaml.safe_load(file)
# print(config)

class Menu:
    def __init__(self) -> None:
        pass

    def mainmenu(self):
        self.check = {}
        self.host_buttons = {}
        self.blocks = config.keys()
        with ui.left_drawer().classes("bg-blue-100") as left_drawer:
            ui.label("")
            with ui.tabs().props("vertical").classes("w-full") as vertical_tabs:
                for block in self.blocks:
                    ui.tab(block, icon="computer").classes("h-20")
        with ui.tab_panels(vertical_tabs).classes("w-full w-[200px]"):
            self.make_tab_pannel()

    def make_tab_pannel(self):
        for group in self.blocks:
            self.get_group_class(group)

    def get_group_class(self, group):
        return {
            'SCS': Group(config, group),
            'IWS': IWS_Group(config, group)
        }[group]

    def exec_host_option(self, event):
        if event.sender.name == 'ip':
            pass
        elif event.sender.name == 'hardware':
            pass
        elif event.sender.name == 'network':
            pass



ui.run(title="Система Управления Комплексным Авиатренажером")


Menu().mainmenu()


def exec_host_option(self, event):
    if event.sender.name == "ip":
        pass
    elif event.sender.name == "hardware":
        pass
    elif event.sender.name == "network":
        pass