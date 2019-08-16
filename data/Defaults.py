from PyQt5.QtGui import QBrush, QPen, QColor
from PyQt5.QtCore import Qt


class Defaults:

    image_data_file_path = 'data/images_to_classify_manually.h5'
    output_path = 'output.csv'
    cmap = 'Spectral_r'
    pen = QPen(Qt.NoPen)
    single_color = QColor(22, 153, 0, 130)
    skip_color = QColor(255, 194, 35, 130)
    multi_color = QColor(236, 0, 28, 130)