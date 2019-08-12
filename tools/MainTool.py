from PyQt5.QtWidgets import QMainWindow

from tools.MainToolUI import MainToolUI

from services.ImageService import ImageService

from data.Defaults import Defaults


class MainTool(QMainWindow):

    def __init__(self):
        super().__init__()
        self._view = MainToolUI(parent=self)

        self._image_service = ImageService()
        self._image_service.load_images(Defaults.image_data_file_path)

        self._connect_buttons()

        self.setCentralWidget(self._view)
        self._show_random_image()

    def _connect_buttons(self):
        self._view._single_button.clicked.connect(self._image_classified_single)
        self._view._skip_button.clicked.connect(self._show_random_image)
        self._view._multi_button.clicked.connect(self._image_classified_multi)

    def _show_random_image(self):
        try:
            self._image_service.next_image()
        except IndexError:
            print('no more images to classify')
        self._view._show_image(self._image_service.current_image)

    def _image_classified_single(self):
        self._image_service.classify_image('single')
        self._show_random_image()

    def _image_classified_multi(self):
        self._image_service.classify_image('multi')
        self._show_random_image()

    def _save_results(self, path=Defaults.output_path):
        self._image_service.save_results(path)