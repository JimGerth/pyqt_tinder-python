from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QColor
from matplotlib import colors
from matplotlib import cm
import qimage2ndarray as i2a

from data.Defaults import Defaults


class PlotService:

    def convert_to_image(self, image, cmap=Defaults.cmap):

        # norm = colors.Normalize(vmin=0, vmax=image.data.max())
        # cmap = cm.get_cmap(cmap)
        #
        # for x in range(image.width):
        #     for y in range(image.height):
        #         image.data[x][y] = list(cmap(norm(image.data[x][y])))

        q_image = i2a.array2qimage(image.data, normalize=True)
        image.q_image = q_image
        return q_image

    def convert_to_pixmap(self, image, cmap=Defaults.cmap):
        q_pixmap = QPixmap.fromImage(self.convert_to_image(image, cmap))
        image.q_pixmap = q_pixmap
        return q_pixmap
