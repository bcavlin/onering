import datetime
import re
import sip
import subprocess
import time

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
        self.thread_call = DialogConnectionsThread(self.parent(), 'validate')
        self.thread_call.start()

        while not self.thread_call.isFinished():
            self.parent().app.processEvents()
            time.sleep(0.1)

        if self.thread_call.result:
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
            self.thread_call_ns.gather_data = True
            self.thread_call_ns.start()

        else:
            self.thread_call_ns.gather_data = False
            self.dialog.ui.pushButton_start_netstat.setText('Start')
            self.stop_thread_ns()

    def __init__(self, parent):
        super().__init__(parent)
        sip.setapi('QString', 2)
        self.dialog = QDialog(parent)
        self.dialog.ui = Ui_DialogConnections()
        self.dialog.ui.setupUi(self.dialog)
        self.selected_index = -1
        self.thread_call = NotImplemented
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

    def get_table_model_data_in_array(self, table):
        """
        :param QtGui.QTableWidget table:
        :return:
        """
        model = table.model()
        data = []
        for row in range(model.rowCount()):
            data.append([])
            for column in range(model.columnCount()):
                index = model.index(row, column)
                # We suppose data are strings
                data[row].append(str(model.data(index)))

        return data

    def update_netstat(self, message_array):
        """
        :param message_array:
        :return:
        """
        self.thread_call_ns.gather_data = False  # pause processing

        data_list = self.get_table_model_data_in_array(self.dialog.ui.tableWidget)

        for message in message_array:
            row_data_index = -1
            row_data = []
            for idx, data in enumerate(data_list):
                if data[DialogConnections.COLUMN_NS_PROTO] == message[DialogConnections.COLUMN_NS_PROTO] \
                        and data[DialogConnections.COLUMN_NS_PROTO] == message[DialogConnections.COLUMN_NS_PROTO] \
                        and data[DialogConnections.COLUMN_NS_LOCAL_ADDR] == message[
                            DialogConnections.COLUMN_NS_LOCAL_ADDR] \
                        and data[DialogConnections.COLUMN_NS_LOCAL_PORT] == message[
                            DialogConnections.COLUMN_NS_LOCAL_PORT] \
                        and data[DialogConnections.COLUMN_NS_REMOTE_ADDR] == message[
                            DialogConnections.COLUMN_NS_REMOTE_ADDR] \
                        and data[DialogConnections.COLUMN_NS_REMOTE_PORT] == message[
                            DialogConnections.COLUMN_NS_REMOTE_PORT] \
                        and data[DialogConnections.COLUMN_NS_PID] == message[DialogConnections.COLUMN_NS_PID]:
                    row_data_index = idx
                    row_data = data
                    break

            if row_data_index > -1 and row_data[DialogConnections.COLUMN_NS_STATE] != message[
                DialogConnections.COLUMN_NS_STATE]:
                self.update_ns_exiting_row(row_data_index, message)

            elif row_data_index > -1 and row_data[DialogConnections.COLUMN_NS_STATE] == message[
                DialogConnections.COLUMN_NS_STATE]:
                pass
            else:
                print('Adding new row {0}'.format(message))
                self.update_ns_exiting_row(row_data_index, message)

        self.thread_call_ns.gather_data = True  # continue processing

    def update_ns_exiting_row(self, row, message):
        if row > -1:  # update
            self.dialog.ui.tableWidget.item(row, DialogConnections.COLUMN_NS_LAST).setText(
                message[DialogConnections.COLUMN_NS_LAST])
            self.dialog.ui.tableWidget.item(row, DialogConnections.COLUMN_NS_STATE).setText(
                message[DialogConnections.COLUMN_NS_STATE])
        else:  # add new
            row_position = 0
            self.dialog.ui.tableWidget.insertRow(row_position)

            item1 = QtGui.QTableWidgetItem(message[DialogConnections.COLUMN_NS_LAST])  # last
            item1.setTextAlignment(QtCore.Qt.AlignCenter)
            self.dialog.ui.tableWidget.setItem(row_position, DialogConnections.COLUMN_NS_LAST, item1)

            item2 = QtGui.QTableWidgetItem(message[DialogConnections.COLUMN_NS_PROTO])
            item2.setTextAlignment(QtCore.Qt.AlignCenter)
            self.dialog.ui.tableWidget.setItem(row_position, DialogConnections.COLUMN_NS_PROTO, item2)

            item3 = QtGui.QTableWidgetItem(message[DialogConnections.COLUMN_NS_LOCAL_ADDR])
            item3.setTextAlignment(QtCore.Qt.AlignCenter)
            self.dialog.ui.tableWidget.setItem(row_position, DialogConnections.COLUMN_NS_LOCAL_ADDR, item3)

            item4 = QtGui.QTableWidgetItem(message[DialogConnections.COLUMN_NS_LOCAL_PORT])
            item4.setTextAlignment(QtCore.Qt.AlignCenter)
            self.dialog.ui.tableWidget.setItem(row_position, DialogConnections.COLUMN_NS_LOCAL_PORT, item4)

            item5 = QtGui.QTableWidgetItem(message[DialogConnections.COLUMN_NS_REMOTE_ADDR])
            item5.setTextAlignment(QtCore.Qt.AlignCenter)
            self.dialog.ui.tableWidget.setItem(row_position, DialogConnections.COLUMN_NS_REMOTE_ADDR, item5)

            item6 = QtGui.QTableWidgetItem(message[DialogConnections.COLUMN_NS_REMOTE_PORT])
            item6.setTextAlignment(QtCore.Qt.AlignCenter)
            self.dialog.ui.tableWidget.setItem(row_position, DialogConnections.COLUMN_NS_REMOTE_PORT, item6)

            item7 = QtGui.QTableWidgetItem(message[DialogConnections.COLUMN_NS_STATE])
            item7.setTextAlignment(QtCore.Qt.AlignCenter)
            self.dialog.ui.tableWidget.setItem(row_position, DialogConnections.COLUMN_NS_STATE, item7)

            item8 = QtGui.QTableWidgetItem(message[DialogConnections.COLUMN_NS_PID])
            item8.setTextAlignment(QtCore.Qt.AlignCenter)
            self.dialog.ui.tableWidget.setItem(row_position, DialogConnections.COLUMN_NS_PID, item8)

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
                                   stderr=subprocess.DEVNULL, bufsize=1)
        parsed = []
        while not self.terminate_flag:
            output = process.stdout.readline().decode('utf-8')
            if output == '' and process.poll() is not None:
                break
            if output and self.gather_data:
                if output.startswith('Active Internet connections') and parsed:
                    self.emit(SIGNAL('update_netstat'), parsed)
                    parsed = []
                    time.sleep(1)
                else:
                    line = self.split_netstat_message(output.strip())
                    if line:
                        parsed.append(line)

        process.kill()
        print('netstat process completed')

    @staticmethod
    def split_netstat_message(message):
        parsed = []
        lines = message.splitlines()
        for line in lines:
            match = re.match(
                r'^(tcp6|udp6|tcp|udp)\s*\d+\s*\d+\s*([.:0-9a-zA-Z]*)\s*([.:0-9a-zA-Z*]*)\s*(=?[A-Z_]*)\s*(\d*)/.*$',
                line)
            if match:
                # order
                # protocol, local addr, local port, remote addr, remote port, state, pid, appl, sha256, last
                parsed.append(match.group(1).strip())  # protocol

                match2 = re.match(r'([.:0-9a-zA-Z*]*):(\d+)$', match.group(2).strip())
                parsed.append(match2.group(1))  # ip from address
                parsed.append(match2.group(2))  # ip from port

                match3 = re.match(r'([.:0-9a-zA-Z*]*):(\d+|\*)$', match.group(3).strip())
                parsed.append(match3.group(1))  # ip remote address
                parsed.append(match3.group(2))  # ip remote port

                parsed.append(match.group(4).strip())  # state
                parsed.append(match.group(5).strip())  # pid
                parsed.append('')  # appl
                parsed.append('')  # sha256
                parsed.append(datetime.datetime.now().isoformat())  # last

        return parsed

    def is_local(self):
        return self.parent().selected_connection.ip == '127.0.0.1'

    def __init__(self, parent, command='validate'):
        QThread.__init__(self, parent)
        self.command = command
        # this holds string result
        self.result = ''
        # this holds parsed data ready for processing into GUI
        self.data = []
        self.gather_data = False
        self.terminate_flag = False

    def run(self):
        if self.command == 'validate':
            self.validate_command()
        elif self.command == 'execute netstat':
            self.execute_command()
