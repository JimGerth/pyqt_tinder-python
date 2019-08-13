from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QColor
from matplotlib import colors
from matplotlib import cm


class PlotService:

    def convert_to_image(self, image_data, cmap='Spectral_r'):
        image = QImage(image_data.width, image_data.height, QImage.Format_ARGB32)
        norm = colors.Normalize(vmin=0, vmax=image_data.data.max())
        cmap = cm.get_cmap(cmap)

        for x in range(image_data.width):
            for y in range(image_data.height):
                rgba = cmap(norm(image_data.data[x][y]))
                color = QColor()
                color.setRed(rgba[0] * 255)
                color.setGreen(rgba[1] * 255)
                color.setBlue(rgba[2] * 255)
                color.setAlpha(rgba[3] * 255)
                image.setPixel(x, y, color.rgb())

        return image

    def convert_to_pixmap(self, image_data):
        return QPixmap.fromImage(self.convert_to_image(image_data))
