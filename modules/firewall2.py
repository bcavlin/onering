import logging
import re

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt, QThread, SIGNAL
from PyQt4.QtGui import QMainWindow, QStandardItemModel, QStandardItem

from modules.abstr import Abstr
from modules.commons import run_remote_command, is_local_ip
from modules.custom_proxy_filter import CustomSortFilterProxyModel
from modules.windowFirewall_ui import Ui_MainWindow_firewall


class WindowFirewall(QMainWindow, Ui_MainWindow_firewall, Abstr):
    COLUMN_NUMBER = 0
    COLUMN_TO = 1
    COLUMN_ACTION = 2
    COLUMN_FROM = 3

    def __init__(self, parent=None, selected_connection=None):
        QMainWindow.__init__(self, flags=QtCore.Qt.Window)
        self.setupUi(self)
        self.resize(900, self.height())
        self.selected_connection = selected_connection
        self.setup_firewall_table_view(self.tableView_firewall)
        self.firewall_status = False  # disabled
        self.pushButton_refresh.clicked.connect(self.execute_command)
        self.pushButton_enabled.clicked.connect(self.enable_disable_firewall)

    def setup_firewall_table_view(self, table):
        """
        Setup table for firewall
        :param table:
        :return:
        """

        model = QStandardItemModel(self)
        model.setHorizontalHeaderLabels(['#', 'To', 'Action', 'From'])

        proxy = CustomSortFilterProxyModel(self)
        proxy.setSourceModel(model)
        table.setModel(proxy)

        table.setColumnWidth(WindowFirewall.COLUMN_NUMBER, 50)
        table.setColumnWidth(WindowFirewall.COLUMN_FROM, 200)
        table.setColumnWidth(WindowFirewall.COLUMN_ACTION, 100)
        table.setColumnWidth(WindowFirewall.COLUMN_TO, 200)

        header = table.horizontalHeader()
        header.setDefaultAlignment(Qt.AlignHCenter)

    def execute_command(self):
        thread_call = DialogFirewallThread(self, 'execute')
        self.connect(thread_call, SIGNAL("update_ufw"), self.update_ufw)
        thread_call.start()
        self.pushButton_enabled.setEnabled(not self.firewall_status)

    def enable_disable_firewall(self):
        thread_call = DialogFirewallThread(self, 'enable_disable')
        thread_call.start()
        thread_call.wait()
        self.execute_command()  # need to refresh

    def validate_command(self):
        thread_call = DialogFirewallThread(self, 'validate')
        thread_call.start()
        thread_call.wait()

        if thread_call.validation_result:
            enabled = True
        else:
            QtGui.QMessageBox.warning(self.parent(), "UFW not found", "Check if the UFW is installed",
                                      QtGui.QMessageBox.Ok)
            enabled = False

        return enabled

    def update_ufw(self, message_array):
        model = self.tableView_firewall.model().sourceModel()  # type: QStandardItemModel
        model.reset()

        for message in message_array:
            item1 = QStandardItem(message[WindowFirewall.COLUMN_NUMBER])
            item1.setTextAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

            item2 = QStandardItem(message[WindowFirewall.COLUMN_FROM])
            item2.setTextAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

            item3 = QStandardItem(message[WindowFirewall.COLUMN_ACTION])
            item3.setTextAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)

            item4 = QStandardItem(message[WindowFirewall.COLUMN_TO])
            item4.setTextAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

            row = 4 * [None]
            row[WindowFirewall.COLUMN_NUMBER] = item1
            row[WindowFirewall.COLUMN_FROM] = item2
            row[WindowFirewall.COLUMN_ACTION] = item3
            row[WindowFirewall.COLUMN_TO] = item4

            model.appendRow(row)


class DialogFirewallThread(QThread):
    def __init__(self, parent, command='validate'):
        super().__init__(parent)
        self.command = command
        # this holds string result
        self.validation_result = None

    def run(self):
        if self.command == 'validate':
            self.validate_command()
        elif self.command == 'execute':
            self.execute_command()
        elif self.command == 'enable_disable':
            if self.parent().firewall_status:  # enabled
                self.disable_firewall()
            else:
                self.enable_firewall()

    def enable_firewall(self):
        command = "ufw --force enable"
        process = run_remote_command(command,
                                     self.parent().selected_connection.ip,
                                     self.parent().selected_connection.username,
                                     self.parent().selected_connection.password,
                                     self.parent().selected_connection.use_key_file,
                                     self.parent().selected_connection.sudo_password,
                                     use_sudo_=True,
                                     blocking_=True)

        if is_local_ip(self.parent().selected_connection.ip):
            result = process.stdout.read().decode('utf-8').strip()
            process.kill()
        else:
            stdin, stdout, stderr = process.exec_command(command)
            result = stdout.read().decode('utf-8').strip()
            process.close()

        logging.debug(command + ' result: ' + result)

    def disable_firewall(self):
        command = "ufw disable"
        process = run_remote_command(command,
                                     self.parent().selected_connection.ip,
                                     self.parent().selected_connection.username,
                                     self.parent().selected_connection.password,
                                     self.parent().selected_connection.use_key_file,
                                     self.parent().selected_connection.sudo_password,
                                     use_sudo_=True,
                                     blocking_=True)

        if is_local_ip(self.parent().selected_connection.ip):
            result = process.stdout.read().decode('utf-8').strip()
            process.kill()
        else:
            stdin, stdout, stderr = process.exec_command(command)
            result = stdout.read().decode('utf-8').strip()
            process.close()

        logging.debug(command + ' result: ' + result)

    def execute_command(self):
        command = "ufw status numbered"
        process = run_remote_command(command,
                                     self.parent().selected_connection.ip,
                                     self.parent().selected_connection.username,
                                     self.parent().selected_connection.password,
                                     self.parent().selected_connection.use_key_file,
                                     self.parent().selected_connection.sudo_password,
                                     use_sudo_=True,
                                     blocking_=True)

        if is_local_ip(self.parent().selected_connection.ip):
            output = process.stdout.read().decode('utf-8').strip()
            process.kill()
        else:
            stdin, stdout, stderr = process.exec_command(command)
            output = stdout.read().decode('utf-8').strip()
            process.close()

        if output:
            lines = output.split("\n")
            parsed = []
            for line in lines:
                result = self.split_message(line.strip())
                if result:
                    parsed.append(result)
            if parsed:
                self.emit(SIGNAL('update_ufw'), parsed)

    def split_message(self, line):
        parsed = []
        match_status = re.match(r'^Status:\s*(.*)', line)
        if match_status:
            status = match_status.group(1).strip()
            self.parent().firewall_status = True if status == 'active' else False
            logging.debug('Firewall status is: ' + status)
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
        return parsed

    def validate_command(self):
        command = "which ufw | awk 'END{{print NR}}'"
        process = run_remote_command(command,
                                     self.parent().selected_connection.ip,
                                     self.parent().selected_connection.username,
                                     self.parent().selected_connection.password,
                                     self.parent().selected_connection.use_key_file,
                                     self.parent().selected_connection.sudo_password,
                                     use_sudo_=True,
                                     blocking_=True)

        if is_local_ip(self.parent().selected_connection.ip):
            result = process.stdout.read().decode('utf-8').strip()
            process.kill()
        else:
            stdin, stdout, stderr = process.exec_command(command)
            result = stdout.read().decode('utf-8').strip()
            process.close()

        if result == '1':
            logging.debug('Validation successful for ufw')
            self.validation_result = True
        else:
            logging.warning('Validation error for ufw')
            self.validation_result = False
