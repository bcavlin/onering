# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './modules/dialogConnections.ui'
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

class Ui_DialogConnections(object):
    def setupUi(self, DialogConnections):
        DialogConnections.setObjectName(_fromUtf8("DialogConnections"))
        DialogConnections.resize(786, 447)
        self.horizontalLayout_2 = QtGui.QHBoxLayout(DialogConnections)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.tabWidget = QtGui.QTabWidget(DialogConnections)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab_1 = QtGui.QWidget()
        self.tab_1.setObjectName(_fromUtf8("tab_1"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.tab_1)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.groupBox = QtGui.QGroupBox(self.tab_1)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.tableWidget = QtGui.QTableWidget(self.groupBox)
        self.tableWidget.setAutoScroll(False)
        self.tableWidget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(10)
        self.tableWidget.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(7, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(8, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(9, item)
        self.verticalLayout_3.addWidget(self.tableWidget)
        self.horizontalLayout.addWidget(self.groupBox)
        self.groupBox_2 = QtGui.QGroupBox(self.tab_1)
        self.groupBox_2.setMinimumSize(QtCore.QSize(200, 0))
        self.groupBox_2.setMaximumSize(QtCore.QSize(200, 16777215))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.pushButton_start_netstat = QtGui.QPushButton(self.groupBox_2)
        self.pushButton_start_netstat.setObjectName(_fromUtf8("pushButton_start_netstat"))
        self.verticalLayout.addWidget(self.pushButton_start_netstat)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.horizontalLayout.addWidget(self.groupBox_2)
        self.horizontalLayout_3.addLayout(self.horizontalLayout)
        self.tabWidget.addTab(self.tab_1, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.horizontalLayout_5 = QtGui.QHBoxLayout(self.tab_2)
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.groupBox_3 = QtGui.QGroupBox(self.tab_2)
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.tableWidget_2 = QtGui.QTableWidget(self.groupBox_3)
        self.tableWidget_2.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tableWidget_2.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tableWidget_2.setObjectName(_fromUtf8("tableWidget_2"))
        self.tableWidget_2.setColumnCount(7)
        self.tableWidget_2.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(4, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(5, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(6, item)
        self.verticalLayout_4.addWidget(self.tableWidget_2)
        self.horizontalLayout_4.addWidget(self.groupBox_3)
        self.groupBox_4 = QtGui.QGroupBox(self.tab_2)
        self.groupBox_4.setMinimumSize(QtCore.QSize(200, 0))
        self.groupBox_4.setMaximumSize(QtCore.QSize(200, 16777215))
        self.groupBox_4.setObjectName(_fromUtf8("groupBox_4"))
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.groupBox_4)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.verticalLayout_6 = QtGui.QVBoxLayout()
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.pushButton_start_tcpdump = QtGui.QPushButton(self.groupBox_4)
        self.pushButton_start_tcpdump.setObjectName(_fromUtf8("pushButton_start_tcpdump"))
        self.verticalLayout_6.addWidget(self.pushButton_start_tcpdump)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_6.addItem(spacerItem1)
        self.verticalLayout_5.addLayout(self.verticalLayout_6)
        self.horizontalLayout_4.addWidget(self.groupBox_4)
        self.horizontalLayout_5.addLayout(self.horizontalLayout_4)
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.horizontalLayout_2.addWidget(self.tabWidget)

        self.retranslateUi(DialogConnections)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(DialogConnections)
        DialogConnections.setTabOrder(self.tabWidget, self.pushButton_start_netstat)
        DialogConnections.setTabOrder(self.pushButton_start_netstat, self.tableWidget)
        DialogConnections.setTabOrder(self.tableWidget, self.pushButton_start_tcpdump)
        DialogConnections.setTabOrder(self.pushButton_start_tcpdump, self.tableWidget_2)

    def retranslateUi(self, DialogConnections):
        DialogConnections.setWindowTitle(_translate("DialogConnections", "Connections", None))
        self.groupBox.setTitle(_translate("DialogConnections", "List", None))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("DialogConnections", "Last", None))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("DialogConnections", "Proto", None))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("DialogConnections", "Local Addr", None))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("DialogConnections", "Local Port", None))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("DialogConnections", "Remote Addr", None))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("DialogConnections", "Remote Port", None))
        item = self.tableWidget.horizontalHeaderItem(6)
        item.setText(_translate("DialogConnections", "State", None))
        item = self.tableWidget.horizontalHeaderItem(7)
        item.setText(_translate("DialogConnections", "PID", None))
        item = self.tableWidget.horizontalHeaderItem(8)
        item.setText(_translate("DialogConnections", "Application", None))
        item = self.tableWidget.horizontalHeaderItem(9)
        item.setText(_translate("DialogConnections", "SHA256", None))
        self.groupBox_2.setTitle(_translate("DialogConnections", "Options", None))
        self.pushButton_start_netstat.setText(_translate("DialogConnections", "Start", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_1), _translate("DialogConnections", "Connections (netstat)", None))
        self.groupBox_3.setTitle(_translate("DialogConnections", "List", None))
        item = self.tableWidget_2.horizontalHeaderItem(0)
        item.setText(_translate("DialogConnections", "Last", None))
        item = self.tableWidget_2.horizontalHeaderItem(1)
        item.setText(_translate("DialogConnections", "Proto", None))
        item = self.tableWidget_2.horizontalHeaderItem(2)
        item.setText(_translate("DialogConnections", "Local Address", None))
        item = self.tableWidget_2.horizontalHeaderItem(3)
        item.setText(_translate("DialogConnections", "Local Port", None))
        item = self.tableWidget_2.horizontalHeaderItem(4)
        item.setText(_translate("DialogConnections", "Remote Address", None))
        item = self.tableWidget_2.horizontalHeaderItem(5)
        item.setText(_translate("DialogConnections", "Remote Port", None))
        item = self.tableWidget_2.horizontalHeaderItem(6)
        item.setText(_translate("DialogConnections", "Total", None))
        self.groupBox_4.setTitle(_translate("DialogConnections", "Options", None))
        self.pushButton_start_tcpdump.setText(_translate("DialogConnections", "Start", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("DialogConnections", "Trace (tcpdump)", None))

