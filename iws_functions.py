import inspect


class IWS:
    def __init__(self, config):
        self.available_functions = {}
        self.config = config
        self.validate_config(config)


    def validate_config(self):
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if callable(attr) and hasattr(attr, 'required_params'):
                if self.execute_check(attr):
                    self.available_functions[attr_name] = attr.required_params


    def execute_check(self, func) -> bool:
        required_params = func.required_params
        config_keys = self._get_all_keys(self.config)
        return all(param in config_keys for param in required_params)

    def require_params(*required_params):
        def decorator(func):
            func.required_params = required_params
            return func
        return decorator


    @require_params('ip')
    def check_network(ip):
        pass

    @require_params('ip', 'web_interface')
    def check_web_interface(ip, web_interface):
        pass



    @classmethod
    def get_dict_of_methods(cls):
        methods_dict = {}
        for name, method in inspect.getmembers(cls, predicate=inspect.isfunction):
            args = inspect.getfullargspec(method).args
            if 'self' in args:
                args.remove('self')
            methods_dict[name] = args
        return methods_dict


