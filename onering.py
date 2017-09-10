import pickle
import sys

from PyQt4 import QtGui
from PyQt4.QtGui import QMainWindow, QSystemTrayIcon, QIcon, QMenu, QApplication
from screeninfo import get_monitors

import oneringui_ui
from modules.firewall import DialogFirewall
from modules.password import DialogPassword
from modules.variables import Connection


class OneRingApp(QMainWindow, oneringui_ui.Ui_MainWindow):
    def __init__(self, app):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.app = app
        self.connections = []

        self.tray = QSystemTrayIcon(self)
        self.dialog_password = DialogPassword(self)
        self.setup_connections()
        self.selected_connection = self.connections[0]
        self.dialog_firewall = DialogFirewall(self)

        self.setup_icon()
        self.setup_menu()

        self.pushButton_Firewall.clicked.connect(self.show_firewall_dialog)
        self.pushButton_sudo.clicked.connect(self.show_password_dialog)

    def setup_connections(self):
        try:
            self.connections = pickle.load(open('onering.p', 'rb'))
        except FileNotFoundError:
            self.connections.append(Connection())

        self.dialog_password.load_connections()
        self.setWindowTitle(self.windowTitle() + ' [' + self.connections[0].get_title() + ']')

    def close_data_exit(self):
        self.close_data()
        sys.exit(0)

    def close_data(self):
        for connection in self.connections:
            if not connection.store_password:
                connection.password = ''
                connection.sudo_password = ''

        pickle.dump(self.connections, open('onering.p', 'wb'))

    def closeEvent(self, QCloseEvent):
        self.close_data()
        super().closeEvent(QCloseEvent)

    def setup_icon(self):
        icon = QIcon("images/icon-hat-white.png")
        self.tray.setIcon(icon)

    def setup_menu(self):
        menu = QMenu()
        show_app = menu.addAction("Show")
        show_app.triggered.connect(self.show_application)
        show_app.setIcon(QIcon("images/S.png"))
        exit_action = menu.addAction("Exit")
        exit_action.triggered.connect(self.close_data_exit)
        exit_action.setIcon(QIcon("images/X.png"))
        self.tray.setContextMenu(menu)
        self.tray.show()

    def show_firewall_dialog(self):
        if len(self.selected_connection.sudo_password) > 0 and self.dialog_firewall.validate_command():
            self.dialog_firewall.dialog.setWindowTitle('Firewall (UFW): [' + self.selected_connection.get_title() + ']')
            self.dialog_firewall.dialog.ui.tableWidget.setRowCount(0)
            self.dialog_firewall.dialog.show()
        else:
            QtGui.QMessageBox.warning(self.parent(), "Password warning", "sudo password is required for this operation",
                                      QtGui.QMessageBox.Ok)

    def show_password_dialog(self):
        self.dialog_password.dialog.exec_()

    def show_application(self):
        self.show()


def main():
    app = QApplication(sys.argv)
    form = OneRingApp(app)
    m = get_monitors()[0]
    form.move(m.width - 250, 50)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
