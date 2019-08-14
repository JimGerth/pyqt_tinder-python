from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QColor
from matplotlib import colors
from matplotlib import cm

from data.Defaults import Defaults


class PlotService:

    def convert_to_image(self, image, cmap=Defaults.cmap):
        q_image = QImage(image.width, image.height, QImage.Format_ARGB32)
        norm = colors.Normalize(vmin=0, vmax=image.data.max())
        cmap = cm.get_cmap(cmap)

        for x in range(image.width):
            for y in range(image.height):
                rgba = cmap(norm(image.data[x][y]))
                color = QColor()
                color.setRed(rgba[0] * 255)
                color.setGreen(rgba[1] * 255)
                color.setBlue(rgba[2] * 255)
                color.setAlpha(rgba[3] * 255)
                q_image.setPixel(x, y, color.rgb())

        image.q_image = q_image
        return q_image

    def convert_to_pixmap(self, image, cmap=Defaults.cmap):
        q_pixmap = QPixmap.fromImage(self.convert_to_image(image, cmap))
        image.q_pixmap = q_pixmap
        return q_pixmap
