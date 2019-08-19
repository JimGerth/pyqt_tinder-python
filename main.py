from PyQt5.QtWidgets import QApplication

from tools.main_tool import MainTool

application = QApplication([])

window = MainTool(application=application)
window.show()

application.exec_()