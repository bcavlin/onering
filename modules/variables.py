import base64
import getpass
import socket
import uuid

from Crypto.Cipher import AES

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
