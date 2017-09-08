import re
import subprocess

from PyQt4 import QtGui
from PyQt4.QtCore import QThread
from PyQt4.QtGui import QDialog, QWidget

from modules.abstr import Abstr
from modules.dialogFirewall import Ui_DialogFirewall


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
                for data in thread_call.data:
                    row_position = self.dialog.ui.tableWidget.rowCount()
                    self.dialog.ui.tableWidget.insertRow(row_position)
                    self.dialog.ui.tableWidget.setItem(row_position, 0, QtGui.QTableWidgetItem(data[0]))
                    self.dialog.ui.tableWidget.setItem(row_position, 1, QtGui.QTableWidgetItem(data[1]))
                    self.dialog.ui.tableWidget.setItem(row_position, 2, QtGui.QTableWidgetItem(data[2]))
                    self.dialog.ui.tableWidget.setItem(row_position, 3, QtGui.QTableWidgetItem(data[3]))

            print(thread_call.result)

    def __init__(self, parent):
        super().__init__(parent)
        self.dialog = QDialog(parent)
        self.dialog.ui = Ui_DialogFirewall()
        self.dialog.ui.setupUi(self.dialog)
        self.dialog.ui.pushButton_refresh.clicked.connect(self.execute_command)


class DialogFirewallThread(QThread, Abstr):
    def execute_command(self):
        self.result = subprocess.Popen("echo %s | sudo -S ufw status numbered" % self.parent.decode(),
                                       shell=True,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.DEVNULL).stdout.read().decode('utf-8')
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
        QThread.__init__(self)
        self.command = command
        self.parent = parent  # needed for decode function
        self.result = ''  # this holds string result
        self.data = []  # this holds parsed data ready for processing into GUI

    def __del__(self):
        self.wait()

    def run(self):
        if self.command == 'validate':
            self.validate_command()
        else:
            self.execute_command()
