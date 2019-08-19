from PyQt5.QtWidgets import QMainWindow, QMessageBox, QAction, QMenu, QMenuBar, QFileDialog
from PyQt5.QtGui import QGuiApplication, QKeySequence
from PyQt5.QtCore import QRect

from tools.MainToolUI import MainToolUI
from tools.TinderUI import TinderUI
from tools.MatplotTinderUI import MatplotTinderUI
from tools.UI import UI

from services.ImageService import ImageService

from data.Defaults import Defaults


class MainTool(QMainWindow):

    def __init__(self, parent=None, application=None):
        super().__init__(parent)
        self._application = application
        self._saved = False
        self._save_path = None
        self._image_service = ImageService(Defaults.image_data_file_path)
        self._ui = TinderUI(parent=self)
        if not isinstance(self._ui, UI):
            raise TypeError('warning: supplied user interface class might not be compatible with this program. It has to be of type UI - check tools/UI.py for specifications')
        self.setCentralWidget(self._ui)
        self._setup_menu_bar()
        self._set_screen_size()
        self._create_connections()
        self._show_image_to_classify()

    def _setup_menu_bar(self):
        self.setMenuBar(QMenuBar())
        self.save_action = QAction('Save')
        self.save_action.setShortcut(QKeySequence.Save)
        self.save_action.triggered.connect(self._save_results)
        self.save_as_action = QAction('Save as...')
        self.save_as_action.setShortcut(QKeySequence.SaveAs)
        self.save_as_action.triggered.connect(self._save_as_results)
        self.file_menu = QMenu('File')
        self.file_menu.addAction(self.save_action)
        self.file_menu.addAction(self.save_as_action)
        self.menuBar().addMenu(self.file_menu)

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
        self.setWindowTitle('{} classified multi   |   {} classified single   |   {} to go!'.format(self._image_service.num_classified_multi, self._image_service.num_classified_single, self._image_service.num_images_to_classify + 1))
        self._ui.show_image(self._image_service.current_image)

    def _image_skipped(self):
        self._image_service.skip_image()
        self._show_image_to_classify()

    def _image_classified_single(self):
        self._image_service.classify_image('single')
        self._saved = False
        if self._image_service.done:
            self._show_thank_you_screen()
        else:
            self._show_image_to_classify()

    def _image_classified_multi(self):
        self._image_service.classify_image('multi')
        self._saved = False
        if self._image_service.done:
            self._show_thank_you_screen()
        else:
            self._show_image_to_classify()

    def  _show_thank_you_screen(self):
        thank_you_screen = QMessageBox()
        thank_you_screen.setText('Thank you!')
        thank_you_screen.setInformativeText('You classified all 200 images.')
        thank_you_screen.setIcon(QMessageBox.Information)
        thank_you_screen.setContentsMargins(25, 25, 25, 25)
        thank_you_screen.buttonClicked.connect(self._exit)
        thank_you_screen.exec()

    def _exit(self):
        while not self._saved:
            self._save_results()
        self._application.exit()

    def _save_results(self):
        if not self._save_path:
            self._save_path = QFileDialog.getSaveFileName(self, 'save classifications', './output.csv', 'CSV Files (*.csv)')[0]
        try:
            self._image_service.save_results(self._save_path)
            self._saved = True
        except:
            self._saved = False

    def _save_as_results(self):
        self._save_path = None
        self._save_results()