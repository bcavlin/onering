import datetime
import re
import sip
import time

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QThread, SIGNAL, Qt
from PyQt4.QtGui import QWidget, QDialog, QStandardItemModel, QStandardItem

from modules.abstr import Abstr
from modules.commons import run_remote_command
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
    COLUMN_NS_SHA1 = 8
    COLUMN_NS_LAST = 9

    def __init__(self, parent):
        super().__init__(parent)
        sip.setapi('QString', 2)
        self.dialog = QDialog(parent)
        self.dialog.ui = Ui_DialogConnections()
        self.dialog.ui.setupUi(self.dialog)
        self.dialog.resize(1200, self.dialog.height())
        self.setup_ns_table_view(self.dialog.ui.tableView)
        self.selected_index = -1
        self.thread_call = NotImplemented
        self.thread_call_ns = NotImplemented
        self.dialog.closeEvent = self.closeEvent
        self.dialog.ui.pushButton_start_netstat.setText('Start')

        self.dialog.ui.pushButton_start_netstat.clicked.connect(self.execute_command)

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

            self.dialog.ui.tableView.model().reset()
            self.selected_index = -1

            self.thread_call_ns = DialogConnectionsThread(self.parent(), 'execute netstat')
            self.connect(self.thread_call_ns, SIGNAL("update_netstat"), self.update_netstat)
            self.thread_call_ns.gather_data = True
            self.thread_call_ns.start()

        else:
            self.thread_call_ns.gather_data = False
            self.dialog.ui.pushButton_start_netstat.setText('Start')
            self.stop_thread_ns()

    def setup_ns_table_view(self, table):
        """
        :param QtGui.QTableView table:
        :return:
        """
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(
            ['Prt', 'Local Addr', 'L. Port', 'Remote Addr', 'R. Port', 'State', 'PID', 'Application', 'SHA1',
             'Last'])

        model.setHeaderData(DialogConnections.COLUMN_NS_APPLICATION, Qt.Horizontal, Qt.AlignLeft, Qt.TextAlignmentRole)
        model.setHeaderData(DialogConnections.COLUMN_NS_SHA1, Qt.Horizontal, Qt.AlignLeft, Qt.TextAlignmentRole)

        table.setModel(model)

        table.setColumnWidth(DialogConnections.COLUMN_NS_PID, 100)
        table.setColumnWidth(DialogConnections.COLUMN_NS_STATE, 130)
        table.setColumnWidth(DialogConnections.COLUMN_NS_REMOTE_PORT, 70)
        table.setColumnWidth(DialogConnections.COLUMN_NS_REMOTE_ADDR, 150)
        table.setColumnWidth(DialogConnections.COLUMN_NS_LOCAL_PORT, 70)
        table.setColumnWidth(DialogConnections.COLUMN_NS_LOCAL_ADDR, 150)
        table.setColumnWidth(DialogConnections.COLUMN_NS_PROTO, 50)
        table.setColumnWidth(DialogConnections.COLUMN_NS_LAST, 250)
        table.setColumnWidth(DialogConnections.COLUMN_NS_APPLICATION, 400)
        table.setColumnWidth(DialogConnections.COLUMN_NS_SHA1, 400)

        header = table.horizontalHeader()
        header.setDefaultAlignment(Qt.AlignHCenter)

    def get_table_model_data_in_array(self, table):
        """
        :param QtGui.QTableView table:
        :return:
        """
        model = table.model()
        data = []
        for row in range(model.rowCount()):
            data.append([])
            for column in range(model.columnCount()):
                index = model.index(row, column)
                data[row].append(str(model.data(index)))

        return data

    def update_netstat(self, message_array):
        """
        :param message_array:
        :return:
        """
        self.thread_call_ns.gather_data = False  # pause processing

        data_list = self.get_table_model_data_in_array(self.dialog.ui.tableView)

        for idx, data in enumerate(data_list):
            # remove date to identify those not sent in messages
            index = self.dialog.ui.tableView.model().index(idx, DialogConnections.COLUMN_NS_LAST)
            item = self.dialog.ui.tableView.model().itemFromIndex(index)  # type: QStandardItem
            item.setText('-1')

        for message in message_array:
            row_data_index = -1
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
                    break

            self.update_ns_exiting_row(row_data_index, message)

        data_list = self.get_table_model_data_in_array(self.dialog.ui.tableView)

        for idx, data in enumerate(data_list):
            if data[DialogConnections.COLUMN_NS_LAST] == '-1':
                self.dialog.ui.tableView.model().removeRow(idx)

        self.thread_call_ns.gather_data = True  # continue processing

    def update_ns_exiting_row(self, idx, message):
        if idx > -1:  # update
            index = self.dialog.ui.tableView.model().index(idx, DialogConnections.COLUMN_NS_LAST)
            item = self.dialog.ui.tableView.model().itemFromIndex(index)  # type: QStandardItem
            item.setText(message[DialogConnections.COLUMN_NS_LAST])

            index = self.dialog.ui.tableView.model().index(idx, DialogConnections.COLUMN_NS_STATE)
            item = self.dialog.ui.tableView.model().itemFromIndex(index)  # type: QStandardItem
            item.setText(message[DialogConnections.COLUMN_NS_STATE])
            self.color_code(item, message)
        else:  # add new
            item1 = QStandardItem(message[DialogConnections.COLUMN_NS_LAST])  # last
            item1.setTextAlignment(QtCore.Qt.AlignCenter)

            item2 = QStandardItem(message[DialogConnections.COLUMN_NS_PROTO])
            item2.setTextAlignment(QtCore.Qt.AlignCenter)

            item3 = QStandardItem(message[DialogConnections.COLUMN_NS_LOCAL_ADDR])
            item3.setTextAlignment(QtCore.Qt.AlignCenter)

            item4 = QStandardItem(message[DialogConnections.COLUMN_NS_LOCAL_PORT])
            item4.setTextAlignment(QtCore.Qt.AlignCenter)

            item5 = QStandardItem(message[DialogConnections.COLUMN_NS_REMOTE_ADDR])
            item5.setTextAlignment(QtCore.Qt.AlignCenter)

            item6 = QStandardItem(message[DialogConnections.COLUMN_NS_REMOTE_PORT])
            item6.setTextAlignment(QtCore.Qt.AlignCenter)

            item7 = QStandardItem(message[DialogConnections.COLUMN_NS_STATE])
            item7.setTextAlignment(QtCore.Qt.AlignCenter)

            item8 = QStandardItem(message[DialogConnections.COLUMN_NS_PID])
            item8.setTextAlignment(QtCore.Qt.AlignCenter)

            item9 = QStandardItem(message[DialogConnections.COLUMN_NS_APPLICATION])
            item9.setTextAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

            item10 = QStandardItem(message[DialogConnections.COLUMN_NS_SHA1])
            item10.setTextAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

            row = 10 * [None]
            row[DialogConnections.COLUMN_NS_LAST] = item1
            row[DialogConnections.COLUMN_NS_PROTO] = item2
            row[DialogConnections.COLUMN_NS_LOCAL_ADDR] = item3
            row[DialogConnections.COLUMN_NS_LOCAL_PORT] = item4
            row[DialogConnections.COLUMN_NS_REMOTE_ADDR] = item5
            row[DialogConnections.COLUMN_NS_REMOTE_PORT] = item6
            row[DialogConnections.COLUMN_NS_STATE] = item7
            row[DialogConnections.COLUMN_NS_PID] = item8
            row[DialogConnections.COLUMN_NS_APPLICATION] = item9
            row[DialogConnections.COLUMN_NS_SHA1] = item10

            self.color_code(item7, message)

            self.dialog.ui.tableView.model().appendRow(row)

    def color_code(self, item, message):
        if message[DialogConnections.COLUMN_NS_STATE] == 'ESTABLISHED':
            item.setBackground(QtGui.QColor('green'))
        elif message[DialogConnections.COLUMN_NS_STATE] == 'LISTEN':
            item.setBackground(QtGui.QColor('blue'))
        else:
            item.setBackground(QtGui.QColor('white'))

    def stop_thread_ns(self):
        if self.thread_call_ns != NotImplemented and self.thread_call_ns.isRunning():
            self.thread_call_ns.terminate_flag = True
            self.thread_call_ns.wait(2)

    def closeEvent(self, QCloseEvent):
        self.stop_thread_ns()
        super().closeEvent(QCloseEvent)


class DialogConnectionsThread(QThread, Abstr):
    def __init__(self, parent, command='validate'):
        QThread.__init__(self, parent)
        self.command = command
        # this holds string result
        self.result = ''
        # this holds parsed data ready for processing into GUI
        self.data = []
        self.gather_data = False
        self.terminate_flag = False
        self.proc_exe = {}  # list of process id's and its exe
        self.proc_sha1 = {}  # list of process id's and its exe

    def run(self):
        if self.command == 'validate':
            self.validate_command()
        elif self.command == 'execute netstat':
            self.execute_command()

    def validate_command(self):
        process = run_remote_command("which netstat | awk 'END{print NR}'",
                                     self.parent().selected_connection.ip,
                                     self.parent().selected_connection.username,
                                     self.parent().selected_connection.password,
                                     self.parent().selected_connection.use_key_file,
                                     self.parent().selected_connection.sudo_password,
                                     use_sudo=False)

        result = process.stdout.read().decode('utf-8').strip()

        print('netstat ' + result)

        if result == '1':
            self.result = True
        else:
            self.result = False

    def execute_command(self):
        process = run_remote_command("netstat -atupc",
                                     self.parent().selected_connection.ip,
                                     self.parent().selected_connection.username,
                                     self.parent().selected_connection.password,
                                     self.parent().selected_connection.use_key_file,
                                     self.parent().selected_connection.sudo_password,
                                     use_sudo=True)

        process_shell = run_remote_command('/bin/sh',
                                           self.parent().selected_connection.ip,
                                           self.parent().selected_connection.username,
                                           self.parent().selected_connection.password,
                                           self.parent().selected_connection.use_key_file,
                                           self.parent().selected_connection.sudo_password,
                                           use_sudo=False)

        parsed = []
        while not self.terminate_flag:
            output = process.stdout.readline().decode('utf-8')
            if output == '' and process.poll() is not None:
                break
            if output and self.gather_data:
                if output.startswith('Active Internet connections') and parsed:
                    self.emit(SIGNAL('update_netstat'), parsed)
                    parsed = []
                    time.sleep(1.9)
                else:
                    line = self.split_netstat_message(output.strip(), process_shell)
                    if line:
                        parsed.append(line)

        process_shell.kill()
        process.kill()
        print('netstat process completed')

    def split_netstat_message(self, message, process_shell):
        parsed = []
        lines = message.splitlines()

        for line in lines:
            match = re.match(
                r'^(tcp6|udp6|tcp|udp)\s*\d+\s*\d+\s*([\w*-:\[\]]*:[\w*]*)\s*([\w*-:\[\]]*:[\w*]*)\s*([CLTE]\w*|\s)\s*(\d*)/.*$',
                line)
            if match:
                # order
                # protocol, local addr, local port, remote addr, remote port, state, pid, appl, sha1, last
                parsed.append(match.group(1).strip())  # protocol

                match2 = re.match(r'([\w*-:\[\]]*):([\w*]*)', match.group(2).strip())
                parsed.append(match2.group(1))  # ip from address
                parsed.append(match2.group(2))  # ip from port

                match3 = re.match(r'([\w*-:\[\]]*):([\w*]*)', match.group(3).strip())
                parsed.append(match3.group(1))  # ip remote address
                parsed.append(match3.group(2))  # ip remote port

                parsed.append(match.group(4).strip())  # state

                pid_ = match.group(5).strip()
                parsed.append(pid_)  # pid

                if not self.proc_exe.get(pid_) and pid_:
                    print('Adding item ' + pid_)
                    self.proc_exe[pid_] = self.get_application(pid_, process_shell)  # add item
                    self.proc_sha1[pid_] = self.get_sha1(self.proc_exe[pid_], process_shell)  # add item

                parsed.append(self.proc_exe.get(pid_))  # appl
                parsed.append(self.proc_sha1.get(pid_))  # sha1
                parsed.append(datetime.datetime.now().isoformat())  # last

        return parsed

    def get_application(self, pid, process_shell):
        command = 'readlink /proc/{0}/exe'
        return run_remote_command(command.format(pid),
                                  self.parent().selected_connection.ip,
                                  self.parent().selected_connection.username,
                                  self.parent().selected_connection.password,
                                  self.parent().selected_connection.use_key_file,
                                  self.parent().selected_connection.sudo_password,
                                  use_sudo=True,
                                  process_=process_shell).strip()

    def get_sha1(self, application, process_shell):
        command = 'sha1sum -b {0}'
        return run_remote_command(command.format(application),
                                  self.parent().selected_connection.ip,
                                  self.parent().selected_connection.username,
                                  self.parent().selected_connection.password,
                                  self.parent().selected_connection.use_key_file,
                                  self.parent().selected_connection.sudo_password,
                                  use_sudo=True,
                                  process_=process_shell).strip()
