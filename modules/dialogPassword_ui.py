# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './modules/dialogPassword.ui'
#
# Created by: PyQt4 UI code generator 4.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_DialogPassword(object):
    def setupUi(self, DialogPassword):
        DialogPassword.setObjectName(_fromUtf8("DialogPassword"))
        DialogPassword.setWindowModality(QtCore.Qt.WindowModal)
        DialogPassword.resize(526, 305)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Ubuntu Mono"))
        DialogPassword.setFont(font)
        self.verticalLayout_2 = QtGui.QVBoxLayout(DialogPassword)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.previousConnectionsLabel = QtGui.QLabel(DialogPassword)
        self.previousConnectionsLabel.setObjectName(_fromUtf8("previousConnectionsLabel"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.previousConnectionsLabel)
        self.previousConnectionsComboBox = QtGui.QComboBox(DialogPassword)
        self.previousConnectionsComboBox.setObjectName(_fromUtf8("previousConnectionsComboBox"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.previousConnectionsComboBox)
        self.rememberPasswordsLabel = QtGui.QLabel(DialogPassword)
        self.rememberPasswordsLabel.setObjectName(_fromUtf8("rememberPasswordsLabel"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.rememberPasswordsLabel)
        self.rememberPasswordsCheckBox = QtGui.QCheckBox(DialogPassword)
        self.rememberPasswordsCheckBox.setObjectName(_fromUtf8("rememberPasswordsCheckBox"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.rememberPasswordsCheckBox)
        self.iPAddressLabel = QtGui.QLabel(DialogPassword)
        self.iPAddressLabel.setObjectName(_fromUtf8("iPAddressLabel"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.iPAddressLabel)
        self.iPAddressLineEdit = QtGui.QLineEdit(DialogPassword)
        self.iPAddressLineEdit.setMaxLength(256)
        self.iPAddressLineEdit.setObjectName(_fromUtf8("iPAddressLineEdit"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.iPAddressLineEdit)
        self.usernameLabel = QtGui.QLabel(DialogPassword)
        self.usernameLabel.setObjectName(_fromUtf8("usernameLabel"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.usernameLabel)
        self.usernameLineEdit = QtGui.QLineEdit(DialogPassword)
        self.usernameLineEdit.setObjectName(_fromUtf8("usernameLineEdit"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.usernameLineEdit)
        self.passwordLabel = QtGui.QLabel(DialogPassword)
        self.passwordLabel.setObjectName(_fromUtf8("passwordLabel"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.LabelRole, self.passwordLabel)
        self.passwordLineEdit = QtGui.QLineEdit(DialogPassword)
        self.passwordLineEdit.setMaxLength(256)
        self.passwordLineEdit.setEchoMode(QtGui.QLineEdit.Password)
        self.passwordLineEdit.setObjectName(_fromUtf8("passwordLineEdit"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.FieldRole, self.passwordLineEdit)
        self.sudoPasswordLabel = QtGui.QLabel(DialogPassword)
        self.sudoPasswordLabel.setObjectName(_fromUtf8("sudoPasswordLabel"))
        self.formLayout.setWidget(6, QtGui.QFormLayout.LabelRole, self.sudoPasswordLabel)
        self.sudoPasswordLineEdit = QtGui.QLineEdit(DialogPassword)
        self.sudoPasswordLineEdit.setMaxLength(256)
        self.sudoPasswordLineEdit.setEchoMode(QtGui.QLineEdit.Password)
        self.sudoPasswordLineEdit.setObjectName(_fromUtf8("sudoPasswordLineEdit"))
        self.formLayout.setWidget(6, QtGui.QFormLayout.FieldRole, self.sudoPasswordLineEdit)
        self.useKeyFileLabel = QtGui.QLabel(DialogPassword)
        self.useKeyFileLabel.setObjectName(_fromUtf8("useKeyFileLabel"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.useKeyFileLabel)
        self.useKeyFileCheckBox = QtGui.QCheckBox(DialogPassword)
        self.useKeyFileCheckBox.setObjectName(_fromUtf8("useKeyFileCheckBox"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.useKeyFileCheckBox)
        self.verticalLayout.addLayout(self.formLayout)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.pushButton_addNew = QtGui.QPushButton(DialogPassword)
        self.pushButton_addNew.setObjectName(_fromUtf8("pushButton_addNew"))
        self.horizontalLayout.addWidget(self.pushButton_addNew)
        self.pushButton_remove = QtGui.QPushButton(DialogPassword)
        self.pushButton_remove.setObjectName(_fromUtf8("pushButton_remove"))
        self.horizontalLayout.addWidget(self.pushButton_remove)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton_cancel = QtGui.QPushButton(DialogPassword)
        self.pushButton_cancel.setObjectName(_fromUtf8("pushButton_cancel"))
        self.horizontalLayout.addWidget(self.pushButton_cancel)
        self.pushButton_ok = QtGui.QPushButton(DialogPassword)
        self.pushButton_ok.setObjectName(_fromUtf8("pushButton_ok"))
        self.horizontalLayout.addWidget(self.pushButton_ok)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.listWidget_messages = QtGui.QListWidget(DialogPassword)
        self.listWidget_messages.setMaximumSize(QtCore.QSize(16777215, 40))
        self.listWidget_messages.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.listWidget_messages.setObjectName(_fromUtf8("listWidget_messages"))
        self.verticalLayout.addWidget(self.listWidget_messages)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(DialogPassword)
        QtCore.QMetaObject.connectSlotsByName(DialogPassword)
        DialogPassword.setTabOrder(self.passwordLineEdit, self.sudoPasswordLineEdit)
        DialogPassword.setTabOrder(self.sudoPasswordLineEdit, self.previousConnectionsComboBox)
        DialogPassword.setTabOrder(self.previousConnectionsComboBox, self.rememberPasswordsCheckBox)
        DialogPassword.setTabOrder(self.rememberPasswordsCheckBox, self.iPAddressLineEdit)
        DialogPassword.setTabOrder(self.iPAddressLineEdit, self.usernameLineEdit)
        DialogPassword.setTabOrder(self.usernameLineEdit, self.useKeyFileCheckBox)
        DialogPassword.setTabOrder(self.useKeyFileCheckBox, self.listWidget_messages)

    def retranslateUi(self, DialogPassword):
        DialogPassword.setWindowTitle(_translate("DialogPassword", "Enter and select connection details", None))
        self.previousConnectionsLabel.setText(_translate("DialogPassword", "Previous connections:", None))
        self.rememberPasswordsLabel.setText(_translate("DialogPassword", "Remember passwords:", None))
        self.iPAddressLabel.setText(_translate("DialogPassword", "IP address:", None))
        self.usernameLabel.setText(_translate("DialogPassword", "Username:", None))
        self.passwordLabel.setText(_translate("DialogPassword", "Password: ", None))
        self.sudoPasswordLabel.setText(_translate("DialogPassword", "Sudo password *:", None))
        self.useKeyFileLabel.setText(_translate("DialogPassword", "Use key file:", None))
        self.pushButton_addNew.setText(_translate("DialogPassword", "Add New", None))
        self.pushButton_remove.setText(_translate("DialogPassword", "Remove", None))
        self.pushButton_cancel.setText(_translate("DialogPassword", "Cancel", None))
        self.pushButton_ok.setText(_translate("DialogPassword", "OK", None))

