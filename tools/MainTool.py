from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtCore import QRect

from tools.MainToolUI import MainToolUI
from tools.TinderUI import TinderUI
from tools.UI import UI

from services.ImageService import ImageService

from data.Defaults import Defaults


class MainTool(QMainWindow):

    def __init__(self, parent=None, application=None):
        super().__init__(parent)
        self._application = application

        self._ui = TinderUI(parent=self)
        if not isinstance(self._ui, UI):
            raise TypeError('warning: supplied user interface class might not be compatible with this program. It has to be of type UI - check tools/UI.py for specifications')

        self._set_screen_size()
        self.setCentralWidget(self._ui)

        self._image_service = ImageService(Defaults.image_data_file_path)

        self._create_connections()

        self._show_image_to_classify()

    def _set_screen_size(self): # should also be responsibility of the UI!
        screen_geometry = QGuiApplication.primaryScreen().availableGeometry()
        geometry = QRect(0, 0, screen_geometry.width() * 3 / 4, screen_geometry.height() * 3 / 4)
        geometry.moveCenter(screen_geometry.center())
        self.setGeometry(geometry)

    def _create_connections(self):
        self._ui.connect_single_classification_listener(self._image_classified_single)
        self._ui.connect_skip_classification_listener(self._image_skipped)
        self._ui.connect_multi_classification_listener(self._image_classified_multi)

    def _show_image_to_classify(self):
        self._ui.show_image(self._image_service.current_image)

    def _image_skipped(self):
        self._image_service.skip_image()
        self._show_image_to_classify()

    def _image_classified_single(self):
        self._image_service.classify_image('single')
        if self._image_service.done:
            self._everything_classified()
        self._show_image_to_classify()

    def _image_classified_multi(self):
        self._image_service.classify_image('multi')
        if self._image_service.done:
            self._everything_classified()
        self._show_image_to_classify()

    def _everything_classified(self):
        self._show_thank_you_screen()

    def  _show_thank_you_screen(self):
        thank_you_screen = QMessageBox()
        thank_you_screen.setText('Thank you!')
        thank_you_screen.setInformativeText('You classified all 200 images.')
        thank_you_screen.setIcon(QMessageBox.Information)
        thank_you_screen.buttonClicked.connect(self._exit)
        thank_you_screen.exec()

    def _exit(self):
        self._save_results()
        self._application.exit()

    def _save_results(self, path=Defaults.output_path):
        self._image_service.save_results(path)