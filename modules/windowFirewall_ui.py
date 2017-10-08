# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './modules/windowFirewall.ui'
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

class Ui_MainWindow_firewall(object):
    def setupUi(self, MainWindow_firewall):
        MainWindow_firewall.setObjectName(_fromUtf8("MainWindow_firewall"))
        MainWindow_firewall.setWindowModality(QtCore.Qt.WindowModal)
        MainWindow_firewall.resize(796, 406)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Ubuntu Mono"))
        font.setPointSize(12)
        MainWindow_firewall.setFont(font)
        MainWindow_firewall.setFocusPolicy(QtCore.Qt.StrongFocus)
        MainWindow_firewall.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.centralwidget = QtGui.QWidget(MainWindow_firewall)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.groupBox_2 = QtGui.QGroupBox(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tableView_firewall = QtGui.QTableView(self.groupBox_2)
        self.tableView_firewall.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Ubuntu Mono"))
        self.tableView_firewall.setFont(font)
        self.tableView_firewall.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tableView_firewall.setProperty("showDropIndicator", False)
        self.tableView_firewall.setDragDropOverwriteMode(False)
        self.tableView_firewall.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tableView_firewall.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tableView_firewall.setShowGrid(True)
        self.tableView_firewall.setObjectName(_fromUtf8("tableView_firewall"))
        self.verticalLayout.addWidget(self.tableView_firewall)
        self.horizontalLayout.addWidget(self.groupBox_2)
        self.groupBox = QtGui.QGroupBox(self.centralwidget)
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
        self.pushButton_insert = QtGui.QPushButton(self.groupBox)
        self.pushButton_insert.setEnabled(False)
        self.pushButton_insert.setObjectName(_fromUtf8("pushButton_insert"))
        self.verticalLayout_3.addWidget(self.pushButton_insert)
        self.pushButton_remove = QtGui.QPushButton(self.groupBox)
        self.pushButton_remove.setEnabled(False)
        self.pushButton_remove.setCheckable(False)
        self.pushButton_remove.setChecked(False)
        self.pushButton_remove.setAutoDefault(False)
        self.pushButton_remove.setObjectName(_fromUtf8("pushButton_remove"))
        self.verticalLayout_3.addWidget(self.pushButton_remove)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem)
        self.pushButton_enabled = QtGui.QPushButton(self.groupBox)
        self.pushButton_enabled.setEnabled(False)
        self.pushButton_enabled.setObjectName(_fromUtf8("pushButton_enabled"))
        self.verticalLayout_3.addWidget(self.pushButton_enabled)
        self.verticalLayout_4.addLayout(self.verticalLayout_3)
        self.horizontalLayout.addWidget(self.groupBox)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        MainWindow_firewall.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow_firewall)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow_firewall.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow_firewall)
        QtCore.QMetaObject.connectSlotsByName(MainWindow_firewall)

    def retranslateUi(self, MainWindow_firewall):
        MainWindow_firewall.setWindowTitle(_translate("MainWindow_firewall", "Firewall", None))
        self.groupBox_2.setTitle(_translate("MainWindow_firewall", "Rules", None))
        self.groupBox.setTitle(_translate("MainWindow_firewall", "Options", None))
        self.pushButton_refresh.setText(_translate("MainWindow_firewall", "Refresh", None))
        self.pushButton_insert.setText(_translate("MainWindow_firewall", "Insert Rule", None))
        self.pushButton_remove.setText(_translate("MainWindow_firewall", "Remove Rule", None))
        self.pushButton_enabled.setText(_translate("MainWindow_firewall", "Disable", None))

