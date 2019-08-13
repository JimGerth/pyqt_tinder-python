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

        supplied_UI = MainToolUI(parent=self)
        if not isinstance(supplied_UI, UI):
            raise TypeError('warning: supplied user interface class might not be compatible with this program. It has to be of type UI - check tools/UI.py for specifications')

        self._set_screen_size()
        self.setCentralWidget(supplied_UI)

        self._image_service = ImageService()
        self._image_service.load_images(Defaults.image_data_file_path)

        self._connect_buttons()

        self._show_next_image()

    def _set_screen_size(self):
        screen_geometry = QGuiApplication.primaryScreen().availableGeometry()
        geometry = QRect(0, 0, screen_geometry.width() * 3 / 4, screen_geometry.height() * 3 / 4)
        geometry.moveCenter(screen_geometry.center())
        self.setGeometry(geometry)

    def _connect_buttons(self):
        self.centralWidget()._single_button.clicked.connect(self._image_classified_single)
        self.centralWidget()._skip_button.clicked.connect(self._show_next_image)
        self.centralWidget()._multi_button.clicked.connect(self._image_classified_multi)

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