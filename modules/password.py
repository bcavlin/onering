import sip
import subprocess

from PyQt4 import QtCore
from PyQt4.QtCore import QThread
from PyQt4.QtGui import QDialog, QWidget, QDialogButtonBox, QListWidgetItem

from modules.dialogPassword_ui import Ui_DialogPassword
from modules.variables import Connection


class DialogPassword(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        sip.setapi('QString', 2)
        self.dialog = QDialog(parent)
        self.dialog.ui = Ui_DialogPassword()
        self.dialog.ui.setupUi(self.dialog)
        self.dialog.ui.buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.clicked_ok)
        self.dialog.ui.buttonBox.button(QDialogButtonBox.Cancel).clicked.connect(self.clicked_cancel)

        self.connect(self.dialog.ui.previousConnectionsComboBox, QtCore.SIGNAL("currentIndexChanged(const QString&)"),
                     self.change_selection)

    def clicked_ok(self):
        selected_connection = Connection()
        selected_connection.ip = self.dialog.ui.iPAddressLineEdit.text()
        selected_connection.username = self.dialog.ui.usernameLineEdit.text()
        selected_connection.password = self.dialog.ui.passwordLineEdit.text()
        selected_connection.sudo_password = self.dialog.ui.sudoPasswordLineEdit.text()

        connection_found = False
        for connection in self.parent().connections:
            if connection.ip == selected_connection.ip and connection.username == selected_connection.username:
                connection_found = True

        self.parent().selected_connection = selected_connection

        if not connection_found:
            self.parent().connections.append(selected_connection)
            self.dialog.ui.previousConnectionsComboBox.addItem(
                selected_connection.username + '@' + selected_connection.ip, selected_connection)
        else:
            for connection in self.parent().connections:
                if connection.get_title() == selected_connection.get_title():
                    connection.username = selected_connection.username
                    connection.password = selected_connection.password
                    connection.sudo_password = selected_connection.sudo_password

            index = self.dialog.ui.previousConnectionsComboBox.currentIndex()
            self.dialog.ui.previousConnectionsComboBox.setItemData(index, selected_connection)

        # encode(self.dialog.ui.sudoPasswordLineEdit.text().rjust(32))
        self.dialog.close()

    def can_save_passwords(self):
        return self.dialog.ui.rememberPasswordsCheckBox.isChecked()

    def clicked_cancel(self):
        # self.dialog.ui.passwordLineEdit.setText('')
        # self.dialog.ui.sudoPasswordLineEdit.setText('')
        self.dialog.close()

    def load_connections(self):
        for connection in self.parent().connections:
            print('c ' + connection.ip)
            self.dialog.ui.previousConnectionsComboBox.addItem(connection.username + '@' + connection.ip, connection)

        self.dialog.ui.previousConnectionsComboBox.setCurrentIndex(0)
        self.change_selection()

    def add_message(self, message):
        self.dialog.ui.listWidget_messages.addItem(QListWidgetItem(message))

    def change_selection(self):
        self.dialog.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)

        index = self.dialog.ui.previousConnectionsComboBox.currentIndex()
        data = self.dialog.ui.previousConnectionsComboBox.itemData(index, QtCore.Qt.UserRole)
        if data:
            self.parent().current_selection = data
            self.dialog.ui.iPAddressLineEdit.setText(self.parent().current_selection.ip)
            self.dialog.ui.usernameLineEdit.setText(self.parent().current_selection.username)
            self.dialog.ui.passwordLineEdit.setText(self.parent().current_selection.password)
            self.dialog.ui.sudoPasswordLineEdit.setText(self.parent().current_selection.sudo_password)

            thread_call = DialogPasswordThread(self.parent(), self.parent().current_selection.ip)
            thread_call.start()

            while not thread_call.isFinished():
                self.parent().app.processEvents()

            if thread_call.result:
                self.add_message(self.parent().current_selection.ip + ' is up')
                self.dialog.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)
            else:
                self.add_message(self.parent().current_selection.ip + ' is down')


class DialogPasswordThread(QThread):
    def __init__(self, parent, host):
        super().__init__(parent)
        self.result = ''
        self.host = host

    def run(self):
        command = ["nmap -oG - -sP {0} | awk '/Status: Up/{{print $0}}'".format(self.host)]

        self.result = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL).stdout.read().decode('utf-8')
