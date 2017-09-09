import re
import sip
import subprocess

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QThread
from PyQt4.QtGui import QDialog, QWidget

from modules.abstr import Abstr
from modules.dialogFirewall_ui import Ui_DialogFirewall


class DialogFirewall(QWidget, Abstr):
    def validate_command(self):
        if not self.enabled:
            thread_call = DialogFirewallThread(self.parent(), 'validate')
            thread_call.start()

            while not thread_call.isFinished():
                self.parent().app.processEvents()

            print(thread_call.result)

            if thread_call.result.startswith('ufw'):
                self.enabled = True
            else:
                QtGui.QMessageBox.warning(self.parent(), "UFW not enabled", "Check if the UFW is installed",
                                          QtGui.QMessageBox.Ok)
                self.enabled = False

        return self.enabled

    def execute_command(self):
        if self.enabled:
            thread_call = DialogFirewallThread(self.parent(), 'execute')
            thread_call.start()

            while not thread_call.isFinished():
                self.parent().app.processEvents()

            if thread_call.data:
                # clear table data
                self.dialog.ui.tableWidget.setRowCount(0)
                self.selected_index = -1

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

            print(thread_call.result)

    def __init__(self, parent):
        super().__init__(parent)
        sip.setapi('QString', 2)
        self.dialog = QDialog(parent)
        self.dialog.ui = Ui_DialogFirewall()
        self.dialog.ui.setupUi(self.dialog)
        self.dialog.ui.pushButton_refresh.clicked.connect(self.execute_command)
        self.dialog.ui.tableWidget.setColumnWidth(0, 50)
        self.dialog.ui.tableWidget.setColumnWidth(1, 200)
        self.dialog.ui.tableWidget.setColumnWidth(2, 100)
        self.dialog.ui.tableWidget.setColumnWidth(3, 200)
        self.dialog.ui.tableWidget.clicked.connect(self.table_row_selected)
        self.selected_index = -1

    def table_row_selected(self):
        self.selected_index = self.dialog.ui.tableWidget.selectedIndexes()[0].row()


class DialogFirewallThread(QThread, Abstr):
    def execute_command(self):
        if self.parent().selected_connection.ip == '127.0.0.1':
            command = ["echo {0} | sudo -S ufw status numbered".format(self.parent().selected_connection.sudo_password)]
        else:
            command = ["sshpass", "-p", "{0}".format(self.parent().selected_connection.password), "ssh",
                       "{0}@{1}".format(self.parent().selected_connection.username,
                                        self.parent().selected_connection.ip),
                       "echo {0} | sudo -S ufw status numbered".format(self.parent().selected_connection.sudo_password)]

        self.result = subprocess.Popen(
            command,
            shell=False if len(command) > 1 else True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE).stdout.read().decode('utf-8')

        print(command)
        print(self.result)

        if self.result:
            lines = self.result.splitlines()
            to_start = 0
            action_start = 0
            from_start = 0
            for line in lines:
                parsed = []
                if re.match(r'^\s*To\s*Action\s*From', line):
                    to_start = line.find('To')
                    action_start = line.find('Action')
                    from_start = line.find('From')
                elif re.match(r'^\s*\[', line) and to_start > 0:
                    parsed.append(line[:to_start].strip())
                    parsed.append(line[to_start:action_start].strip())
                    parsed.append(line[action_start:from_start].strip())
                    parsed.append(line[from_start:].strip())
                    self.data.append(parsed)

    def validate_command(self):
        self.result = subprocess.Popen("ufw version", shell=True, stdout=subprocess.PIPE,
                                       stderr=subprocess.DEVNULL).stdout.read().decode('utf-8')

    def __init__(self, parent, command='validate'):
        # QThread.__init__(self, parent)
        # self.parent = parent  # needed for decode function
        super().__init__(parent)
        self.command = command
        # this holds string result
        self.result = ''
        # this holds parsed data ready for processing into GUI
        self.data = []

    def run(self):
        if self.command == 'validate':
            self.validate_command()
        else:
            self.execute_command()
