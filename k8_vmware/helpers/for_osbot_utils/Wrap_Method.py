class Wrap_Method:
    def __init__(self, target_module, target_method):
        self.target_module   = target_module
        self.target_method   = target_method
        self.target          = getattr(target_module, target_method)
        self.wrapper_method  = None
        self.calls           = []

    def __enter__(self):
        self.wrap()
        return self

    def __exit__(self, type, value, traceback):
        self.unwrap()

    def calls_count(self):
        return len(self.calls)

    def wrap(self):
        def wrapper_method(*args, **kwargs):
            call = {
                        'args'        : args,
                        'kwargs'      : kwargs,
                        'return_value': self.target(*args, **kwargs)
                    }
            self.calls.append(call)
            return call['return_value']

        self.wrapper_method = wrapper_method
        setattr(self.target_module, self.target_method, self.wrapper_method)
        return self.wrapper_method

    def unwrap(self):
        setattr(self.target_module, self.target_method, self.target)
