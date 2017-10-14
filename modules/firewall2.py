import logging
import re

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt, QThread, SIGNAL
from PyQt4.QtGui import QMainWindow, QStandardItemModel, QStandardItem

from modules import commons
from modules.abstr import Abstr
from modules.commons import run_remote_command, is_local_ip, get_full_command
from modules.custom_proxy_filter import CustomSortFilterProxyModel
from modules.windowFirewall_ui import Ui_MainWindow_firewall, _translate


class WindowFirewall(QMainWindow, Ui_MainWindow_firewall, Abstr):
    NUMBER_OF_COLUMNS = 10
    COLUMN_TO_IP = 0
    COLUMN_TO_PORT = 1
    COLUMN_TO_V6 = 2
    COLUMN_TO_INTERFACE = 3
    COLUMN_TO_PROTOCOL = 4
    COLUMN_ACTION = 5
    # COLUMN_FROM = 6
    COLUMN_FROM_IP = 6
    COLUMN_FROM_PORT = 7
    COLUMN_FROM_V6 = 8
    COLUMN_FROM_PROTOCOL = 9

    def __init__(self, parent=None, selected_connection=None):
        QMainWindow.__init__(self, flags=QtCore.Qt.Window)
        self.setupUi(self)
        self.resize(900, self.height())
        self.selected_connection = selected_connection
        self.setup_firewall_table_view()
        self.firewall_active = None  # disabled
        self.pushButton_refresh.clicked.connect(self.execute_command)
        self.pushButton_enabled.clicked.connect(self.enable_disable_firewall)

    def setup_firewall_table_view(self):
        table = self.tableView_firewall
        model = QStandardItemModel(self)
        model.setHorizontalHeaderLabels(
            ['To:ip', ' To:port', 'To:ver', 'On iface', 'To:proto', 'Action', 'From:ip', 'From:port', 'From:ver',
             'From:proto'])

        proxy = CustomSortFilterProxyModel(self)
        proxy.setSourceModel(model)
        table.setModel(proxy)

        table.setColumnWidth(WindowFirewall.COLUMN_TO_IP, 200)
        table.setColumnWidth(WindowFirewall.COLUMN_TO_PORT, 150)
        table.setColumnWidth(WindowFirewall.COLUMN_TO_V6, 70)
        table.setColumnWidth(WindowFirewall.COLUMN_TO_INTERFACE, 100)
        table.setColumnWidth(WindowFirewall.COLUMN_TO_PROTOCOL, 70)
        table.setColumnWidth(WindowFirewall.COLUMN_ACTION, 100)
        table.setColumnWidth(WindowFirewall.COLUMN_FROM_IP, 200)
        table.setColumnWidth(WindowFirewall.COLUMN_FROM_PORT, 150)
        table.setColumnWidth(WindowFirewall.COLUMN_FROM_V6, 70)
        table.setColumnWidth(WindowFirewall.COLUMN_FROM_PROTOCOL, 70)

        header = table.horizontalHeader()
        header.setDefaultAlignment(Qt.AlignHCenter)

    def execute_command(self):
        self.tableView_firewall.model().reset()
        thread_call = DialogFirewallThread(self, 'execute')
        self.connect(thread_call, SIGNAL("update_ufw"), self.update_ufw)
        self.connect(thread_call, SIGNAL("update_status"), self.update_status)
        thread_call.start()
        thread_call.wait()
        self.pushButton_enabled.setEnabled(self.firewall_active is not None)
        self.update_enabled_button()

    def update_enabled_button(self):
        if self.firewall_active:
            self.pushButton_enabled.setText('Disable')
        else:
            self.pushButton_enabled.setText('Enable')

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

    def update_status(self, message):
        status_ = message.get('status')
        logging_ = message.get('logging')
        default_ = message.get('default')
        if status_:
            self.label_status.setText(_translate("MainWindow_firewall", "<html><head/><body><p>Status: "
                                                                        "<span style=\" font-weight:600; color:#00007f;\">{0}</span></p></body></html>"
                                                 .format(status_), None))
            self.firewall_active = True if status_ == 'active' else False
            self.update_enabled_button()
        elif logging_:
            self.label_logging.setText(_translate("MainWindow_firewall", "<html><head/><body><p>Logging level: "
                                                                         "<span style=\" font-weight:600; color:#00007f;\">{0}</span></p></body></html>"
                                                  .format(logging_), None))
        elif default_:
            self.label_default.setText(_translate("MainWindow_firewall", "<html><head/><body><p>Default: "
                                                                         "<span style=\" font-weight:600; color:#00007f;\">{0}</span></p></body></html>"
                                                  .format(default_), None))

    def update_ufw(self, message_array):
        model = self.tableView_firewall.model().sourceModel()  # type: QStandardItemModel
        row = WindowFirewall.NUMBER_OF_COLUMNS * [None]

        for message in message_array:
            for idx, m in enumerate(message):
                item = QStandardItem(m)
                if idx in (
                        WindowFirewall.COLUMN_TO_PROTOCOL, WindowFirewall.COLUMN_TO_V6,
                        WindowFirewall.COLUMN_TO_INTERFACE, WindowFirewall.COLUMN_ACTION,
                        WindowFirewall.COLUMN_FROM_PROTOCOL, WindowFirewall.COLUMN_FROM_V6,
                        WindowFirewall.COLUMN_TO_PORT, WindowFirewall.COLUMN_FROM_PORT):
                    item.setTextAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
                else:
                    item.setTextAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
                row[idx] = item
            model.appendRow(row)


class DialogFirewallThread(QThread):
    def __init__(self, parent, command='validate'):
        super().__init__(parent)
        self.command = command
        self.validation_result = None

    def run(self):
        if self.command == 'validate':
            self.validate_command()
        elif self.command == 'execute':
            self.execute_command()
        elif self.command == 'enable_disable':
            if self.parent().firewall_active:  # enabled
                self.disable_firewall()
            else:
                self.enable_firewall()

    def enable_firewall(self):
        command = get_full_command("ufw --force enable", self.parent().selected_connection.sudo_password)
        process = run_remote_command(command,
                                     self.parent().selected_connection.ip,
                                     self.parent().selected_connection.username,
                                     self.parent().selected_connection.password,
                                     self.parent().selected_connection.use_key_file,
                                     blocking_=True)

        if is_local_ip(self.parent().selected_connection.ip):
            result = process.stdout.read().decode('utf-8').strip()
            process.kill()
        else:
            stdin, stdout, stderr = process.exec_command(command[0])
            result = stdout.read().decode('utf-8').strip()
            process.close()
        logging.debug(command + ' result: ' + result)

    def disable_firewall(self):
        command = get_full_command("ufw disable", self.parent().selected_connection.sudo_password)
        process = run_remote_command(command,
                                     self.parent().selected_connection.ip,
                                     self.parent().selected_connection.username,
                                     self.parent().selected_connection.password,
                                     self.parent().selected_connection.use_key_file,
                                     blocking_=True)

        if is_local_ip(self.parent().selected_connection.ip):
            result = process.stdout.read().decode('utf-8').strip()
            process.kill()
        else:
            stdin, stdout, stderr = process.exec_command(command[0])
            result = stdout.read().decode('utf-8').strip()
            process.close()
        logging.debug(command + ' result: ' + result)

    def execute_command(self):
        command = get_full_command("ufw status verbose", self.parent().selected_connection.sudo_password)
        process = run_remote_command(command,
                                     self.parent().selected_connection.ip,
                                     self.parent().selected_connection.username,
                                     self.parent().selected_connection.password,
                                     self.parent().selected_connection.use_key_file,
                                     blocking_=True)

        if is_local_ip(self.parent().selected_connection.ip):
            output = process.stdout.read().decode('utf-8').strip()
            process.kill()
        else:
            stdin, stdout, stderr = process.exec_command(command[0])
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
        match_status = commons.REGEX_UFW_STATUS.search(line)
        match_logging = commons.REGEX_UFW_LOGGING.search(line)
        match_default = commons.REGEX_UFW_DEFAULT.search(line)
        if match_status:
            status = match_status.group(1).strip()
            logging.debug('Firewall status is: ' + status)
            self.emit(SIGNAL('update_status'), {'status': status})
        elif match_logging:
            status = match_logging.group(1).strip()
            logging.debug('Firewall logging is: ' + status)
            self.emit(SIGNAL('update_status'), {'logging': status})
        elif match_default:
            status = match_default.group(1).strip()
            logging.debug('Firewall default is: ' + status)
            self.emit(SIGNAL('update_status'), {'default': status})
        else:
            logging.debug('Line is: ' + line)
            match = commons.REGEX_UFW_WHOLE_LINE.search(line)
            logging.debug('match is: ' + str(match))
            if match:
                parsed = WindowFirewall.NUMBER_OF_COLUMNS * [None]
                if match.group('to'):  # this refers to whole to group - it needs to be split
                    to = match.group('to').strip()
                    self.split_to_from(parsed, to, 'to')

                if match.group('action'):
                    parsed[WindowFirewall.COLUMN_ACTION] = match.group('action').strip()

                if match.group('from'):
                    from_ = match.group('from').strip()
                    self.split_to_from(parsed, from_, 'from')

        return parsed

    def split_to_from(self, parsed, line, indicator):
        split = re.split(commons.REGEX_UFW_SPLIT, line)
        if split:
            for s in split:
                search, group_ = commons.REGEX_UFW_ANYWHERE.search(s), 'any'
                if search and search.group(group_):
                    logging.debug('found ' + group_ + ' ' + search.group(group_))
                    parsed[
                        WindowFirewall.COLUMN_TO_IP if indicator == 'to' else WindowFirewall.COLUMN_FROM_IP] = search.group(
                        group_).strip()
                    continue
                search, group_ = commons.REGEX_UFW_IP4.search(s), 'ip4'
                if search and search.group(group_):
                    logging.debug('found ' + group_ + ' ' + search.group(group_))
                    parsed[
                        WindowFirewall.COLUMN_TO_IP if indicator == 'to' else WindowFirewall.COLUMN_FROM_IP] = search.group(
                        group_).strip()
                    continue
                search, group_ = commons.REGEX_UFW_IP6.search(s), 'ip6'
                if search and search.group(group_):
                    logging.debug('found ' + group_ + ' ' + search.group(group_))
                    parsed[
                        WindowFirewall.COLUMN_TO_IP if indicator == 'to' else WindowFirewall.COLUMN_FROM_IP] = search.group(
                        group_).strip()
                    continue
                search, group_ = commons.REGEX_UFW_INTERFACE.search(s), 'interface'
                if search and search.group(group_):
                    logging.debug('found ' + group_ + ' ' + search.group(group_))
                    parsed[WindowFirewall.COLUMN_TO_INTERFACE] = search.group(group_).strip()
                    continue
                search, group_, group2_ = commons.REGEX_UFW_PORT_LIST.search(s), 'port_list', 'proto'
                if search and search.group(group_) and search.group(group2_):
                    logging.debug('found ' + group_ + ' ' + search.group(group_))
                    logging.debug('found ' + group2_ + ' ' + search.group(group2_))
                    parsed[WindowFirewall.COLUMN_TO_PORT if indicator == 'to' else WindowFirewall.COLUMN_FROM_PORT] = search.group(group_).strip()
                    parsed[WindowFirewall.COLUMN_TO_PROTOCOL if indicator == 'to' else WindowFirewall.COLUMN_FROM_PROTOCOL] = search.group(group2_).strip()
                    continue
                search, group_, group2_ = commons.REGEX_UFW_PORT_RANGE.search(s), 'port_range', 'proto'
                if search and search.group(group_) and search.group(group2_):
                    logging.debug('found ' + group_ + ' ' + search.group(group_))
                    logging.debug('found ' + group2_ + ' ' + search.group(group2_))
                    parsed[WindowFirewall.COLUMN_TO_PORT if indicator == 'to' else WindowFirewall.COLUMN_FROM_PORT] = search.group(group_).strip()
                    parsed[WindowFirewall.COLUMN_TO_PROTOCOL if indicator == 'to' else WindowFirewall.COLUMN_FROM_PROTOCOL] = search.group(group2_).strip()
                    continue
                search, group_ = commons.REGEX_UFW_V6.search(s), 'v6'
                if search and search.group(group_):
                    logging.debug('found ' + group_ + ' ' + search.group(group_))
                    parsed[WindowFirewall.COLUMN_TO_V6 if indicator == 'to' else WindowFirewall.COLUMN_FROM_V6] = search.group(group_).strip()
                    continue
                search, group_ = commons.REGEX_UFW_PORT.search(s), 'port'
                if search and search.group(group_):
                    logging.debug('found ' + group_ + ' ' + search.group(group_))
                    parsed[WindowFirewall.COLUMN_TO_PORT if indicator == 'to' else WindowFirewall.COLUMN_FROM_PORT] = search.group(group_).strip()
                    continue
        if not parsed[WindowFirewall.COLUMN_TO_PROTOCOL if indicator == 'to' else WindowFirewall.COLUMN_FROM_PROTOCOL]:
            parsed[WindowFirewall.COLUMN_TO_PROTOCOL if indicator == 'to' else WindowFirewall.COLUMN_FROM_PROTOCOL] = 'both'
        if not parsed[WindowFirewall.COLUMN_TO_V6 if indicator == 'to' else WindowFirewall.COLUMN_FROM_V6]:
            parsed[WindowFirewall.COLUMN_TO_V6 if indicator == 'to' else WindowFirewall.COLUMN_FROM_V6] = '(v4)'
        if not parsed[WindowFirewall.COLUMN_TO_IP if indicator == 'to' else WindowFirewall.COLUMN_FROM_IP]:
            parsed[WindowFirewall.COLUMN_TO_IP if indicator == 'to' else WindowFirewall.COLUMN_FROM_IP] = 'Anywhere'
        if not parsed[WindowFirewall.COLUMN_TO_INTERFACE]:
            parsed[WindowFirewall.COLUMN_TO_INTERFACE] = 'All'

    def validate_command(self):
        command = get_full_command("which ufw | awk 'END{{print NR}}'", self.parent().selected_connection.sudo_password,
                                   use_sudo_=False)
        process = run_remote_command(command,
                                     self.parent().selected_connection.ip,
                                     self.parent().selected_connection.username,
                                     self.parent().selected_connection.password,
                                     self.parent().selected_connection.use_key_file,
                                     blocking_=True)

        if is_local_ip(self.parent().selected_connection.ip):
            result = process.stdout.read().decode('utf-8').strip()
            process.kill()
        else:
            stdin, stdout, stderr = process.exec_command(command[0])
            result = stdout.read().decode('utf-8').strip()
            process.close()

        if result == '1':
            logging.debug('Validation successful for ufw')
            self.validation_result = True
        else:
            logging.warning('Validation error for ufw')
            self.validation_result = False
