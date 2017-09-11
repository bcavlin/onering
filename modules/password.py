import sip
import subprocess

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QThread
from PyQt4.QtGui import QDialog, QWidget, QDialogButtonBox, QListWidgetItem

from modules.dialogPassword_ui import Ui_DialogPassword
from modules.variables import Connection, validate_ip_address


class DialogPassword(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        # string behave like str
        sip.setapi('QString', 2)
        self.dialog = QDialog(parent)
        self.dialog.ui = Ui_DialogPassword()
        # create ui
        self.dialog.ui.setupUi(self.dialog)
        # setup what buttons do
        self.dialog.ui.buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.clicked_ok)
        self.dialog.ui.buttonBox.button(QDialogButtonBox.Cancel).clicked.connect(self.clicked_cancel)
        # setup signal for the item change in combobox
        self.connect(self.dialog.ui.previousConnectionsComboBox, QtCore.SIGNAL("currentIndexChanged(int)"),
                     self.change_selection)
        self.connect(self.dialog.ui.useKeyFileCheckBox, QtCore.SIGNAL("stateChanged(int)"),
                     self.use_key_file)

    def clicked_ok(self):

        # validate IP
        is_ok = validate_ip_address(self.dialog.ui.iPAddressLineEdit.text())
        if not is_ok:
            QtGui.QMessageBox.warning(self.parent(), "IP address invalid", "Please check your IP address",
                                      QtGui.QMessageBox.Ok)
            return

        # create new connection
        selected_connection = Connection()
        selected_connection.ip = self.dialog.ui.iPAddressLineEdit.text()
        selected_connection.username = self.dialog.ui.usernameLineEdit.text()
        selected_connection.password = self.dialog.ui.passwordLineEdit.text()
        selected_connection.sudo_password = self.dialog.ui.sudoPasswordLineEdit.text()
        selected_connection.store_password = self.dialog.ui.rememberPasswordsCheckBox.isChecked()
        selected_connection.use_key_file = self.dialog.ui.useKeyFileCheckBox.isChecked()

        connection_found = False
        # compare new with old connection
        for connection in self.parent().connections:
            if connection.ip == selected_connection.ip and connection.username == selected_connection.username:
                connection_found = True

        # set selected connection to new parameters in any case
        self.parent().selected_connection = selected_connection

        if not connection_found:
            # add new connection into list and parent items
            self.parent().connections.append(selected_connection)
            self.dialog.ui.previousConnectionsComboBox.addItem(
                selected_connection.username + '@' + selected_connection.ip, selected_connection)
        else:
            # if connection found then update current connection details with new ones
            for connection in self.parent().connections:
                if connection.get_title() == selected_connection.get_title():
                    connection.store_password = selected_connection.store_password
                    connection.use_key_file = selected_connection.use_key_file
                    connection.username = selected_connection.username
                    connection.password = selected_connection.password
                    connection.sudo_password = selected_connection.sudo_password

            index = self.dialog.ui.previousConnectionsComboBox.currentIndex()
            self.dialog.ui.previousConnectionsComboBox.setItemData(index, selected_connection)

        # encode(self.dialog.ui.sudoPasswordLineEdit.text().rjust(32))
        self.dialog.close()

    def can_save_passwords(self):
        # can we save passwords
        return self.dialog.ui.rememberPasswordsCheckBox.isChecked()

    def clicked_cancel(self):
        self.dialog.close()

    def load_connections(self):
        for connection in self.parent().connections:
            self.dialog.ui.previousConnectionsComboBox.addItem(connection.username + '@' + connection.ip, connection)

        self.dialog.ui.previousConnectionsComboBox.setCurrentIndex(0)
        self.change_selection()

    def add_message(self, message):
        self.dialog.ui.listWidget_messages.addItem(QListWidgetItem(message))

    def use_key_file(self):
        self.dialog.ui.passwordLineEdit.setEnabled(not self.dialog.ui.useKeyFileCheckBox.isChecked())

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
            self.dialog.ui.rememberPasswordsCheckBox.setChecked(self.parent().current_selection.store_password)
            self.dialog.ui.useKeyFileCheckBox.setChecked(self.parent().current_selection.use_key_file)

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
        self.command = ''

    def run(self):
        self.command = ["nmap -oG - -sP -PA22 {0} | awk '/Status: Up/{{print $0}}'".format(self.host)]

        self.result = subprocess.Popen(
            self.command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL).stdout.read().decode('utf-8')
