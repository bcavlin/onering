# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './modules/dialogFirewall.ui'
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

class Ui_DialogFirewall(object):
    def setupUi(self, DialogFirewall):
        DialogFirewall.setObjectName(_fromUtf8("DialogFirewall"))
        DialogFirewall.resize(795, 485)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Ubuntu Mono"))
        DialogFirewall.setFont(font)
        self.verticalLayout_2 = QtGui.QVBoxLayout(DialogFirewall)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.groupBox_2 = QtGui.QGroupBox(DialogFirewall)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tableWidget = QtGui.QTableWidget(self.groupBox_2)
        self.tableWidget.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Ubuntu Mono"))
        self.tableWidget.setFont(font)
        self.tableWidget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setProperty("showDropIndicator", False)
        self.tableWidget.setDragDropOverwriteMode(False)
        self.tableWidget.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tableWidget.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tableWidget.setShowGrid(True)
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        item.setText(_fromUtf8("#"))
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        self.verticalLayout.addWidget(self.tableWidget)
        self.horizontalLayout.addWidget(self.groupBox_2)
        self.groupBox = QtGui.QGroupBox(DialogFirewall)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setMinimumSize(QtCore.QSize(200, 0))
        self.groupBox.setMaximumSize(QtCore.QSize(200, 16777215))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.pushButton_refresh = QtGui.QPushButton(self.groupBox)
        self.pushButton_refresh.setDefault(True)
        self.pushButton_refresh.setObjectName(_fromUtf8("pushButton_refresh"))
        self.verticalLayout_3.addWidget(self.pushButton_refresh)
        self.pushButton_removeRule = QtGui.QPushButton(self.groupBox)
        self.pushButton_removeRule.setEnabled(False)
        self.pushButton_removeRule.setCheckable(False)
        self.pushButton_removeRule.setChecked(False)
        self.pushButton_removeRule.setAutoDefault(False)
        self.pushButton_removeRule.setObjectName(_fromUtf8("pushButton_removeRule"))
        self.verticalLayout_3.addWidget(self.pushButton_removeRule)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem)
        self.verticalLayout_4.addLayout(self.verticalLayout_3)
        self.horizontalLayout.addWidget(self.groupBox)
        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.retranslateUi(DialogFirewall)
        QtCore.QMetaObject.connectSlotsByName(DialogFirewall)
        DialogFirewall.setTabOrder(self.pushButton_refresh, self.pushButton_removeRule)

    def retranslateUi(self, DialogFirewall):
        DialogFirewall.setWindowTitle(_translate("DialogFirewall", "Firewall (UFW)", None))
        self.groupBox_2.setTitle(_translate("DialogFirewall", "Rules", None))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("DialogFirewall", "To", None))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("DialogFirewall", "Action", None))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("DialogFirewall", "From", None))
        self.groupBox.setTitle(_translate("DialogFirewall", "Options", None))
        self.pushButton_refresh.setText(_translate("DialogFirewall", "Refresh", None))
        self.pushButton_removeRule.setText(_translate("DialogFirewall", "Remove Rule", None))

