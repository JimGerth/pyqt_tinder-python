from services.QueueService import QueueService
from services.FileService import FileService

from materials.Image import Image

from data.Defaults import Defaults


class ImageService:

    def __init__(self):
        self._image_queue = QueueService()
        self._classified_images = list()
        self.current_image = None

    # def __del__(self):
    #     self.save_results() # doesn't work, objects deleted before file could be written

    def load_images(self, path):
        image_data_array = FileService().read_h5_file(path)
        for id, image_data in enumerate(image_data_array):
            self._image_queue.enqueue(Image(id, image_data))
        self._next_image()

    def _next_image(self):
        self.current_image = self._image_queue.dequeue()

    def skip_image(self):
        self._image_queue.enqueue(self.current_image)
        self._next_image()

    def classify_image(self, category):
        self.current_image.classify(category)
        self._classified_images.append(self.current_image)
        self._next_image()

    def save_results(self, path=Defaults.output_path):
        output = 'image_id,category\n'
        for id, image in enumerate(self._classified_images):
            output += '{},{}\n'.format(id, image.classification)
        FileService().write_csv_file(path, output)