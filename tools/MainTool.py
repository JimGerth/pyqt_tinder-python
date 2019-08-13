from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtCore import QRect

from tools.MainToolUI import MainToolUI
from tools.UI import UI

from services.ImageService import ImageService

from data.Defaults import Defaults


class MainTool(QMainWindow):

    def __init__(self):
        super().__init__()

        self._ui = MainToolUI(parent=self)
        if not isinstance(self._ui, UI):
            raise TypeError('warning: supplied user interface class might not be compatible with this program. It has to be of type UI - check tools/UI.py for specifications')

        self._set_screen_size()
        self.setCentralWidget(self._ui)

        self._image_service = ImageService()
        self._image_service.load_images(Defaults.image_data_file_path)

        self._create_connections()

        self._show_next_image()

    def _set_screen_size(self):
        screen_geometry = QGuiApplication.primaryScreen().availableGeometry()
        geometry = QRect(0, 0, screen_geometry.width() * 3 / 4, screen_geometry.height() * 3 / 4)
        geometry.moveCenter(screen_geometry.center())
        self.setGeometry(geometry)

    def _create_connections(self):
        self._ui.connect_single_classification_listener(self, self._image_classified_single)
        self._ui.connect_skip_classification_listener(self, self._show_next_image)
        self._ui.connect_multi_classification_listener(self, self._image_classified_multi)

    def _show_next_image(self):
        try:
            self._image_service.next_image()
        except IndexError:
            print('no more images to classify')
        self.centralWidget()._show_image(self._image_service.current_image)

    def _image_classified_single(self):
        self._image_service.classify_image('single')
        self._show_next_image()

    def _image_classified_multi(self):
        self._image_service.classify_image('multi')
        self._show_next_image()

    def _save_results(self, path=Defaults.output_path):
        self._image_service.save_results(path)