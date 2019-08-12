from PyQt5.QtWidgets import QApplication
from MainViewController import MainViewController

application = QApplication([])

window = MainViewController()
window.show()

application.exec_()