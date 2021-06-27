from abc import ABC, abstractmethod

'''
class Engine:
    pass
'''


class ObservableEngine(Engine):
    def __init__(self):
        self.subscribers = set()
        pass

    def subscribe(self, subscriber):
        self.subscribers.add(subscriber)

    def unsubscribe(self, subscriber):
        self.subscribers.remove(subscriber)

    def notify(self, ach):
        for s in self.subscribers:
            s.update(ach)


class AbstractObserver(ABC):
    @abstractmethod
    def update(self, ach):
        pass


class ShortNotificationPrinter(AbstractObserver):
    def __init__(self):
        self.achievements = set()

    def update(self, ach):
        if ach["title"] not in self.achievements:
            self.achievements.add(ach["title"])


class FullNotificationPrinter(AbstractObserver):
    def __init__(self):
        self.achievements = list()
        self.ach_set = set()

    def update(self, ach):
        if ach["title"] not in self.ach_set:
            self.ach_set.add(ach["title"])
            self.achievements.append(ach)


