from PyQt5.QtGui import QPixmap
from matplotlib import colors
from matplotlib import cm
import qimage2ndarray as i2a

from data.Defaults import Defaults


class PlotService:

    def convert_to_image(self, image, cmap=Defaults.cmap):
        norm = colors.Normalize(vmin=image.data.min(), vmax=image.data.max())
        cmap = cm.get_cmap(cmap)
        normalized_colored_data = cmap(norm(image.data))
        q_image = i2a.array2qimage(normalized_colored_data, normalize=True)
        image.q_image = q_image

    def convert_to_pixmap(self, image, cmap=Defaults.cmap):
        q_pixmap = QPixmap.fromImage(self.convert_to_image(image, cmap))
        image.q_pixmap = q_pixmap