from PyQt4.QtGui import QDialog, QWidget, QDialogButtonBox

from modules.dialogPassword import Ui_DialogPassword


class DialogPassword(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.dialog = QDialog(parent)
        self.dialog.ui = Ui_DialogPassword()
        self.dialog.ui.setupUi(self.dialog)
        self.dialog.ui.buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.clicked_ok)
        self.dialog.ui.buttonBox.button(QDialogButtonBox.Cancel).clicked.connect(self.clicked_cancel)

    def clicked_ok(self):
        self.dialog.close()

    def clicked_cancel(self):
        self.dialog.ui.passwordLineEdit.setText('')
        self.dialog.close()

    def get_text_and_null(self):
        text = self.dialog.ui.passwordLineEdit.text()
        self.dialog.ui.passwordLineEdit.setText('')
        return text

    def get_text(self):
        text = self.dialog.ui.passwordLineEdit.text()
        return text
