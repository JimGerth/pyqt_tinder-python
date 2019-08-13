from PyQt5.QtWidgets import QApplication

from tools.MainTool import MainTool

application = QApplication([])

window = MainTool()
window.show()

application.exec_()