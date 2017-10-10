# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './modules/dialogFirewallRule.ui'
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

class Ui_Dialog_firewall_rules(object):
    def setupUi(self, Dialog_firewall_rules):
        Dialog_firewall_rules.setObjectName(_fromUtf8("Dialog_firewall_rules"))
        Dialog_firewall_rules.resize(403, 345)
        self.verticalLayout_2 = QtGui.QVBoxLayout(Dialog_firewall_rules)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.formLayout_2 = QtGui.QFormLayout()
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.actionLabel = QtGui.QLabel(Dialog_firewall_rules)
        self.actionLabel.setObjectName(_fromUtf8("actionLabel"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.actionLabel)
        self.actionComboBox = QtGui.QComboBox(Dialog_firewall_rules)
        self.actionComboBox.setObjectName(_fromUtf8("actionComboBox"))
        self.actionComboBox.addItem(_fromUtf8(""))
        self.actionComboBox.addItem(_fromUtf8(""))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.FieldRole, self.actionComboBox)
        self.directionLabel = QtGui.QLabel(Dialog_firewall_rules)
        self.directionLabel.setObjectName(_fromUtf8("directionLabel"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, self.directionLabel)
        self.directionComboBox = QtGui.QComboBox(Dialog_firewall_rules)
        self.directionComboBox.setObjectName(_fromUtf8("directionComboBox"))
        self.directionComboBox.addItem(_fromUtf8(""))
        self.directionComboBox.addItem(_fromUtf8(""))
        self.directionComboBox.addItem(_fromUtf8(""))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.FieldRole, self.directionComboBox)
        self.serviceLabel = QtGui.QLabel(Dialog_firewall_rules)
        self.serviceLabel.setObjectName(_fromUtf8("serviceLabel"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.LabelRole, self.serviceLabel)
        self.serviceComboBox = QtGui.QComboBox(Dialog_firewall_rules)
        self.serviceComboBox.setObjectName(_fromUtf8("serviceComboBox"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.FieldRole, self.serviceComboBox)
        self.portLabel = QtGui.QLabel(Dialog_firewall_rules)
        self.portLabel.setObjectName(_fromUtf8("portLabel"))
        self.formLayout_2.setWidget(3, QtGui.QFormLayout.LabelRole, self.portLabel)
        self.portLineEdit = QtGui.QLineEdit(Dialog_firewall_rules)
        self.portLineEdit.setObjectName(_fromUtf8("portLineEdit"))
        self.formLayout_2.setWidget(3, QtGui.QFormLayout.FieldRole, self.portLineEdit)
        self.protocolLabel = QtGui.QLabel(Dialog_firewall_rules)
        self.protocolLabel.setObjectName(_fromUtf8("protocolLabel"))
        self.formLayout_2.setWidget(4, QtGui.QFormLayout.LabelRole, self.protocolLabel)
        self.protocolComboBox = QtGui.QComboBox(Dialog_firewall_rules)
        self.protocolComboBox.setObjectName(_fromUtf8("protocolComboBox"))
        self.protocolComboBox.addItem(_fromUtf8(""))
        self.protocolComboBox.addItem(_fromUtf8(""))
        self.protocolComboBox.addItem(_fromUtf8(""))
        self.formLayout_2.setWidget(4, QtGui.QFormLayout.FieldRole, self.protocolComboBox)
        self.fromIPLabel = QtGui.QLabel(Dialog_firewall_rules)
        self.fromIPLabel.setObjectName(_fromUtf8("fromIPLabel"))
        self.formLayout_2.setWidget(5, QtGui.QFormLayout.LabelRole, self.fromIPLabel)
        self.fromIPLineEdit = QtGui.QLineEdit(Dialog_firewall_rules)
        self.fromIPLineEdit.setObjectName(_fromUtf8("fromIPLineEdit"))
        self.formLayout_2.setWidget(5, QtGui.QFormLayout.FieldRole, self.fromIPLineEdit)
        self.toIPLabel = QtGui.QLabel(Dialog_firewall_rules)
        self.toIPLabel.setObjectName(_fromUtf8("toIPLabel"))
        self.formLayout_2.setWidget(6, QtGui.QFormLayout.LabelRole, self.toIPLabel)
        self.toIPLineEdit = QtGui.QLineEdit(Dialog_firewall_rules)
        self.toIPLineEdit.setObjectName(_fromUtf8("toIPLineEdit"))
        self.formLayout_2.setWidget(6, QtGui.QFormLayout.FieldRole, self.toIPLineEdit)
        self.interfaceLabel = QtGui.QLabel(Dialog_firewall_rules)
        self.interfaceLabel.setObjectName(_fromUtf8("interfaceLabel"))
        self.formLayout_2.setWidget(7, QtGui.QFormLayout.LabelRole, self.interfaceLabel)
        self.interfaceComboBox = QtGui.QComboBox(Dialog_firewall_rules)
        self.interfaceComboBox.setObjectName(_fromUtf8("interfaceComboBox"))
        self.formLayout_2.setWidget(7, QtGui.QFormLayout.FieldRole, self.interfaceComboBox)
        self.verticalLayout.addLayout(self.formLayout_2)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.label_command = QtGui.QLabel(Dialog_firewall_rules)
        self.label_command.setAlignment(QtCore.Qt.AlignCenter)
        self.label_command.setObjectName(_fromUtf8("label_command"))
        self.verticalLayout_2.addWidget(self.label_command)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog_firewall_rules)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(Dialog_firewall_rules)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog_firewall_rules.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog_firewall_rules.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog_firewall_rules)

    def retranslateUi(self, Dialog_firewall_rules):
        Dialog_firewall_rules.setWindowTitle(_translate("Dialog_firewall_rules", "Add Firewall Rule", None))
        self.actionLabel.setText(_translate("Dialog_firewall_rules", "Action:", None))
        self.actionComboBox.setItemText(0, _translate("Dialog_firewall_rules", "allow", None))
        self.actionComboBox.setItemText(1, _translate("Dialog_firewall_rules", "deny", None))
        self.directionLabel.setText(_translate("Dialog_firewall_rules", "Direction: ", None))
        self.directionComboBox.setItemText(0, _translate("Dialog_firewall_rules", "both", None))
        self.directionComboBox.setItemText(1, _translate("Dialog_firewall_rules", "in", None))
        self.directionComboBox.setItemText(2, _translate("Dialog_firewall_rules", "out", None))
        self.serviceLabel.setText(_translate("Dialog_firewall_rules", "Service:", None))
        self.portLabel.setText(_translate("Dialog_firewall_rules", "Port:", None))
        self.portLineEdit.setPlaceholderText(_translate("Dialog_firewall_rules", "e.g. 80 or 80,82 or 8080:9090", None))
        self.protocolLabel.setText(_translate("Dialog_firewall_rules", "Protocol:", None))
        self.protocolComboBox.setItemText(0, _translate("Dialog_firewall_rules", "both", None))
        self.protocolComboBox.setItemText(1, _translate("Dialog_firewall_rules", "tcp", None))
        self.protocolComboBox.setItemText(2, _translate("Dialog_firewall_rules", "udp", None))
        self.fromIPLabel.setText(_translate("Dialog_firewall_rules", "From IP:", None))
        self.fromIPLineEdit.setPlaceholderText(_translate("Dialog_firewall_rules", "e.g. any or 192.168.1.1 or 192.168.1.0/24", None))
        self.toIPLabel.setText(_translate("Dialog_firewall_rules", "To IP:", None))
        self.toIPLineEdit.setPlaceholderText(_translate("Dialog_firewall_rules", "e.g. any or 192.168.1.1 or 192.168.1.0/24", None))
        self.interfaceLabel.setText(_translate("Dialog_firewall_rules", "Interface:", None))
        self.label_command.setText(_translate("Dialog_firewall_rules", "command...", None))

