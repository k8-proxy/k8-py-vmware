from pprint import pprint


class Catch:
    """
    Helper class for cases when the native Python exception traces is too noisy
    """
    def __enter__(self):
        pass

    def __exit__(self, exception_type, exception_value, exception_traceback):
        if (exception_type is not None):
            print()
            print("***************************")
            print("********* Catch ***********")
            print("***************************")
            print()
            print(exception_type)
            print()
            pprint(exception_value)
            #print(f"Exception Type : {exception_type}")
            #print(f"Exception Value : {exception_value}")
            #print(f"Exception Trace: {exception_traceback}")               # todo: find good way to show this traceback in a consumable way
        return True     # returning true here will prevent the exception to be propagated (which is the objective of this class :) )
