from PyQt5.Qt import QThreadPool

from services.QueueService import QueueService
from services.FileService import FileService
from services.PlotService import PlotService
from services.ThreadingService import ThreadingService

from materials.Image import Image

from data.Defaults import Defaults


class ImageService:

    def __init__(self, path=None):
        self._image_queue = QueueService()
        self._classified_images = list()
        self.current_image = None
        self._next_image = None

        self.num_classified_single = 0
        self.num_classified_multi = 0

        self._thread_pool = QThreadPool()

        if path:
            self.load_images(path)
            # if no path was supplied load_images(path) has to be called, before working with ImageService!

    @property
    def num_images_to_classify(self):
        return len(self._image_queue)

    @property
    def done(self):
        return self.num_images_to_classify == 0 and not self.current_image

    def load_images(self, path):
        image_data_array = FileService().read_h5_file(path)
        for id, image_data in enumerate(image_data_array):
            self._image_queue.enqueue(Image(id, image_data))
        self._image_queue.shuffle()
        self._get_next_image()

    def _get_next_image(self):
        if self._next_image:
            self.current_image = self._next_image
            self._image_queue.dequeue()
        else:
            self.current_image = self._image_queue.dequeue()

        try:
            self._preload_next_image()
        except:
            pass

    def _preload_next_image(self): # preloads next image in queue into memory in a different thread
        self._next_image = self._image_queue.peek()
        self._thread_pool.start(ThreadingService(PlotService().convert_to_image, image=self._next_image))

    def skip_image(self):
        self._image_queue.enqueue(self.current_image)
        self._get_next_image()

    def classify_image(self, category):
        if category == 'single':
            self.num_classified_single += 1
        elif category == 'multi':
            self.num_classified_multi += 1
        self.current_image.classify(category)
        self._classified_images.append(self.current_image)
        try:
            self._get_next_image()
        except:
            self.current_image = None

    def save_results(self, path=Defaults.output_path):
        output = 'image_id,category\n'
        for image in self._classified_images:
            output += '{},{}\n'.format(image.id, image.classification)
        FileService().write_csv_file(path, output)