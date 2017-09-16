import re
import sip
import subprocess

from PyQt4 import QtGui
from PyQt4.QtCore import QThread, SIGNAL
from PyQt4.QtGui import QWidget, QDialog

from modules.abstr import Abstr
from modules.commons import use_sshpass
from modules.dialogConnections_ui import Ui_DialogConnections


class DialogConnections(QWidget, Abstr):
    def validate_command(self):
        thread_call = DialogConnectionsThread(self.parent(), 'validate')
        thread_call.start()

        while not thread_call.isFinished():
            self.parent().app.processEvents()

        if thread_call.result:
            enabled = True
        else:
            QtGui.QMessageBox.warning(self.parent(), "netstat not found", "Check if the netstat is installed",
                                      QtGui.QMessageBox.Ok)
            enabled = False

        return enabled

    def execute_command(self):
        if self.dialog.ui.pushButton_start_netstat.text() == 'Start':
            self.dialog.ui.pushButton_start_netstat.setText('Stop')

            self.dialog.ui.tableWidget.setRowCount(0)
            self.selected_index = -1

            self.thread_call_ns = DialogConnectionsThread(self.parent(), 'execute netstat')
            self.connect(self.thread_call_ns, SIGNAL("update_netstat(QString)"), self.update_netstat)
            self.thread_call_ns.start()

            while not self.thread_call_ns.isFinished():
                self.parent().app.processEvents()
        else:
            self.dialog.ui.pushButton_start_netstat.setText('Start')
            self.stop_thread_ns()

    def __init__(self, parent):
        super().__init__(parent)
        sip.setapi('QString', 2)
        self.dialog = QDialog(parent)
        self.dialog.ui = Ui_DialogConnections()
        self.dialog.ui.setupUi(self.dialog)
        self.selected_index = -1
        self.thread_call_ns = NotImplemented
        self.dialog.closeEvent = self.closeEvent
        self.dialog.ui.pushButton_start_netstat.setText('Start')

        self.dialog.ui.pushButton_start_netstat.clicked.connect(self.execute_command)

    def update_netstat(self, message):
        print(self.split_netstat_message(message.strip()))
        # self.dialog.ui.tableWidget.insertRow(0)
        # item1 = QtGui.QTableWidgetItem(data[0])  # number
        # item1.setTextAlignment(QtCore.Qt.AlignCenter)
        # self.dialog.ui.tableWidget.setItem(row_position, 0, item1)

    def split_netstat_message(self, message):
        parsed = []
        lines = message.splitlines()
        for line in lines:
            match = re.match(
                r'^(tcp6|udp6|tcp|udp)\s*\d+\s*\d+\s*([.:0-9a-zA-Z]*)\s*([.:0-9a-zA-Z*]*)\s*(=?[A-Z_]*)\s*(\d*)/.*$', line)
            if match:
                size = len(match.groups())
                parsed.append(match.group(1).strip())

                match2 = re.match(r'([.:0-9a-zA-Z*]*):(\d+)$', match.group(2).strip())
                parsed.append(match2.group(1))
                parsed.append(match2.group(2))

                match3 = re.match(r'([.:0-9a-zA-Z*]*):(\d+|\*)$', match.group(3).strip())
                parsed.append(match3.group(1))
                parsed.append(match3.group(2))

                parsed.append(match.group(4).strip())
                parsed.append(match.group(5).strip())

        return parsed

    def stop_thread_ns(self):
        if self.thread_call_ns.isRunning():
            self.thread_call_ns.terminate_flag = True
            self.thread_call_ns.wait(2)

    def closeEvent(self, QCloseEvent):
        self.stop_thread_ns()
        super().closeEvent(QCloseEvent)


class DialogConnectionsThread(QThread, Abstr):
    def validate_command(self):
        base_command = "which netstat | awk 'END{print NR}'"
        if self.is_local():
            command = [base_command]
        else:
            command = use_sshpass(self.parent().selected_connection.use_key_file,
                                  self.parent().selected_connection.sudo_password) + ["ssh",
                                                                                      "{0}@{1}".format(
                                                                                          self.parent().selected_connection.username,
                                                                                          self.parent().selected_connection.ip),
                                                                                      base_command]

        result = subprocess.Popen(command,
                                  shell=False if len(command) > 1 else True,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.DEVNULL).stdout.read().decode('utf-8').strip()
        print('netstat ' + result)

        if result == '1':
            self.result = True
        else:
            self.result = False

    def execute_command(self):
        base_command = "echo {0} | sudo -S netstat -antupc"
        if self.is_local():
            command = [base_command.format(self.parent().selected_connection.sudo_password)]
        else:
            command = use_sshpass(self.parent().selected_connection.use_key_file,
                                  self.parent().selected_connection.sudo_password) + ["ssh",
                                                                                      "{0}@{1}".format(
                                                                                          self.parent().selected_connection.username,
                                                                                          self.parent().selected_connection.ip),
                                                                                      base_command.format(
                                                                                          self.parent().selected_connection.sudo_password)]

        process = subprocess.Popen(command,
                                   shell=False if len(command) > 1 else True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.DEVNULL)

        while not self.terminate_flag:
            output = process.stdout.readline().decode('utf-8')
            if output == '' and process.poll() is not None:
                break
            if output:
                self.emit(SIGNAL('update_netstat(QString)'), output.strip())

        print('process done')

    def is_local(self):
        return self.parent().selected_connection.ip == '127.0.0.1'

    def __init__(self, parent, command='validate'):
        super().__init__(parent)
        self.command = command
        # this holds string result
        self.result = ''
        # this holds parsed data ready for processing into GUI
        self.data = []
        self.status = False
        self.terminate_flag = False

    def run(self):
        if self.command == 'validate':
            self.validate_command()
        elif self.command == 'execute netstat':
            self.execute_command()
