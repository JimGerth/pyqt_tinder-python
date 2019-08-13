from PyQt5.QtWidgets import QApplication
from tools.MainTool import MainTool
from MainWidget import MainWidget

application = QApplication([])

window = MainWidget()
window.show()

application.exec_()