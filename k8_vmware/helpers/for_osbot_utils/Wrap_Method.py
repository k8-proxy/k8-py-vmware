# todo: note sure if this is the best name "Hook _Method" might be better
class Wrap_Method:
    def __init__(self, target_module, target_method):
        self.target_module   = target_module
        self.target_method   = target_method
        self.target          = getattr(target_module, target_method)
        self.wrapper_method  = None
        self.calls           = []
        self.on_before_call  = []
        self.on_after_call   = []
        self.mock_call       = None

    def __enter__(self):
        self.wrap()
        return self

    def __exit__(self, type, value, traceback):
        self.unwrap()

    def add_on_after_call(self, on_after_call):
        self.on_after_call.append(on_after_call)
        return self

    def add_on_before_call(self, on_before_call):
        self.on_before_call.append(on_before_call)
        return self

    def calls_count(self):
        return len(self.calls)

    def calls_last_one(self):
        if len(self.calls) > 0:
            return self.calls[-1]

    def after_call(self, return_value):
        for method in self.on_after_call:
            return_value = method(return_value)
        return return_value

    def before_call(self, *args, **kwargs):
        for method in self.on_before_call:
            (args, kwargs) = method(*args, **kwargs)
        return (args, kwargs)



    def wrap(self):

        def wrapper_method(*args, **kwargs):

            if self.mock_call:
                return_value = self.mock_call(*args,**kwargs)
            else:
                (args, kwargs) = self.before_call(*args, **kwargs)
                return_value   = self.target(*args, **kwargs)
                return_value   = self.after_call(return_value)

            call = {
                        'args'        : args,
                        'kwargs'      : kwargs,
                        'return_value': return_value
                    }
            self.calls.append(call)
            return call['return_value']

        self.wrapper_method = wrapper_method
        setattr(self.target_module, self.target_method, self.wrapper_method)
        return self.wrapper_method

    def unwrap(self):
        setattr(self.target_module, self.target_method, self.target)
