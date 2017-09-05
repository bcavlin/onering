import base64
import sys
import uuid

from Crypto.Cipher import AES
from PyQt4 import QtGui
from PyQt4.QtGui import QIcon
from screeninfo import get_monitors

import oneringui
from modules.firewall import DialogFirewall
from modules.password import DialogPassword

cipher = AES.new(uuid.uuid4().hex, AES.MODE_ECB)
secret = ''


def encode(msg_text):
    return base64.b64encode(cipher.encrypt(msg_text))


def decode(encoded):
    return cipher.decrypt(base64.b64decode(encoded)).strip()


class OneRingApp(QtGui.QMainWindow, oneringui.Ui_MainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)  # oneringui
        self.tray = QtGui.QSystemTrayIcon()

        self.setup_icon()
        self.setup_menu()
        self.dialog_password = DialogPassword(self)
        self.dialog_firewall = DialogFirewall(self)

        self.pushButton_Firewall.clicked.connect(self.show_firewall_dialog)

    def setup_icon(self):
        icon = QtGui.QIcon("images/icon-hat-white.png")
        self.tray.setIcon(icon)

    def setup_menu(self):
        menu = QtGui.QMenu()
        show_app = menu.addAction("Show")
        show_app.triggered.connect(self.show_application)
        show_app.setIcon(QIcon("images/S.png"))
        exit_action = menu.addAction("Exit")
        exit_action.triggered.connect(sys.exit)
        exit_action.setIcon(QIcon("images/X.png"))
        self.tray.setContextMenu(menu)
        self.tray.show()

    def show_firewall_dialog(self):
        global secret
        if secret == '':
            self.dialog_password.dialog.exec_()
            secret = encode(self.dialog_password.get_text_and_null().rjust(32))
            print(secret)
            print(decode(secret))

        self.dialog_firewall.dialog.show()

    def show_application(self):
        self.show()


def main():
    app = QtGui.QApplication(sys.argv)
    form = OneRingApp()
    m = get_monitors()[0]
    form.move(m.width - 250, 50)
    app.exec_()


if __name__ == '__main__':
    main()
