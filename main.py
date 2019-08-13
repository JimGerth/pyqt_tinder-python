from PyQt5.QtWidgets import QApplication

from tools.MainWidget import MainWidget

application = QApplication([])

window = MainWidget()
window.show()

application.exec_()