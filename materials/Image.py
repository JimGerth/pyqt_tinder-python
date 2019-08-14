
class Image:

    def __init__(self, id, data):
        self.id = id
        self.data = data # 2D int array
        self.classification = None
        self.QImage = None
        self.QPixmap = None

    @property
    def width(self):
        return len(self.data)

    @property
    def height(self):
        return len(self.data[0])

    def classify(self, category):
        self.classification = category