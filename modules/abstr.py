import abc


class Abstr(object):
    __metaclass__ = abc.ABCMeta

    enabled = False

    @abc.abstractmethod
    def validate_command(self):
        """validate command to see if we have privileges and if the command exists"""

    @abc.abstractmethod
    def execute_command(self):
        """execute command"""

