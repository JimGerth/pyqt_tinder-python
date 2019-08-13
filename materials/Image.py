
class Image:

    def __init__(self, id, data):
        self._id = id
        self._data = data # 2D int array
        self._classification = None

    @property
    def id(self):
        return self._id

    @property
    def data(self):
        return self._data

    @property
    def classification(self):
        return self._classification

    @property
    def width(self):
        return len(self._data)

    @property
    def height(self):
        return len(self._data[0])

    def classify(self, category):
        self._classification = category