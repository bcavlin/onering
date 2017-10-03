import base64
import getpass
import logging
import socket
import subprocess
import uuid

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
        self.result = ''
        self.selected_connection = selected_connection
        self.command = ''

    def run(self):
        logging.debug('Validating connection for {0}'.format(self.selected_connection.ip))
        self.command = ["nmap -oG - -sP -PA22 {0} | awk '/Status: Up/{{print $0}}'".format(self.selected_connection.ip)]

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


def run_remote_command(command, ip, username, password, use_key_file, sudo_password, use_sudo=True, process_=None):
    """
    :param command:
    :param ip:
    :param username:
    :param password:
    :param use_key_file:
    :param sudo_password:
    :param use_sudo:
    :param subprocess.Popen process_:
    :return:
    """
    if sudo_password and use_sudo:
        base_command = "echo {0} | sudo -S " + command.strip()
        base_command = base_command.format(sudo_password)
    else:
        base_command = command.strip()

    if ip.strip() == '127.0.0.1':
        command = [base_command]
    else:
        command = use_sshpass(use_key_file, password) + ["ssh", "{0}@{1}".format(username, ip),
                                                         base_command]

    if process_:
        command.append('\n')
        process_.stdin.write(' '.join(command).encode())
        process_.stdin.flush()
        # line = process_.communicate(' '.join(command).encode())[0]
        # process_.wait()
        line = process_.stdout.readline()
        return line
    else:
        return subprocess.Popen(command, shell=False if len(command) > 1 else True, stdout=subprocess.PIPE,
                                stderr=subprocess.DEVNULL, stdin=subprocess.PIPE, bufsize=1)


