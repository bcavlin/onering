import re
import sip
import time

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QThread
from PyQt4.QtGui import QDialog, QWidget

from modules.abstr import Abstr
from modules.commons import run_remote_command
from modules.dialogFirewall_ui import Ui_DialogFirewall


class DialogFirewall(QWidget, Abstr):
    def enable_disable_firewall(self):
        thread_call = DialogFirewallThread(self.parent(), self.dialog.ui.pushButton_enabled.text().lower())
        thread_call.start()

        while not thread_call.isFinished():
            self.parent().app.processEvents()
            time.sleep(0.1)

        self.execute_command()

    def validate_command(self):
        thread_call = DialogFirewallThread(self.parent(), 'validate')
        thread_call.start()

        while not thread_call.isFinished():
            self.parent().app.processEvents()
            time.sleep(0.1)

        if thread_call.result:
            enabled = True
        else:
            QtGui.QMessageBox.warning(self.parent(), "UFW not found", "Check if the UFW is installed",
                                      QtGui.QMessageBox.Ok)
            enabled = False

        return enabled

    def execute_command(self):
        self.dialog.ui.tableWidget.setRowCount(0)
        self.selected_index = -1

        thread_call = DialogFirewallThread(self.parent(), 'execute')
        thread_call.start()

        while not thread_call.isFinished():
            self.parent().app.processEvents()
            time.sleep(0.1)

        self.dialog.ui.pushButton_enabled.setEnabled(True)
        self.dialog.ui.pushButton_remove.setEnabled(False)

        if thread_call.status:
            self.dialog.ui.pushButton_enabled.setText('Disable')
            self.dialog.ui.pushButton_insert.setEnabled(True)
        else:
            self.dialog.ui.pushButton_enabled.setText('Enable')
            self.dialog.ui.pushButton_insert.setEnabled(False)

        if thread_call.data:
            # parse new data
            for data in thread_call.data:
                row_position = self.dialog.ui.tableWidget.rowCount()
                self.dialog.ui.tableWidget.insertRow(row_position)
                item1 = QtGui.QTableWidgetItem(data[0])  # number
                item1.setTextAlignment(QtCore.Qt.AlignCenter)
                self.dialog.ui.tableWidget.setItem(row_position, 0, item1)
                item2 = QtGui.QTableWidgetItem(data[1])  # to
                item2.setTextAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
                self.dialog.ui.tableWidget.setItem(row_position, 1, item2)
                item3 = QtGui.QTableWidgetItem(data[2])  # action
                item3.setTextAlignment(QtCore.Qt.AlignCenter)
                self.dialog.ui.tableWidget.setItem(row_position, 2, item3)
                item4 = QtGui.QTableWidgetItem(data[3])  # from
                item4.setTextAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
                self.dialog.ui.tableWidget.setItem(row_position, 3, item4)

    def __init__(self, parent):
        super().__init__(parent)
        sip.setapi('QString', 2)
        self.dialog = QDialog(parent)
        self.dialog.ui = Ui_DialogFirewall()
        self.dialog.ui.setupUi(self.dialog)
        self.dialog.ui.tableWidget.setColumnWidth(0, 50)
        self.dialog.ui.tableWidget.setColumnWidth(1, 200)
        self.dialog.ui.tableWidget.setColumnWidth(2, 100)
        self.dialog.ui.tableWidget.setColumnWidth(3, 200)
        self.dialog.ui.tableWidget.clicked.connect(self.table_row_selected)
        self.selected_index = -1

        self.dialog.ui.pushButton_refresh.clicked.connect(self.execute_command)
        self.dialog.ui.pushButton_enabled.clicked.connect(self.enable_disable_firewall)

    def table_row_selected(self):
        self.selected_index = self.dialog.ui.tableWidget.selectedIndexes()[0].row()
        self.dialog.ui.pushButton_remove.setEnabled(True)


class DialogFirewallThread(QThread, Abstr):
    def __init__(self, parent, command='validate'):
        super().__init__(parent)
        self.command = command
        # this holds string result
        self.result = ''
        # this holds parsed data ready for processing into GUI
        self.data = []
        self.status = False

    def run(self):
        if self.command == 'validate':
            self.validate_command()
        elif self.command == 'execute':
            self.execute_command()
        elif self.command == 'enable':
            self.enable_firewall()
        elif self.command == 'disable':
            self.disable_firewall()

    def enable_firewall(self):
        process = run_remote_command("ufw --force enable",
                                     self.parent().selected_connection.ip,
                                     self.parent().selected_connection.username,
                                     self.parent().selected_connection.password,
                                     self.parent().selected_connection.use_key_file,
                                     self.parent().selected_connection.sudo_password,
                                     use_sudo=True)
        self.result = process.stdout.read().decode('utf-8').strip()
        print(self.result)

    def disable_firewall(self):
        process = run_remote_command("ufw disable",
                                     self.parent().selected_connection.ip,
                                     self.parent().selected_connection.username,
                                     self.parent().selected_connection.password,
                                     self.parent().selected_connection.use_key_file,
                                     self.parent().selected_connection.sudo_password,
                                     use_sudo=True)
        self.result = process.stdout.read().decode('utf-8').strip()
        print(self.result)

    def execute_command(self):
        process = run_remote_command("ufw status numbered",
                                     self.parent().selected_connection.ip,
                                     self.parent().selected_connection.username,
                                     self.parent().selected_connection.password,
                                     self.parent().selected_connection.use_key_file,
                                     self.parent().selected_connection.sudo_password,
                                     use_sudo=True)
        self.result = process.stdout.read().decode('utf-8').strip()
        print(self.result)

        if self.result:
            self.split_message()

    def split_message(self):
        lines = self.result.splitlines()
        for line in lines:
            parsed = []
            match_status = re.match(r'^Status:\s*(.*)', line)
            if match_status:
                self.status = True if match_status.group(1).strip() == 'active' else False
            else:
                match = re.match(r'^(\[.*\])\s*(.*)\s*(ALLOW|DENY|DROP|REJECT)\s(IN|OUT)?\s*(.*)', line)
                if match:
                    size = len(match.groups())
                    parsed.append(match.group(1).strip())
                    parsed.append(match.group(2).strip())
                    if size == 4:
                        parsed.append(match.group(3).strip())
                        parsed.append(match.group(4).strip())
                    else:
                        parsed.append(match.group(3).strip() + ' ' + match.group(4).strip())
                        parsed.append(match.group(5).strip())
                    self.data.append(parsed)

    def validate_command(self):
        process = run_remote_command("which ufw | awk 'END{{print NR}}'",
                                     self.parent().selected_connection.ip,
                                     self.parent().selected_connection.username,
                                     self.parent().selected_connection.password,
                                     self.parent().selected_connection.use_key_file,
                                     self.parent().selected_connection.sudo_password,
                                     use_sudo=True)
        self.result = process.stdout.read().decode('utf-8').strip()
        print(self.result)

        if self.result == '1':
            self.result = True
        else:
            self.result = False
