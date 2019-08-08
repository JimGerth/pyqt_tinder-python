from PyQt5.QtWidgets import QApplication
from Window import Window

application = QApplication([])

window = Window()
window.show()

application.exec_()