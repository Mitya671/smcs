from nicegui import ui
import inspect
from typing import Any, Dict, List


class host_item(ui.item):
    def __init__(self, text, on_click, name):
        super().__init__(text=text, on_click=on_click)
        self.name = name


class Group(ui.tab_panel):
    def __init__(self, config, group):
        self.host_buttons = {}
        super().__init__(name=group)
        self.group_config = config[group]
        with self:
            for host in self.group_config.keys():
                self.make_host_buttons(group, host)

    def make_host_buttons(self, group, hostname):
        self.host_buttons[hostname] = self.Host(hostname, self.group_config)
        self.host_buttons[hostname].validate_config()
        # print(self.host_buttons[hostname].available_functions)
        self.host_buttons[hostname].draw()

    class Host(ui.dropdown_button):
        def __init__(self, hostname, group_config):
            super().__init__(hostname)
            self.host_config = group_config[hostname]
            self.hostname = hostname
            self.available_functions = {}
        
        def draw(self):
            with self:
                host_options = self.available_functions.keys()
                for host_option in host_options:
                    print(host_option)
                    button = host_item(
                        name=host_option,
                        text=host_option, on_click=lambda ho=host_option: print(f"ABOBAA {ho}")
                    ).style("text-align: center;")

        def validate_config(self):
            for attr_name in dir(self):
                attr = getattr(self, attr_name)
                if callable(attr) and hasattr(attr, "required_params"):
                    if self.execute_check(attr):
                        self.available_functions[attr_name] = attr.required_params

        def execute_check(self, func) -> bool:
            required_params = func.required_params
            return all(param in self.host_config for param in required_params)

        def require_params(*required_params):
            def decorator(func):
                func.required_params = required_params
                return func
            return decorator

        @require_params("ip", "web_interface")
        def check_web_interface(ip, web_interface):
            pass


class IWS_Group(Group):
    def __init__(self, config, group):
        super().__init__(config, group)

    class Host(Group.Host):
        def __init__(self, hostname, group_config):
            super().__init__(hostname, group_config)

        def require_params(*required_params):
            def decorator(func):
                func.required_params = required_params
                return func
            return decorator

        @require_params("ip", "web_interface")
        def check_interface(ip, web_interface):
            pass




# class IWS_Group(Group):

#     class Host(Group.Host):
#         def __init__(self, hostname, group_config):
#             super().__init__(self, hostname, group_config)
#             print(self.available_functions)

#         def require_params(*required_params):
#             def decorator(func):
#                 func.required_params = required_params
#                 return func
#             return decorator

#         @require_params("ip", "web_interface")
#         def check_aboba_interface(ip, web_interface):
#             pass

#         @require_params("ip", "web_interface")
#         def check_network_interface(ip, web_interface):
#             pass

class SCS_Group(Group):

    def __init__(self, config, group):
        super().__init__(config, group)
        self.group_config = config[group]

    # class SCS(Group.Host):
    #     def __init__(self, hostname):
    #         super().__init__(hostname)

        # @Group.Host.require_params("ip")
        # def check_network(ip):
        #     pass

        # @Group.Host.require_params("ip", "web_interface")
        # def check_web_interface(ip, web_interface):
        #     pass


