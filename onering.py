import base64
import sys
import uuid

from Crypto.Cipher import AES
from PyQt4.QtGui import QMainWindow, QSystemTrayIcon, QIcon, QMenu, QApplication
from screeninfo import get_monitors

import oneringui
from modules.firewall import DialogFirewall
from modules.password import DialogPassword


class OneRingApp(QMainWindow, oneringui.Ui_MainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.tray = QSystemTrayIcon(self)

        self.setup_icon()
        self.setup_menu()
        self.dialog_password = DialogPassword(self)
        self.dialog_firewall = DialogFirewall(self)

        self.pushButton_Firewall.clicked.connect(self.show_firewall_dialog)

        self.cipher = AES.new(uuid.uuid4().hex, AES.MODE_ECB)
        self.secret = ''

    def encode(self, msg_text):
        return base64.b64encode(self.cipher.encrypt(msg_text))

    def decode(self):
        return self.cipher.decrypt(base64.b64decode(self.secret)).strip().decode("utf-8")

    def setup_icon(self):
        icon = QIcon("images/icon-hat-white.png")
        self.tray.setIcon(icon)

        icon2 = QIcon("images/icon-hat-white.png")
        # self.statusBar.addWidget(icon2)

    def setup_menu(self):
        menu = QMenu()
        show_app = menu.addAction("Show")
        show_app.triggered.connect(self.show_application)
        show_app.setIcon(QIcon("images/S.png"))
        exit_action = menu.addAction("Exit")
        exit_action.triggered.connect(sys.exit)
        exit_action.setIcon(QIcon("images/X.png"))
        self.tray.setContextMenu(menu)
        self.tray.show()

    def show_firewall_dialog(self):
        # global secret
        if self.secret == '':
            self.dialog_password.dialog.exec_()
            if len(self.dialog_password.get_text()) > 0:
                self.secret = self.encode(self.dialog_password.get_text_and_null().rjust(32))

        if len(self.secret) > 0 and self.dialog_firewall.validate_command():
            self.dialog_firewall.dialog.show()

    def show_application(self):
        self.show()


def main():
    app = QApplication(sys.argv)
    form = OneRingApp()
    m = get_monitors()[0]
    form.move(m.width - 250, 50)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
