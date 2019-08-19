from PyQt5.QtGui import QBrush, QPen, QColor
from PyQt5.QtCore import Qt


class Defaults:

    image_data_file_path = 'data/images_to_classify_manually.h5'
    output_path = 'output.csv'
    cmap = 'Spectral_r'
    pen = QPen(Qt.NoPen)
    single_color = QColor(22, 153, 0, 130) #169900
    skip_color = QColor(255, 194, 35, 130) #FFC223
    multi_color = QColor(236, 0, 28, 130)  #EC001C
    sensibility = 1.5
    title_card_file_path = 'data/TitleCard2.png'
    check_icon_path = 'data/single.png'
    clock_icon_path = 'data/circle_clock.png'
    cross_icon_path = 'data/multi2.png'