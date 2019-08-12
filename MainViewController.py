from PyQt5.QtWidgets import QMainWindow
import h5py as h5
import numpy as np
import random
from MainView import MainView


class MainViewController(QMainWindow):

    def __init__(self):
        super().__init__()
        self._view = MainView(parent=self)
        self._current_image = 0
        self._image_classifications = np.full(200, 'unknown')

        self._connect_buttons()

        self.setCentralWidget(self._view)
        self._load_data()
        self._show_random_image()

    def __del__(self):
        for i in range(200):
            print('image {} classified as {}'.format(i, self._image_classifications[i]))

    def _connect_buttons(self):
        self._view._single_button.clicked.connect(self._image_classified_single)
        self._view._skip_button.clicked.connect(self._show_random_image)
        self._view._multi_button.clicked.connect(self._image_classified_multi)


    def _load_data(self):
        with h5.File('images_to_classify_manually.h5', 'r') as file:
            self._data = np.array(file['X_test'])

    def _show_random_image(self):
        self._current_image = random.randint(0, 199)
        self._view._show_image(self._data[self._current_image])

    def _image_classified_single(self):
        self._image_classifications[self._current_image] = 'single'
        self._show_random_image()

    def _image_classified_multi(self):
        self._image_classifications[self._current_image] = 'multi'
        self._show_random_image()