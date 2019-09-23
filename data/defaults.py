from PyQt5.QtGui import QBrush, QPen, QColor
from PyQt5.QtCore import Qt


class Defaults:

    env = '/Users/jim/PycharmProjects/pyqt_tinder-python/'
    image_data_file_path = env + 'data/images_to_classify_manually.h5'
    output_path = env + 'output.csv'
    cmap = 'Spectral_r'
    pen = QPen(Qt.NoPen)
    single_color = QColor(22, 153, 0, 130) #169900
    skip_color = QColor(255, 194, 35, 130) #FFC223
    multi_color = QColor(236, 0, 28, 130)  #EC001C
    sensibility = 1.5
    title_card_file_path = env + 'data/title_card_2.png'
    check_icon_path = env + 'data/single.png'
    clock_icon_path = env + 'data/circle_clock.png'
    cross_icon_path = env + 'data/multi2.png'