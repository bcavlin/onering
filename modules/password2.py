import datetime

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QDialog, QListWidgetItem

from modules.commons import ValidateConnectionThread, validate_ip_address, Connection
from modules.dialogPassword_ui import Ui_DialogPassword


class DialogPassword(QDialog, Ui_DialogPassword):
    def __init__(self, parent):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.connect(self.previousConnectionsComboBox, QtCore.SIGNAL("currentIndexChanged(int)"),
                     self.change_selection)
        self.connect(self.useKeyFileCheckBox, QtCore.SIGNAL("stateChanged(int)"),
                     self.use_key_file)
        self.pushButton_ok.clicked.connect(self.clicked_ok)
        self.pushButton_cancel.clicked.connect(self.clicked_cancel)
        self.pushButton_addNew.clicked.connect(self.clicked_new)
        self.pushButton_remove.clicked.connect(self.clicked_remove)

    def load_connections(self):
        for connection in self.parent().connections:
            self.previousConnectionsComboBox.addItem(connection.username + '@' + connection.ip, connection)
        self.previousConnectionsComboBox.setCurrentIndex(0)
        self.change_selection()

    def change_selection(self):
        self.pushButton_ok.setEnabled(False)

        index = self.previousConnectionsComboBox.currentIndex()
        data = self.previousConnectionsComboBox.itemData(index, QtCore.Qt.UserRole)
        if data:
            thread_call = ValidateConnectionThread(self.parent(), data)
            thread_call.start()
            thread_call.wait()

            if thread_call.result:
                self.parent().current_selection = data
                self.iPAddressLineEdit.setText(self.parent().current_selection.ip)
                self.usernameLineEdit.setText(self.parent().current_selection.username)
                self.passwordLineEdit.setText(self.parent().current_selection.password)
                self.sudoPasswordLineEdit.setText(self.parent().current_selection.sudo_password)
                self.rememberPasswordsCheckBox.setChecked(self.parent().current_selection.store_password)
                self.useKeyFileCheckBox.setChecked(self.parent().current_selection.use_key_file)
                self.add_message(data.ip + ' is [up]')
                self.pushButton_ok.setEnabled(True)
            else:
                self.add_message(data.ip + ' is [down]')

    def add_message(self, message):
        self.listWidget_messages.insertItem(0, QListWidgetItem(datetime.datetime.now().isoformat() + ' > ' + message))

    def use_key_file(self):
        self.passwordLineEdit.setEnabled(not self.useKeyFileCheckBox.isChecked())

    def can_save_passwords(self):
        # can we save passwords
        return self.rememberPasswordsCheckBox.isChecked()

    def clicked_cancel(self):
        self.close()

    def clicked_ok(self):
        # validate IP
        # is_ok = validate_ip_address(self.iPAddressLineEdit.text())
        # if not is_ok:
        #     QtGui.QMessageBox.warning(self.parent(), "IP address invalid", "Please check the IP address you entered",
        #                               QtGui.QMessageBox.Ok)
        #     return

        # create new connection
        selected_connection = Connection()
        selected_connection.ip = self.iPAddressLineEdit.text().strip()
        selected_connection.username = self.usernameLineEdit.text().strip()
        selected_connection.password = self.passwordLineEdit.text().strip()
        selected_connection.sudo_password = self.sudoPasswordLineEdit.text().strip()
        selected_connection.store_password = self.rememberPasswordsCheckBox.isChecked()
        selected_connection.use_key_file = self.useKeyFileCheckBox.isChecked()

        connection_found = False
        # compare new with old connection
        for connection in self.parent().connections:
            if connection.ip == selected_connection.ip and connection.username == selected_connection.username:
                connection_found = True

        if not connection_found:
            # add new connection into list and parent items
            self.parent().connections.append(selected_connection)
            self.previousConnectionsComboBox.addItem(
                selected_connection.username + '@' + selected_connection.ip, selected_connection)
            self.previousConnectionsComboBox.setCurrentIndex(
                self.previousConnectionsComboBox.count() - 1)
        else:
            # if connection found then update current connection details with new ones
            for connection in self.parent().connections:
                if connection.get_title() == selected_connection.get_title():
                    connection.store_password = selected_connection.store_password
                    connection.use_key_file = selected_connection.use_key_file
                    connection.username = selected_connection.username
                    connection.password = selected_connection.password
                    connection.sudo_password = selected_connection.sudo_password
            index = self.previousConnectionsComboBox.currentIndex()
            self.previousConnectionsComboBox.setItemData(index, selected_connection)

        # set selected connection to new parameters in any case
        self.parent().selected_connection = selected_connection
        # encode(self.sudoPasswordLineEdit.text().rjust(32))
        self.close()

    def clicked_new(self):
        pass

    def clicked_remove(self):
        pass

