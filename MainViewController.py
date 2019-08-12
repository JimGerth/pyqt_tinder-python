from PyQt5.QtWidgets import QMainWindow
import h5py as h5
import numpy as np
import random
from MainView import MainView


class MainViewController(QMainWindow):

    def __init__(self):
        super().__init__()
        self._view = MainView(parent=self)

        self._connect_buttons()

        self.setCentralWidget(self._view)
        self._load_data()
        self._show_random_image()

    def _connect_buttons(self):
        self._view._skip_button.clicked.connect(self._show_random_image)

    def _load_data(self):
        with h5.File('images_to_classify_manually.h5', 'r') as file:
            self._data = np.array(file['X_test'])

    def _show_random_image(self):
        self._view._show_image(self._data[random.randint(0, 199)])