import numpy as np


class QueueService:

    def __init__(self):
        self._data = list()

    def enqueue(self, item):
        self._data.append(item)

    def dequeue(self):
        return self._data.pop(0)

    def peek(self):
        return self._data[0]

    def shuffle(self):
        np.random.shuffle(self._data)