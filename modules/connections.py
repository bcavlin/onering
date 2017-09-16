import datetime
import re
import sip
import subprocess

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QThread, SIGNAL
from PyQt4.QtGui import QWidget, QDialog

from modules.abstr import Abstr
from modules.commons import use_sshpass
from modules.dialogConnections_ui import Ui_DialogConnections


class DialogConnections(QWidget, Abstr):
    COLUMN_NS_PROTO = 0
    COLUMN_NS_LOCAL_ADDR = 1
    COLUMN_NS_LOCAL_PORT = 2
    COLUMN_NS_REMOTE_ADDR = 3
    COLUMN_NS_REMOTE_PORT = 4
    COLUMN_NS_STATE = 5
    COLUMN_NS_PID = 6
    COLUMN_NS_APPLICATION = 7
    COLUMN_NS_SHA256 = 8
    COLUMN_NS_LAST = 9

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
            self.connect(self.thread_call_ns, SIGNAL("update_netstat"), self.update_netstat)
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
        self.dialog.ui.tableWidget.setColumnWidth(DialogConnections.COLUMN_NS_PID, 70)
        self.dialog.ui.tableWidget.setColumnWidth(DialogConnections.COLUMN_NS_STATE, 130)
        self.dialog.ui.tableWidget.setColumnWidth(DialogConnections.COLUMN_NS_REMOTE_PORT, 70)
        self.dialog.ui.tableWidget.setColumnWidth(DialogConnections.COLUMN_NS_REMOTE_ADDR, 150)
        self.dialog.ui.tableWidget.setColumnWidth(DialogConnections.COLUMN_NS_LOCAL_PORT, 70)
        self.dialog.ui.tableWidget.setColumnWidth(DialogConnections.COLUMN_NS_LOCAL_ADDR, 150)
        self.dialog.ui.tableWidget.setColumnWidth(DialogConnections.COLUMN_NS_PROTO, 50)
        self.dialog.ui.tableWidget.setColumnWidth(DialogConnections.COLUMN_NS_LAST, 250)
        self.dialog.ui.tableWidget.setColumnWidth(DialogConnections.COLUMN_NS_APPLICATION, 400)
        self.dialog.ui.tableWidget.setColumnWidth(DialogConnections.COLUMN_NS_SHA256, 400)

        self.dialog.ui.pushButton_start_netstat.clicked.connect(self.execute_command)

    def update_netstat(self, message):
        print('Processing start {0}'.format(message))
        existing_row_found = -1
        for row in range(0, self.dialog.ui.tableWidget.rowCount() - 1):
            item1 = self.dialog.ui.tableWidget.item(row, DialogConnections.COLUMN_NS_PROTO)
            item1 = item1.text() if item1 else ''
            item2 = self.dialog.ui.tableWidget.item(row, DialogConnections.COLUMN_NS_LOCAL_ADDR)
            item2 = item2.text() if item2 else ''
            item3 = self.dialog.ui.tableWidget.item(row, DialogConnections.COLUMN_NS_LOCAL_PORT)
            item3 = item3.text() if item3 else ''
            item4 = self.dialog.ui.tableWidget.item(row, DialogConnections.COLUMN_NS_REMOTE_ADDR)
            item4 = item4.text() if item4 else ''
            item5 = self.dialog.ui.tableWidget.item(row, DialogConnections.COLUMN_NS_REMOTE_PORT)
            item5 = item5.text() if item5 else ''
            item6 = self.dialog.ui.tableWidget.item(row, DialogConnections.COLUMN_NS_PID)
            item6 = item6.text() if item6 else ''
            if item1 == message[
                0] and item2 == message[
                1] and item3 == message[
                2] and item4 == message[
                3] and item5 == message[
                4] and item6 == message[6]:
                existing_row_found = row
                break

        if existing_row_found > -1 and self.dialog.ui.tableWidget.item(existing_row_found,
                                                                       DialogConnections.COLUMN_NS_STATE).text() != \
                message[5]:
            self.update_ns_exiting_row(existing_row_found, message)
        elif existing_row_found > -1 and self.dialog.ui.tableWidget.item(existing_row_found,
                                                                         DialogConnections.COLUMN_NS_STATE).text() == \
                message[5]:
            pass
        else:
            self.update_ns_exiting_row(existing_row_found, message)

    def update_ns_exiting_row(self, row, message):
        if row > -1:  # update
            self.dialog.ui.tableWidget.item(row, DialogConnections.COLUMN_NS_LAST).setText(
                datetime.datetime.now().isoformat())
            self.dialog.ui.tableWidget.item(row, DialogConnections.COLUMN_NS_STATE).setText(message[5])
        else:  # add new
            row_position = 0
            self.dialog.ui.tableWidget.insertRow(row_position)

            item1 = QtGui.QTableWidgetItem(datetime.datetime.now().isoformat())  # last
            item1.setTextAlignment(QtCore.Qt.AlignCenter)
            self.dialog.ui.tableWidget.setItem(row_position, DialogConnections.COLUMN_NS_LAST, item1)

            item2 = QtGui.QTableWidgetItem(message[0])
            item2.setTextAlignment(QtCore.Qt.AlignCenter)
            self.dialog.ui.tableWidget.setItem(row_position, DialogConnections.COLUMN_NS_PROTO, item2)

            item3 = QtGui.QTableWidgetItem(message[1])
            item3.setTextAlignment(QtCore.Qt.AlignCenter)
            self.dialog.ui.tableWidget.setItem(row_position, DialogConnections.COLUMN_NS_LOCAL_ADDR, item3)

            item4 = QtGui.QTableWidgetItem(message[2])
            item4.setTextAlignment(QtCore.Qt.AlignCenter)
            self.dialog.ui.tableWidget.setItem(row_position, DialogConnections.COLUMN_NS_LOCAL_PORT, item4)

            item5 = QtGui.QTableWidgetItem(message[3])
            item5.setTextAlignment(QtCore.Qt.AlignCenter)
            self.dialog.ui.tableWidget.setItem(row_position, DialogConnections.COLUMN_NS_REMOTE_ADDR, item5)

            item6 = QtGui.QTableWidgetItem(message[4])
            item6.setTextAlignment(QtCore.Qt.AlignCenter)
            self.dialog.ui.tableWidget.setItem(row_position, DialogConnections.COLUMN_NS_REMOTE_PORT, item6)

            item7 = QtGui.QTableWidgetItem(message[5])
            item7.setTextAlignment(QtCore.Qt.AlignCenter)
            self.dialog.ui.tableWidget.setItem(row_position, DialogConnections.COLUMN_NS_STATE, item7)

            item8 = QtGui.QTableWidgetItem(message[6])
            item8.setTextAlignment(QtCore.Qt.AlignCenter)
            self.dialog.ui.tableWidget.setItem(row_position, DialogConnections.COLUMN_NS_PID, item8)

            print('Processing end {0}'.format(message))

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
                                  self.parent().selected_connection.sudo_password) + ["ssh", "{0}@{1}".format(
                self.parent().selected_connection.username, self.parent().selected_connection.ip), base_command]

        result = subprocess.Popen(command, shell=False if len(command) > 1 else True, stdout=subprocess.PIPE,
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
                                  self.parent().selected_connection.sudo_password) + ["ssh", "{0}@{1}".format(
                self.parent().selected_connection.username, self.parent().selected_connection.ip), base_command.format(
                self.parent().selected_connection.sudo_password)]

        process = subprocess.Popen(command, shell=False if len(command) > 1 else True, stdout=subprocess.PIPE,
                                   stderr=subprocess.DEVNULL)

        while not self.terminate_flag:
            output = process.stdout.readline().decode('utf-8')
            if output == '' and process.poll() is not None:
                break
            if output:
                parsed = self.split_netstat_message(output.strip())
                if parsed:
                    print('Sending {0}'.format(parsed))
                    self.emit(SIGNAL('update_netstat'), parsed)

        print('Netstat process completed')

    @staticmethod
    def split_netstat_message(message):
        parsed = []
        lines = message.splitlines()
        for line in lines:
            match = re.match(
                r'^(tcp6|udp6|tcp|udp)\s*\d+\s*\d+\s*([.:0-9a-zA-Z]*)\s*([.:0-9a-zA-Z*]*)\s*(=?[A-Z_]*)\s*(\d*)/.*$',
                line)
            if match:
                parsed.append(match.group(1).strip())  # protocol

                match2 = re.match(r'([.:0-9a-zA-Z*]*):(\d+)$', match.group(2).strip())
                parsed.append(match2.group(1))  # ip from address
                parsed.append(match2.group(2))  # ip from port

                match3 = re.match(r'([.:0-9a-zA-Z*]*):(\d+|\*)$', match.group(3).strip())
                parsed.append(match3.group(1))  # ip remote address
                parsed.append(match3.group(2))  # ip remote port

                parsed.append(match.group(4).strip())  # connection status
                parsed.append(match.group(5).strip())  # pid

        return parsed

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
