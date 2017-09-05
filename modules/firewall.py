from PyQt4.QtGui import QDialog, QWidget

from modules.dialogFirewall import Ui_DialogFirewall


class DialogFirewall(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.dialog = QDialog(parent)
        self.dialog.ui = Ui_DialogFirewall()
        self.dialog.ui.setupUi(self.dialog)
