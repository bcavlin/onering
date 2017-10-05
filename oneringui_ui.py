# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './oneringui.ui'
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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.setWindowModality(QtCore.Qt.WindowModal)
        MainWindow.resize(465, 374)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(240, 0))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Ubuntu Mono"))
        font.setPointSize(12)
        font.setItalic(False)
        MainWindow.setFont(font)
        MainWindow.setFocusPolicy(QtCore.Qt.StrongFocus)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("images/icon-hat-white.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.pushButton_connections = QtGui.QPushButton(self.centralwidget)
        self.pushButton_connections.setObjectName(_fromUtf8("pushButton_connections"))
        self.gridLayout_2.addWidget(self.pushButton_connections, 0, 1, 1, 1)
        self.pushButton_Firewall = QtGui.QPushButton(self.centralwidget)
        self.pushButton_Firewall.setObjectName(_fromUtf8("pushButton_Firewall"))
        self.gridLayout_2.addWidget(self.pushButton_Firewall, 0, 0, 1, 1)
        self.pushButton_Netstat = QtGui.QPushButton(self.centralwidget)
        self.pushButton_Netstat.setEnabled(False)
        self.pushButton_Netstat.setObjectName(_fromUtf8("pushButton_Netstat"))
        self.gridLayout_2.addWidget(self.pushButton_Netstat, 1, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 2, 0, 1, 1)
        self.pushButton_sudo = QtGui.QPushButton(self.centralwidget)
        self.pushButton_sudo.setMinimumSize(QtCore.QSize(0, 0))
        self.pushButton_sudo.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.pushButton_sudo.setObjectName(_fromUtf8("pushButton_sudo"))
        self.gridLayout_2.addWidget(self.pushButton_sudo, 3, 0, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_2, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusBar = QtGui.QStatusBar(MainWindow)
        self.statusBar.setObjectName(_fromUtf8("statusBar"))
        MainWindow.setStatusBar(self.statusBar)
        self.menuBar = QtGui.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 465, 24))
        self.menuBar.setObjectName(_fromUtf8("menuBar"))
        self.menuHelp = QtGui.QMenu(self.menuBar)
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
        MainWindow.setMenuBar(self.menuBar)
        self.action_About = QtGui.QAction(MainWindow)
        self.action_About.setObjectName(_fromUtf8("action_About"))
        self.menuHelp.addAction(self.action_About)
        self.menuBar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.pushButton_Firewall, self.pushButton_connections)
        MainWindow.setTabOrder(self.pushButton_connections, self.pushButton_Netstat)
        MainWindow.setTabOrder(self.pushButton_Netstat, self.pushButton_sudo)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "One Ring", None))
        self.pushButton_connections.setText(_translate("MainWindow", "Active Connections", None))
        self.pushButton_Firewall.setText(_translate("MainWindow", "Firewall (UFW)", None))
        self.pushButton_Netstat.setText(_translate("MainWindow", "Network", None))
        self.pushButton_sudo.setText(_translate("MainWindow", "sudo / connection settings", None))
        self.menuHelp.setTitle(_translate("MainWindow", "&Help", None))
        self.action_About.setText(_translate("MainWindow", "&About", None))

