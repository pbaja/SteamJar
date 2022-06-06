from typing import Callable

class Event:

    def __init__(self):
        self.listeners = []

    def subscribe(self, callback: Callable):
        self.listeners.append(callback)
    
    def invoke(self, value):
        for listener in self.listeners:
            listener(value)