# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mirrorless_mirrors.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(919, 659)
        MainWindow.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.imageViewer = QtWidgets.QGraphicsView(self.centralwidget)
        self.imageViewer.setMinimumSize(QtCore.QSize(600, 600))
        self.imageViewer.setObjectName("imageViewer")
        self.horizontalLayout.addWidget(self.imageViewer)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.label_2)
        self.lidarDistanceTextBox = QtWidgets.QTextEdit(self.centralwidget)
        self.lidarDistanceTextBox.setMaximumSize(QtCore.QSize(150, 25))
        self.lidarDistanceTextBox.setObjectName("lidarDistanceTextBox")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.lidarDistanceTextBox)
        self.lidarVelocityTextBox = QtWidgets.QTextEdit(self.centralwidget)
        self.lidarVelocityTextBox.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lidarVelocityTextBox.sizePolicy().hasHeightForWidth())
        self.lidarVelocityTextBox.setSizePolicy(sizePolicy)
        self.lidarVelocityTextBox.setMaximumSize(QtCore.QSize(150, 25))
        self.lidarVelocityTextBox.setObjectName("lidarVelocityTextBox")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.lidarVelocityTextBox)
        self.enableLidar = QtWidgets.QRadioButton(self.centralwidget)
        self.enableLidar.setObjectName("enableLidar")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.enableLidar)
        self.lidarSelector = QtWidgets.QComboBox(self.centralwidget)
        self.lidarSelector.setObjectName("lidarSelector")
        self.lidarSelector.addItem("")
        self.lidarSelector.addItem("")
        self.lidarSelector.addItem("")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.lidarSelector)
        self.enableCamera = QtWidgets.QRadioButton(self.centralwidget)
        self.enableCamera.setObjectName("enableCamera")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.enableCamera)
        self.cameraSelector = QtWidgets.QComboBox(self.centralwidget)
        self.cameraSelector.setObjectName("cameraSelector")
        self.cameraSelector.addItem("")
        self.cameraSelector.addItem("")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.cameraSelector)
        self.carDetectionStatusLabel = QtWidgets.QLabel(self.centralwidget)
        self.carDetectionStatusLabel.setObjectName("carDetectionStatusLabel")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.carDetectionStatusLabel)
        self.carDetectionStatusTextBox = QtWidgets.QLineEdit(self.centralwidget)
        self.carDetectionStatusTextBox.setObjectName("carDetectionStatusTextBox")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.carDetectionStatusTextBox)
        self.verticalLayout.addLayout(self.formLayout)
        self.horizontalLayout.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 919, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Lidar Distance Measurement"))
        self.label_2.setText(_translate("MainWindow", "Lidar Velocity Measurement"))
        self.enableLidar.setText(_translate("MainWindow", "Enable Lidar"))
        self.lidarSelector.setItemText(0, _translate("MainWindow", "Arduino Lidar"))
        self.lidarSelector.setItemText(1, _translate("MainWindow", "Virtual Lidar"))
        self.lidarSelector.setItemText(2, _translate("MainWindow", "UPLidar"))
        self.enableCamera.setText(_translate("MainWindow", "Enable Camera"))
        self.cameraSelector.setItemText(0, _translate("MainWindow", "RealSenseD435"))
        self.cameraSelector.setItemText(1, _translate("MainWindow", "Virtual Camera"))
        self.carDetectionStatusLabel.setText(_translate("MainWindow", "Car Detection Status"))


