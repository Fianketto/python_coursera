'''
class SomeObject:
    def __init__(self):
        self.integer_field = 0
        self.float_field = 0.0
        self.string_field = ""
'''


class EventGet:
    def __init__(self, t):
        self.event_type = "get"
        self.arg_type = t


class EventSet:
    def __init__(self, v):
        self.event_type = "set"
        self.arg_type = type(v)
        self.arg_value = v


class NullHandler:
    def __init__(self, next_handler=None):
        self.next_handler = next_handler

    def handle(self, obj, request):
        pass


class IntHandler(NullHandler):
    def handle(self, obj, event):
        if event.arg_type is int:
            if event.event_type == "set":
                obj.integer_field = event.arg_value
            elif event.event_type == "get":
                return obj.integer_field
        else:
            return self.next_handler.handle(obj, event)


class FloatHandler(NullHandler):
    def handle(self, obj, event):
        if event.arg_type is float:
            if event.event_type == "set":
                obj.float_field = event.arg_value
            elif event.event_type == "get":
                return obj.float_field
        else:
            return self.next_handler.handle(obj, event)


class StrHandler(NullHandler):
    def handle(self, obj, event):
        if event.arg_type is str:
            if event.event_type == "set":
                obj.string_field = event.arg_value
            elif event.event_type == "get":
                return obj.string_field
        else:
            return self.next_handler.handle(obj, event)
