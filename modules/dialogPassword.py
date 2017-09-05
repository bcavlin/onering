# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialogPassword.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
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
        DialogPassword.resize(365, 82)
        self.verticalLayout_2 = QtGui.QVBoxLayout(DialogPassword)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.passwordLabel = QtGui.QLabel(DialogPassword)
        self.passwordLabel.setObjectName(_fromUtf8("passwordLabel"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.passwordLabel)
        self.passwordLineEdit = QtGui.QLineEdit(DialogPassword)
        self.passwordLineEdit.setMaxLength(30)
        self.passwordLineEdit.setEchoMode(QtGui.QLineEdit.Password)
        self.passwordLineEdit.setObjectName(_fromUtf8("passwordLineEdit"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.passwordLineEdit)
        self.verticalLayout.addLayout(self.formLayout)
        self.buttonBox = QtGui.QDialogButtonBox(DialogPassword)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(DialogPassword)
        QtCore.QMetaObject.connectSlotsByName(DialogPassword)

    def retranslateUi(self, DialogPassword):
        DialogPassword.setWindowTitle(_translate("DialogPassword", "Password Dialog", None))
        self.passwordLabel.setText(_translate("DialogPassword", "Password: ", None))

