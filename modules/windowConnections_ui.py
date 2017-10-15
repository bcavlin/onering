# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './modules/windowConnections.ui'
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

class Ui_MainWindow_connections(object):
    def setupUi(self, MainWindow_connections):
        MainWindow_connections.setObjectName(_fromUtf8("MainWindow_connections"))
        MainWindow_connections.setWindowModality(QtCore.Qt.WindowModal)
        MainWindow_connections.resize(836, 496)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Ubuntu Mono"))
        font.setPointSize(12)
        MainWindow_connections.setFont(font)
        MainWindow_connections.setFocusPolicy(QtCore.Qt.StrongFocus)
        MainWindow_connections.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.centralwidget = QtGui.QWidget(MainWindow_connections)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.tabWidget.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab_ns = QtGui.QWidget()
        self.tab_ns.setObjectName(_fromUtf8("tab_ns"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.tab_ns)
        self.horizontalLayout_3.setMargin(0)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.groupBox = QtGui.QGroupBox(self.tab_ns)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.filterLabel = QtGui.QLabel(self.groupBox)
        self.filterLabel.setObjectName(_fromUtf8("filterLabel"))
        self.horizontalLayout_4.addWidget(self.filterLabel)
        self.filterLineEdit = QtGui.QLineEdit(self.groupBox)
        self.filterLineEdit.setEnabled(True)
        self.filterLineEdit.setAutoFillBackground(False)
        self.filterLineEdit.setText(_fromUtf8(""))
        self.filterLineEdit.setMaxLength(200)
        self.filterLineEdit.setFrame(True)
        self.filterLineEdit.setReadOnly(False)
        self.filterLineEdit.setObjectName(_fromUtf8("filterLineEdit"))
        self.horizontalLayout_4.addWidget(self.filterLineEdit)
        self.pushButton_clear = QtGui.QPushButton(self.groupBox)
        self.pushButton_clear.setObjectName(_fromUtf8("pushButton_clear"))
        self.horizontalLayout_4.addWidget(self.pushButton_clear)
        self.verticalLayout_4.addLayout(self.horizontalLayout_4)
        self.tableView_netstat = QtGui.QTableView(self.groupBox)
        self.tableView_netstat.setAutoScroll(False)
        self.tableView_netstat.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tableView_netstat.setProperty("showDropIndicator", False)
        self.tableView_netstat.setDragDropOverwriteMode(False)
        self.tableView_netstat.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tableView_netstat.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tableView_netstat.setSortingEnabled(True)
        self.tableView_netstat.setObjectName(_fromUtf8("tableView_netstat"))
        self.verticalLayout_4.addWidget(self.tableView_netstat)
        self.horizontalLayout.addWidget(self.groupBox)
        self.groupBox_2 = QtGui.QGroupBox(self.tab_ns)
        self.groupBox_2.setMinimumSize(QtCore.QSize(200, 0))
        self.groupBox_2.setMaximumSize(QtCore.QSize(200, 16777215))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.checkBox_numeric = QtGui.QCheckBox(self.groupBox_2)
        self.checkBox_numeric.setChecked(True)
        self.checkBox_numeric.setObjectName(_fromUtf8("checkBox_numeric"))
        self.verticalLayout.addWidget(self.checkBox_numeric)
        self.checkBox_hide_local = QtGui.QCheckBox(self.groupBox_2)
        self.checkBox_hide_local.setObjectName(_fromUtf8("checkBox_hide_local"))
        self.verticalLayout.addWidget(self.checkBox_hide_local)
        self.checkBox_hide_empty = QtGui.QCheckBox(self.groupBox_2)
        self.checkBox_hide_empty.setObjectName(_fromUtf8("checkBox_hide_empty"))
        self.verticalLayout.addWidget(self.checkBox_hide_empty)
        self.line = QtGui.QFrame(self.groupBox_2)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayout.addWidget(self.line)
        self.pushButton_start_netstat = QtGui.QPushButton(self.groupBox_2)
        self.pushButton_start_netstat.setObjectName(_fromUtf8("pushButton_start_netstat"))
        self.verticalLayout.addWidget(self.pushButton_start_netstat)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.horizontalLayout.addWidget(self.groupBox_2)
        self.horizontalLayout_3.addLayout(self.horizontalLayout)
        self.tabWidget.addTab(self.tab_ns, _fromUtf8(""))
        self.horizontalLayout_2.addWidget(self.tabWidget)
        MainWindow_connections.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow_connections)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow_connections.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow_connections)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow_connections)
        MainWindow_connections.setTabOrder(self.pushButton_start_netstat, self.checkBox_numeric)
        MainWindow_connections.setTabOrder(self.checkBox_numeric, self.filterLineEdit)
        MainWindow_connections.setTabOrder(self.filterLineEdit, self.pushButton_clear)
        MainWindow_connections.setTabOrder(self.pushButton_clear, self.tableView_netstat)
        MainWindow_connections.setTabOrder(self.tableView_netstat, self.tabWidget)

    def retranslateUi(self, MainWindow_connections):
        MainWindow_connections.setWindowTitle(_translate("MainWindow_connections", "Connections", None))
        self.groupBox.setTitle(_translate("MainWindow_connections", "List", None))
        self.filterLabel.setText(_translate("MainWindow_connections", "Search string:", None))
        self.filterLineEdit.setPlaceholderText(_translate("MainWindow_connections", "Filter text (all columns ; as separator)", None))
        self.pushButton_clear.setText(_translate("MainWindow_connections", "Clear", None))
        self.groupBox_2.setTitle(_translate("MainWindow_connections", "Options", None))
        self.checkBox_numeric.setText(_translate("MainWindow_connections", "Numeric", None))
        self.checkBox_hide_local.setText(_translate("MainWindow_connections", "Hide local->local", None))
        self.checkBox_hide_empty.setText(_translate("MainWindow_connections", "Hide empty", None))
        self.pushButton_start_netstat.setText(_translate("MainWindow_connections", "Start", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_ns), _translate("MainWindow_connections", "Connections (netstat)", None))

