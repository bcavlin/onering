import subprocess

from PyQt4.QtGui import QDialog, QWidget

from modules.abstr import Abstr
from modules.dialogFirewall import Ui_DialogFirewall


class DialogFirewall(QWidget, Abstr):
    def validate_command(self):
        if not self.enabled:
            text = subprocess.Popen("ufw version", shell=True, stdout=subprocess.PIPE,
                                    stderr=subprocess.DEVNULL).stdout.read().decode('utf-8')

            if text.startswith('ufw'):
                self.enabled = True
                print('Enabled ufw command')

        return self.enabled

    def execute_command(self):
        if self.enabled:
            text = subprocess.Popen("echo %s | sudo -S ufw status numbered" % self.parent().decode(), shell=True, stdout=subprocess.PIPE,
                                    stderr=subprocess.DEVNULL).stdout.read().decode('utf-8')
            print(text)

    def __init__(self, parent):
        super().__init__(parent)
        self.dialog = QDialog(parent)
        self.dialog.ui = Ui_DialogFirewall()
        self.dialog.ui.setupUi(self.dialog)

        self.dialog.ui.pushButton_refresh.clicked.connect(self.execute_command)
