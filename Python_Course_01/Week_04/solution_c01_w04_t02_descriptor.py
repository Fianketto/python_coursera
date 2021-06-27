class Value:
    def __init__(self):
        self.value = None

    @staticmethod
    def _prepare_value(value, commission):
        return value * (1 - commission)

    def __get__(self, obj, obj_type):
        return self.value

    def __set__(self, instance, value):
        self.value = self._prepare_value(value, instance.commission)


class Account:
    amount = Value()

    def __init__(self, commission):
        self.commission = commission
