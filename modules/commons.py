import base64
import fcntl
import getpass
import logging
import os
import socket
import subprocess
import uuid

import paramiko as paramiko
from Crypto.Cipher import AES
from PyQt4.QtCore import QThread

cipher = AES.new(uuid.uuid4().hex, AES.MODE_ECB)


def encode(msg_text):
    return base64.b64encode(cipher.encrypt(msg_text))


def decode(msg_text):
    return cipher.decrypt(base64.b64decode(msg_text)).strip().decode("utf-8")


def auto_str(cls):
    def __str__(self):
        return '%s(%s)' % (
            type(self).__name__,
            ', '.join('%s=%s' % item for item in vars(self).items())
        )

    cls.__str__ = __str__
    return cls


def use_sshpass(key_parameter, password):
    if not key_parameter:
        return ["sshpass", "-p", "{0}".format(password)]
    else:
        return []


def validate_ip_address(ip):
    try:
        socket.inet_aton(ip)
        return True
    except:
        return False


# usage @static_vars(counter=0)
def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func

    return decorate


class ValidateConnectionThread(QThread):
    """
    This class is used to validate connection to the machine that is selected for the operation
    """

    def __init__(self, parent, selected_connection):
        super().__init__(parent)
        self.result = None
        self.selected_connection = selected_connection
        self.command = ''

    def run(self):
        if self.selected_connection.ip in ('127.0.0.1', '::1'):
            self.result = True
        else:
            logging.debug('Validating connection for {0}'.format(self.selected_connection.ip))
            self.command = [
                "nmap -oG - -sP -PA22 {0} | awk '/Status: Up/{{print $0}}'".format(self.selected_connection.ip)]
            self.result = subprocess.Popen(
                self.command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL).stdout.read().decode('utf-8').strip()


@auto_str
class Connection:
    def __init__(self):
        super(self.__class__, self).__init__()
        self.ip = '127.0.0.1'
        self.username = getpass.getuser()
        self.password = ''
        self.sudo_password = ''
        self.store_password = False
        self.use_key_file = False

    def get_title(self):
        return self.username + '@' + self.ip


def is_local_ip(ip):
    return True if ip in ('127.0.0.1', '::1') else False


def run_remote_command(command, ip, username, password, use_key_file, sudo_password, use_sudo_=True, process_=None,
                       blocking_=False, expect_results_=1):
    """
    :param expect_results_:
    :param use_sudo_:
    :param blocking_:   This parameter is used to differentiate between continuous output in loop, where we need non blocking read
                        and a read where we expect immediate and full response (full response needs something written or it will block)
    :param command:
    :param ip:
    :param username:
    :param password:
    :param use_key_file:
    :param sudo_password:
    :param process_:
    :return:
    """
    if sudo_password and use_sudo_:
        base_command = "echo {0} | sudo -S ".format(sudo_password)
        base_command = base_command + command.strip()
    else:
        base_command = command.strip()

    command = [base_command]

    if process_:
        output = ''
        if is_local_ip(ip):
            command.append('\n')
            process_.stdin.write(' '.join(command).encode())
            process_.stdin.flush()
            if blocking_:
                i = 0
                while i < expect_results_:  # need to write command to always return expected results
                    o = process_.stdout.readline()
                    if o:
                        output += o.decode('utf-8')
                    i += 1
            else:
                o = process_.stdout.read()
                if o:
                    output = o.decode('utf-8')

        else:
            stdin, stdout, stderr = process_.exec_command(' '.join(command).encode())
            o = stdout.read()
            if o:
                output = o.decode('utf-8')

        parsed = list((x.strip() for x in output.split('\n')))
        return parsed
    else:
        if is_local_ip(ip):
            proc = subprocess.Popen(command, shell=False if len(command) > 1 else True, stdout=subprocess.PIPE,
                                    stderr=subprocess.DEVNULL, stdin=subprocess.PIPE, bufsize=1)
            if not blocking_:
                fd = proc.stdout.fileno()
                fl = fcntl.fcntl(fd, fcntl.F_GETFL)
                fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
            return proc
        else:
            client = paramiko.SSHClient()
            client.load_system_host_keys()
            client.set_missing_host_key_policy(paramiko.WarningPolicy)
            client.connect(ip, port=22, username=username, password=password)
            return client
