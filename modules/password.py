from PyQt4.QtGui import QDialog, QWidget

from modules.dialogPassword import Ui_DialogPassword


class DialogPassword(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.dialog = QDialog(parent)
        self.dialog.ui = Ui_DialogPassword()
        self.dialog.ui.setupUi(self.dialog)

    def get_text_and_null(self):
        text = self.dialog.ui.passwordLineEdit.text()
        self.dialog.ui.passwordLineEdit.setText('')
        return text
