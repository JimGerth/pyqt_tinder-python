from services.QueueService import QueueService
from services.FileService import FileService

from materials.Image import Image


class ImageService:

    def __init__(self):
        self._image_queue = QueueService()
        self._classified_images = list()
        self._current_image = None

    def __del__(self):
        for image in self._classified_images:
            print('image with id {} was classified as {}'.format(image.id, image.classification))

    @property
    def current_image(self):
        return self._current_image

    def load_images(self, path):
        image_data_array = FileService().read_h5_file(path)
        for id, image_data in enumerate(image_data_array):
            self._image_queue.enqueue(Image(id, image_data))

    def next_image(self):
        self._current_image = self._image_queue.dequeue()

    def skip_image(self):
        self._image_queue.enqueue(self._current_image)

    def classify_image(self, category):
        self._current_image.classify(category)
        self._classified_images.append(self._current_image)