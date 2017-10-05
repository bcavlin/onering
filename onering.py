import logging
import pickle
import random
import sys

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QMainWindow, QSystemTrayIcon, QIcon, QMenu, QApplication
from screeninfo import get_monitors

import oneringui_ui
from modules.commons import Connection, ValidateConnectionThread
from modules.connections2 import WindowConnections
from modules.firewall import DialogFirewall
from modules.password import DialogPassword


class OneRingApp(QMainWindow, oneringui_ui.Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self, flags=QtCore.Qt.Window)
        self.setupUi(self)
        self.connections = []
        self.tray = QSystemTrayIcon(self)
        self.dialog_password = DialogPassword(self)
        self.setup_connections()
        self.selected_connection = self.connections[0]
        self.dialog_firewall = DialogFirewall(self)
        self.windows_list = []

        self.setup_icon()
        self.setup_menu()

        self.pushButton_Firewall.clicked.connect(self.show_firewall_dialog)
        self.pushButton_sudo.clicked.connect(self.show_password_dialog)
        self.pushButton_connections.clicked.connect(self.show_connections_dialog)
        logging.debug('Created main application')

    def setup_connections(self):
        logging.debug('setup_connections')
        try:
            logging.debug('Loading connections from pickle')
            self.connections = pickle.load(open('onering.p', 'rb'))
        except FileNotFoundError:
            self.connections.append(Connection())

        self.dialog_password.load_connections()
        self.setWindowTitle('OneRing [' + self.connections[0].get_title() + ']')

    def close_data_exit(self):
        logging.debug('close_data_exit')
        self.close_data()
        sys.exit(0)

    def close_data(self):
        logging.debug('close_data')
        for w in self.windows_list:  # type: QMainWindow
            w.close()

        for connection in self.connections:
            if not connection.store_password:
                connection.password = ''
                connection.sudo_password = ''

        pickle.dump(self.connections, open('onering.p', 'wb'))

    def closeEvent(self, QCloseEvent):
        logging.debug('closeEvent')
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

    def show_connections_dialog(self):
        thread_call = ValidateConnectionThread(self, self.selected_connection)
        thread_call.start()
        thread_call.wait()

        if thread_call.result:
            window_connection = WindowConnections(selected_connection=self.selected_connection)
            if len(self.selected_connection.sudo_password) > 0 and window_connection.validate_command():
                window_connection.setWindowTitle('Connections: [' + self.selected_connection.get_title() + ']')
                window_connection.move(random.randint(100, 500), random.randint(100, 300))
                self.windows_list.append(window_connection)  # save window so it is not garbage collected
                window_connection.show()
                self.remove_window()
            else:
                QtGui.QMessageBox.warning(self.parent(), "Requirements warning",
                                          "Required: sudo password, netstat, readlink, sha1sum",
                                          QtGui.QMessageBox.Ok)
        else:
            QtGui.QMessageBox.warning(self.parent(), "Connection warning",
                                      "We cannot establish connection to {0}".format(self.selected_connection.ip),
                                      QtGui.QMessageBox.Ok)

    def remove_window(self):
        for w in self.windows_list:
            if not w.isVisible():
                logging.debug('Removing > ' + w.windowTitle())
                self.windows_list.remove(w)

    def show_firewall_dialog(self):
        thread_call = ValidateConnectionThread(self, self.selected_connection)
        thread_call.start()
        thread_call.wait()

        if thread_call.result:
            if len(self.selected_connection.sudo_password) > 0 and self.dialog_firewall.validate_command():
                self.dialog_firewall.dialog.setWindowTitle(
                    'Firewall (UFW): [' + self.selected_connection.get_title() + ']')
                self.dialog_firewall.dialog.ui.tableWidget.setRowCount(0)
                self.dialog_firewall.dialog.move(random.randint(100, 800), random.randint(100, 500))
                self.dialog_firewall.dialog.show()
            else:
                QtGui.QMessageBox.warning(self.parent(), "Password warning",
                                          "sudo password is required for this operation",
                                          QtGui.QMessageBox.Ok)
        else:
            QtGui.QMessageBox.warning(self.parent(), "Connection warning",
                                      "We cannot establish conection to {0}".format(self.current_selection.ip),
                                      QtGui.QMessageBox.Ok)

    def show_password_dialog(self):
        self.dialog_password.dialog.move(random.randint(100, 800), random.randint(100, 500))
        self.dialog_password.dialog.exec_()
        self.setWindowTitle('OneRing [' + self.selected_connection.get_title() + ']')

    def show_application(self):
        self.show()


def main():
    logging.basicConfig(level=logging.DEBUG)
    app = QApplication(sys.argv)
    form = OneRingApp()
    m = get_monitors()[0]
    form.move(m.width - 250, 50)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
