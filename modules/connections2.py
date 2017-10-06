import datetime
import logging
import re
import time

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt, QThread, SIGNAL, pyqtSlot
from PyQt4.QtGui import QMainWindow, QStandardItemModel, QStandardItem

from modules.abstr import Abstr
from modules.commons import run_remote_command, is_local_ip
from modules.custom_proxy_filter import CustomSortFilterProxyModel
from modules.windowConnections_ui import Ui_MainWindow_connections


class WindowConnections(QMainWindow, Ui_MainWindow_connections, Abstr):
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

    def __init__(self, parent=None, selected_connection=None):
        QMainWindow.__init__(self, flags=QtCore.Qt.Window)
        self.setupUi(self)
        self.selected_connection = selected_connection
        self.resize(1200, self.height())
        self.setup_ns_table_view(self.tableView_netstat)
        self.thread_call_validate = NotImplemented
        self.thread_call_ns = NotImplemented
        self.pushButton_start_netstat.setStyleSheet("background-color: green; color: white")
        self.pushButton_start_netstat.setText('Start')
        self.pushButton_start_netstat.clicked.connect(self.execute_command)
        self.pushButton_clear.clicked.connect(self.clear_filter)
        self.filterLineEdit.textChanged.connect(self.update_filter)

    def setup_ns_table_view(self, table):
        """
        :param QtGui.QTableView table:
        :return:
        """
        model = QStandardItemModel(self)
        model.setHorizontalHeaderLabels(
            ['Prt', 'Local Addr', 'L. Port', 'Remote Addr', 'R. Port', 'State', 'PID', 'Application', 'SHA1',
             'Last'])

        model.setHeaderData(WindowConnections.COLUMN_NS_APPLICATION, Qt.Horizontal, Qt.AlignLeft, Qt.TextAlignmentRole)
        model.setHeaderData(WindowConnections.COLUMN_NS_SHA1, Qt.Horizontal, Qt.AlignLeft, Qt.TextAlignmentRole)

        proxy = CustomSortFilterProxyModel(self)
        proxy.setSourceModel(model)
        table.setModel(proxy)

        table.setColumnWidth(WindowConnections.COLUMN_NS_PID, 100)
        table.setColumnWidth(WindowConnections.COLUMN_NS_STATE, 130)
        table.setColumnWidth(WindowConnections.COLUMN_NS_REMOTE_PORT, 70)
        table.setColumnWidth(WindowConnections.COLUMN_NS_REMOTE_ADDR, 150)
        table.setColumnWidth(WindowConnections.COLUMN_NS_LOCAL_PORT, 70)
        table.setColumnWidth(WindowConnections.COLUMN_NS_LOCAL_ADDR, 150)
        table.setColumnWidth(WindowConnections.COLUMN_NS_PROTO, 50)
        table.setColumnWidth(WindowConnections.COLUMN_NS_LAST, 100)
        table.setColumnWidth(WindowConnections.COLUMN_NS_APPLICATION, 400)
        table.setColumnWidth(WindowConnections.COLUMN_NS_SHA1, 400)

        header = table.horizontalHeader()
        header.setDefaultAlignment(Qt.AlignHCenter)

    def clear_filter(self):
        self.filterLineEdit.setText('')

    @pyqtSlot(str)
    def update_filter(self, text):
        proxy = self.tableView_netstat.model()  # type: CustomSortFilterProxyModel
        proxy.setFilterString(text)

    def stop_thread_ns(self):
        if self.thread_call_ns != NotImplemented and self.thread_call_ns.isRunning():
            self.pushButton_start_netstat.setText('Start')
            self.pushButton_start_netstat.setStyleSheet("background-color: green; color: white")
            self.filterLineEdit.setText('')
            self.checkBox_numeric.setEnabled(True)
            self.thread_call_ns.terminate_flag = True
            self.thread_call_ns.wait(2)

    def closeEvent(self, QCloseEvent):
        self.stop_thread_ns()
        super().closeEvent(QCloseEvent)

    def execute_command(self):
        if self.pushButton_start_netstat.text() == 'Start':
            self.pushButton_start_netstat.setText('Stop')
            self.pushButton_start_netstat.setStyleSheet("background-color: red; color: white")
            self.checkBox_numeric.setEnabled(False)
            self.tableView_netstat.model().reset()
            self.thread_call_ns = DialogConnectionsThread(self, 'execute netstat')
            self.connect(self.thread_call_ns, SIGNAL("update_netstat"), self.update_netstat)
            self.thread_call_ns.gather_data = True
            self.thread_call_ns.start()
        else:
            self.thread_call_ns.gather_data = False
            self.stop_thread_ns()

    def validate_command(self):
        self.thread_call_validate = DialogConnectionsThread(self, 'validate')
        self.thread_call_validate.start()
        self.thread_call_validate.wait()
        return True if self.thread_call_validate.validation_result else False

    def get_table_model_data_in_array(self, table):
        """
        :param QtGui.QTableView table:
        :return:
        """
        model = table.model().sourceModel()
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

        data_list = self.get_table_model_data_in_array(self.tableView_netstat)

        for idx, data in enumerate(data_list):
            # remove date to identify those not sent in messages
            model = self.tableView_netstat.model().sourceModel()
            index = model.index(idx, WindowConnections.COLUMN_NS_LAST)
            item = model.itemFromIndex(index)  # type: QStandardItem
            item.setText('-1')

        for message in message_array:
            row_data_index = -1
            for idx, data in enumerate(data_list):
                if data[WindowConnections.COLUMN_NS_PROTO] == message[WindowConnections.COLUMN_NS_PROTO] \
                        and data[WindowConnections.COLUMN_NS_PROTO] == message[WindowConnections.COLUMN_NS_PROTO] \
                        and data[WindowConnections.COLUMN_NS_LOCAL_ADDR] == message[
                            WindowConnections.COLUMN_NS_LOCAL_ADDR] \
                        and data[WindowConnections.COLUMN_NS_LOCAL_PORT] == message[
                            WindowConnections.COLUMN_NS_LOCAL_PORT] \
                        and data[WindowConnections.COLUMN_NS_REMOTE_ADDR] == message[
                            WindowConnections.COLUMN_NS_REMOTE_ADDR] \
                        and data[WindowConnections.COLUMN_NS_REMOTE_PORT] == message[
                            WindowConnections.COLUMN_NS_REMOTE_PORT] \
                        and data[WindowConnections.COLUMN_NS_PID] == message[WindowConnections.COLUMN_NS_PID]:
                    row_data_index = idx
                    break

            self.update_ns_exiting_row(row_data_index, message)

        data_list = self.get_table_model_data_in_array(self.tableView_netstat)

        for idx, data in enumerate(data_list):
            if data[WindowConnections.COLUMN_NS_LAST] == '-1':
                self.tableView_netstat.model().sourceModel().removeRow(idx)

        self.thread_call_ns.gather_data = True  # continue processing

    def update_ns_exiting_row(self, idx, message):
        if idx > -1:  # update
            model = self.tableView_netstat.model().sourceModel()
            index = model.index(idx, WindowConnections.COLUMN_NS_LAST)
            item = model.itemFromIndex(index)  # type: QStandardItem
            item.setText(message[WindowConnections.COLUMN_NS_LAST])

            index = model.index(idx, WindowConnections.COLUMN_NS_STATE)
            item = model.itemFromIndex(index)  # type: QStandardItem
            item.setText(message[WindowConnections.COLUMN_NS_STATE])
            self.color_code(item, message)
        else:  # add new
            item1 = QStandardItem(message[WindowConnections.COLUMN_NS_LAST])  # last
            item1.setTextAlignment(QtCore.Qt.AlignCenter)

            item2 = QStandardItem(message[WindowConnections.COLUMN_NS_PROTO])
            item2.setTextAlignment(QtCore.Qt.AlignCenter)

            item3 = QStandardItem(message[WindowConnections.COLUMN_NS_LOCAL_ADDR])
            item3.setTextAlignment(QtCore.Qt.AlignCenter)

            item4 = QStandardItem(message[WindowConnections.COLUMN_NS_LOCAL_PORT])
            item4.setTextAlignment(QtCore.Qt.AlignCenter)

            item5 = QStandardItem(message[WindowConnections.COLUMN_NS_REMOTE_ADDR])
            item5.setTextAlignment(QtCore.Qt.AlignCenter)

            item6 = QStandardItem(message[WindowConnections.COLUMN_NS_REMOTE_PORT])
            item6.setTextAlignment(QtCore.Qt.AlignCenter)

            item7 = QStandardItem(message[WindowConnections.COLUMN_NS_STATE])
            item7.setTextAlignment(QtCore.Qt.AlignCenter)

            item8 = QStandardItem(message[WindowConnections.COLUMN_NS_PID])
            item8.setTextAlignment(QtCore.Qt.AlignCenter)

            item9 = QStandardItem(message[WindowConnections.COLUMN_NS_APPLICATION])
            item9.setTextAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

            item10 = QStandardItem(message[WindowConnections.COLUMN_NS_SHA1])
            item10.setTextAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

            row = 10 * [None]
            row[WindowConnections.COLUMN_NS_LAST] = item1
            row[WindowConnections.COLUMN_NS_PROTO] = item2
            row[WindowConnections.COLUMN_NS_LOCAL_ADDR] = item3
            row[WindowConnections.COLUMN_NS_LOCAL_PORT] = item4
            row[WindowConnections.COLUMN_NS_REMOTE_ADDR] = item5
            row[WindowConnections.COLUMN_NS_REMOTE_PORT] = item6
            row[WindowConnections.COLUMN_NS_STATE] = item7
            row[WindowConnections.COLUMN_NS_PID] = item8
            row[WindowConnections.COLUMN_NS_APPLICATION] = item9
            row[WindowConnections.COLUMN_NS_SHA1] = item10

            self.color_code(item7, message)

            self.tableView_netstat.model().sourceModel().appendRow(row)

    def color_code(self, item, message):
        if message[WindowConnections.COLUMN_NS_STATE] == 'ESTABLISHED':
            item.setBackground(QtGui.QColor('green'))
            item.setForeground(QtGui.QColor('white'))
        elif message[WindowConnections.COLUMN_NS_STATE] == 'LISTEN':
            item.setBackground(QtGui.QColor('blue'))
            item.setForeground(QtGui.QColor('white'))
        elif message[WindowConnections.COLUMN_NS_STATE] == 'TIME_WAIT':
            item.setBackground(QtGui.QColor('orange'))
            item.setForeground(QtGui.QColor('white'))
        else:
            item.setBackground(QtGui.QColor('white'))


class DialogConnectionsThread(QThread):
    def __init__(self, parent, command='validate'):
        QThread.__init__(self, parent)
        self.command = command
        self.validation_result = None
        self.gather_data = True
        self.terminate_flag = False
        self.proc_exe = {}  # list of process id's and its exe
        self.proc_sha1 = {}  # list of process id's and its sha1

    def run(self):
        if self.command == 'validate':
            self.validate_command()
        elif self.command == 'execute netstat':
            self.execute_command()

    def validate_command(self):
        process = run_remote_command("which netstat readlink sha1sum | awk 'END{print NR}'",
                                     self.parent().selected_connection.ip,
                                     self.parent().selected_connection.username,
                                     self.parent().selected_connection.password,
                                     self.parent().selected_connection.use_key_file,
                                     self.parent().selected_connection.sudo_password,
                                     use_sudo_=False,
                                     blocking_=True)

        if is_local_ip(self.parent().selected_connection.ip):
            result = process.stdout.read().decode('utf-8').strip()
            process.kill()
        else:
            stdin, stdout, stderr = process.exec_command("which netstat readlink sha1sum | awk 'END{print NR}'")
            result = stdout.read().decode('utf-8').strip()
            process.close()

        if result == '3':
            logging.debug('Validation successful for netstat readlink sha1sum')
            self.validation_result = True
        else:
            logging.warning('Validation error for netstat readlink sha1sum')
            self.validation_result = False

    def execute_command(self):
        if self.parent().checkBox_numeric.isChecked():
            command = 'netstat -antup'
        else:
            command = 'netstat -atup'

        process_netstat = run_remote_command('/bin/sh',
                                             self.parent().selected_connection.ip,
                                             self.parent().selected_connection.username,
                                             self.parent().selected_connection.password,
                                             self.parent().selected_connection.use_key_file,
                                             self.parent().selected_connection.sudo_password,
                                             use_sudo_=False)

        process_shell = run_remote_command('/bin/sh',
                                           self.parent().selected_connection.ip,
                                           self.parent().selected_connection.username,
                                           self.parent().selected_connection.password,
                                           self.parent().selected_connection.use_key_file,
                                           self.parent().selected_connection.sudo_password,
                                           use_sudo_=False)

        while not self.terminate_flag:
            output = run_remote_command(command,
                                        self.parent().selected_connection.ip,
                                        self.parent().selected_connection.username,
                                        self.parent().selected_connection.password,
                                        self.parent().selected_connection.use_key_file,
                                        self.parent().selected_connection.sudo_password,
                                        use_sudo_=True,
                                        process_=process_netstat)

            if output:
                lines = output.split("\n")
                parsed = []
                for line in lines:
                    result = self.split_netstat_message(line.strip(), process_shell)
                    if result:
                        parsed.append(result)
                if parsed:
                    self.emit(SIGNAL('update_netstat'), parsed)

            time.sleep(1.9)

        if is_local_ip(self.parent().selected_connection.ip):
            process_shell.kill()
            process_netstat.kill()
        else:
            process_shell.close()
            process_netstat.close()
        print('netstat process_netstat completed')

    def split_netstat_message(self, line, process_shell):
        parsed = []
        match = re.match(
            r'^(tcp6|udp6|tcp|udp)\s*\d+\s*\d+\s*([\w*-:\[\]]*:[\w*]*)\s*([\w*-:\[\]]*:[\w*]*)\s*([CLTEF]\w*|\s)\s*([-|\d/]*).*$',
            line.strip())
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

            pid_ = re.sub('/', '', match.group(5).strip())
            parsed.append(pid_)  # pid

            if '-' != pid_ and not self.proc_exe.get(pid_) and pid_:
                logging.debug('Adding PID to the list: ' + pid_)
                self.proc_exe[pid_] = self.get_application(pid_, process_shell)  # add item
                if self.proc_exe[pid_]:
                    self.proc_sha1[pid_] = self.get_sha1(self.proc_exe[pid_], process_shell)  # add item

            parsed.append(self.proc_exe.get(pid_))  # appl
            parsed.append(self.proc_sha1.get(pid_))  # sha1
            parsed.append(datetime.datetime.now().strftime('%H:%M:%S'))  # last
        return parsed

    def get_application(self, pid, process_shell):
        command = "readlink /proc/{0}/exe | awk '{{ print }} END {{ if (!NR) print \"n/a or sudo required\" }}'"
        line = run_remote_command(command.format(pid),
                                  self.parent().selected_connection.ip,
                                  self.parent().selected_connection.username,
                                  self.parent().selected_connection.password,
                                  self.parent().selected_connection.use_key_file,
                                  self.parent().selected_connection.sudo_password,
                                  use_sudo_=True,
                                  process_=process_shell,
                                  blocking_=True)
        if line:
            return line.strip()
        else:
            return None

    def get_sha1(self, application, process_shell):
        command = 'sha1sum -b {0}'
        line = run_remote_command(command.format(application),
                                  self.parent().selected_connection.ip,
                                  self.parent().selected_connection.username,
                                  self.parent().selected_connection.password,
                                  self.parent().selected_connection.use_key_file,
                                  self.parent().selected_connection.sudo_password,
                                  use_sudo_=True,
                                  process_=process_shell,
                                  blocking_=True)
        if line:
            return line.strip()
        else:
            return None
