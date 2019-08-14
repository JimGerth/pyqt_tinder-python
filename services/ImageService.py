import threading

from services.QueueService import QueueService
from services.FileService import FileService
from services.PlotService import PlotService

from materials.Image import Image

from data.Defaults import Defaults


class ImageService:

    def __init__(self, path=None):
        self._image_queue = QueueService()
        self._classified_images = list()
        self.current_image = None
        self._next_image = None

        if path:
            self.load_images(path)

    # def __del__(self):
    #     self.save_results() # doesn't work, objects deleted before file could be written

    def load_images(self, path):
        image_data_array = FileService().read_h5_file(path)
        for id, image_data in enumerate(image_data_array):
            self._image_queue.enqueue(Image(id, image_data))
        self._get_next_image()

    def _get_next_image(self):
        if self._next_image:
            self.current_image = self._next_image
            self._image_queue.dequeue()
        else:
            self.current_image = self._image_queue.dequeue()

        preload_thread = threading.Thread(target=self._preload_next_image, daemon=True)
        preload_thread.start()

    def _preload_next_image(self): # preloads next image in queue into memory in a different thread
        self._next_image = self._image_queue.peek()
        PlotService().convert_to_pixmap(self._next_image)

    def skip_image(self):
        self._image_queue.enqueue(self.current_image)
        self._get_next_image()

    def classify_image(self, category):
        self.current_image.classify(category)
        self._classified_images.append(self.current_image)
        self._get_next_image()

    def save_results(self, path=Defaults.output_path):
        output = 'image_id,category\n'
        for id, image in enumerate(self._classified_images):
            output += '{},{}\n'.format(id, image.classification)
        FileService().write_csv_file(path, output)