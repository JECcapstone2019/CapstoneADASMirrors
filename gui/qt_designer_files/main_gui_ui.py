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
        MainWindow.resize(1250, 560)
        MainWindow.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.lidarData = QtWidgets.QLabel(self.centralwidget)
        self.lidarData.setText("")
        self.lidarData.setObjectName("lidarData")
        self.verticalLayout.addWidget(self.lidarData)
        self.imageViewer = QtWidgets.QLabel(self.centralwidget)
        self.imageViewer.setMinimumSize(QtCore.QSize(640, 480))
        self.imageViewer.setText("")
        self.imageViewer.setObjectName("imageViewer")
        self.verticalLayout.addWidget(self.imageViewer)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridLayout.addWidget(self.line_2, 7, 0, 1, 1)
        self.line_10 = QtWidgets.QFrame(self.centralwidget)
        self.line_10.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_10.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_10.setObjectName("line_10")
        self.gridLayout.addWidget(self.line_10, 23, 2, 1, 1)
        self.line_8 = QtWidgets.QFrame(self.centralwidget)
        self.line_8.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_8.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_8.setObjectName("line_8")
        self.gridLayout.addWidget(self.line_8, 10, 0, 1, 1)
        self.line_4 = QtWidgets.QFrame(self.centralwidget)
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.gridLayout.addWidget(self.line_4, 10, 1, 1, 1)
        self.cameraTitle = QtWidgets.QLabel(self.centralwidget)
        self.cameraTitle.setObjectName("cameraTitle")
        self.gridLayout.addWidget(self.cameraTitle, 5, 0, 1, 1)
        self.line_3 = QtWidgets.QFrame(self.centralwidget)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.gridLayout.addWidget(self.line_3, 14, 0, 1, 1)
        self.simulationTitle = QtWidgets.QLabel(self.centralwidget)
        self.simulationTitle.setObjectName("simulationTitle")
        self.gridLayout.addWidget(self.simulationTitle, 20, 0, 1, 1)
        self.lidarTitle = QtWidgets.QLabel(self.centralwidget)
        self.lidarTitle.setObjectName("lidarTitle")
        self.gridLayout.addWidget(self.lidarTitle, 0, 0, 1, 1)
        self.line_7 = QtWidgets.QFrame(self.centralwidget)
        self.line_7.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_7.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_7.setObjectName("line_7")
        self.gridLayout.addWidget(self.line_7, 1, 1, 1, 1)
        self.line_6 = QtWidgets.QFrame(self.centralwidget)
        self.line_6.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_6.setObjectName("line_6")
        self.gridLayout.addWidget(self.line_6, 7, 1, 1, 1)
        self.line_5 = QtWidgets.QFrame(self.centralwidget)
        self.line_5.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.gridLayout.addWidget(self.line_5, 14, 1, 1, 1)
        self.line_9 = QtWidgets.QFrame(self.centralwidget)
        self.line_9.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_9.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_9.setObjectName("line_9")
        self.gridLayout.addWidget(self.line_9, 23, 0, 1, 1)
        self.line_12 = QtWidgets.QFrame(self.centralwidget)
        self.line_12.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_12.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_12.setObjectName("line_12")
        self.gridLayout.addWidget(self.line_12, 4, 0, 1, 1)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 1, 0, 1, 1)
        self.line_11 = QtWidgets.QFrame(self.centralwidget)
        self.line_11.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_11.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_11.setObjectName("line_11")
        self.gridLayout.addWidget(self.line_11, 23, 1, 1, 1)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.lidarGetVelocityButton = QtWidgets.QPushButton(self.centralwidget)
        self.lidarGetVelocityButton.setObjectName("lidarGetVelocityButton")
        self.gridLayout_2.addWidget(self.lidarGetVelocityButton, 0, 2, 1, 1)
        self.lidarGetDistanceButton = QtWidgets.QPushButton(self.centralwidget)
        self.lidarGetDistanceButton.setObjectName("lidarGetDistanceButton")
        self.gridLayout_2.addWidget(self.lidarGetDistanceButton, 0, 1, 1, 1)
        self.lidarStreamVelocity = QtWidgets.QCheckBox(self.centralwidget)
        self.lidarStreamVelocity.setObjectName("lidarStreamVelocity")
        self.gridLayout_2.addWidget(self.lidarStreamVelocity, 0, 5, 1, 1)
        self.lidarSetupButton = QtWidgets.QPushButton(self.centralwidget)
        self.lidarSetupButton.setObjectName("lidarSetupButton")
        self.gridLayout_2.addWidget(self.lidarSetupButton, 0, 0, 1, 1)
        self.lidarStreamDistance = QtWidgets.QCheckBox(self.centralwidget)
        self.lidarStreamDistance.setObjectName("lidarStreamDistance")
        self.gridLayout_2.addWidget(self.lidarStreamDistance, 0, 3, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_2, 0, 1, 1, 1)
        self.line_13 = QtWidgets.QFrame(self.centralwidget)
        self.line_13.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_13.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_13.setObjectName("line_13")
        self.gridLayout.addWidget(self.line_13, 4, 1, 1, 1)
        self.simulationSelectFolder = QtWidgets.QPushButton(self.centralwidget)
        self.simulationSelectFolder.setObjectName("simulationSelectFolder")
        self.gridLayout.addWidget(self.simulationSelectFolder, 26, 0, 1, 1)
        self.simulationRunSimulation = QtWidgets.QCheckBox(self.centralwidget)
        self.simulationRunSimulation.setEnabled(False)
        self.simulationRunSimulation.setObjectName("simulationRunSimulation")
        self.gridLayout.addWidget(self.simulationRunSimulation, 25, 0, 1, 1)
        self.simulationFolderSelectedTextEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.simulationFolderSelectedTextEdit.setEnabled(True)
        self.simulationFolderSelectedTextEdit.setObjectName("simulationFolderSelectedTextEdit")
        self.gridLayout.addWidget(self.simulationFolderSelectedTextEdit, 26, 1, 1, 1)
        self.lidarEnableCheckBox = QtWidgets.QCheckBox(self.centralwidget)
        self.lidarEnableCheckBox.setObjectName("lidarEnableCheckBox")
        self.gridLayout.addWidget(self.lidarEnableCheckBox, 2, 0, 1, 1)
        self.simulationStartSavingNew = QtWidgets.QCheckBox(self.centralwidget)
        self.simulationStartSavingNew.setObjectName("simulationStartSavingNew")
        self.gridLayout.addWidget(self.simulationStartSavingNew, 25, 1, 1, 1)
        self.lidarSelection = QtWidgets.QComboBox(self.centralwidget)
        self.lidarSelection.setObjectName("lidarSelection")
        self.gridLayout.addWidget(self.lidarSelection, 2, 1, 1, 1)
        self.carDetectionEnableCheckBox = QtWidgets.QCheckBox(self.centralwidget)
        self.carDetectionEnableCheckBox.setObjectName("carDetectionEnableCheckBox")
        self.gridLayout.addWidget(self.carDetectionEnableCheckBox, 12, 1, 1, 1)
        self.cameraEnableCheckBox = QtWidgets.QCheckBox(self.centralwidget)
        self.cameraEnableCheckBox.setObjectName("cameraEnableCheckBox")
        self.gridLayout.addWidget(self.cameraEnableCheckBox, 5, 1, 1, 1)
        self.carDetectionSelection = QtWidgets.QComboBox(self.centralwidget)
        self.carDetectionSelection.setObjectName("carDetectionSelection")
        self.gridLayout.addWidget(self.carDetectionSelection, 13, 1, 1, 1)
        self.carDetectionTitle = QtWidgets.QLabel(self.centralwidget)
        self.carDetectionTitle.setObjectName("carDetectionTitle")
        self.gridLayout.addWidget(self.carDetectionTitle, 12, 0, 1, 1)
        self.cameraSelection = QtWidgets.QComboBox(self.centralwidget)
        self.cameraSelection.setObjectName("cameraSelection")
        self.gridLayout.addWidget(self.cameraSelection, 6, 1, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1250, 21))
        self.menubar.setObjectName("menubar")
        self.menuSettings = QtWidgets.QMenu(self.menubar)
        self.menuSettings.setObjectName("menuSettings")
        MainWindow.setMenuBar(self.menubar)
        self.actionShow_Options = QtWidgets.QAction(MainWindow)
        self.actionShow_Options.setObjectName("actionShow_Options")
        self.actionHide_Options = QtWidgets.QAction(MainWindow)
        self.actionHide_Options.setObjectName("actionHide_Options")
        self.menuSettings.addAction(self.actionShow_Options)
        self.menuSettings.addAction(self.actionHide_Options)
        self.menubar.addAction(self.menuSettings.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.cameraTitle.setText(_translate("MainWindow", "Camera"))
        self.simulationTitle.setText(_translate("MainWindow", "Simulation Runner"))
        self.lidarTitle.setText(_translate("MainWindow", "Lidar"))
        self.lidarGetVelocityButton.setText(_translate("MainWindow", "Get Velocity"))
        self.lidarGetDistanceButton.setText(_translate("MainWindow", "Get Distance"))
        self.lidarStreamVelocity.setText(_translate("MainWindow", "Stream Velocity"))
        self.lidarSetupButton.setText(_translate("MainWindow", "Setup Lidar"))
        self.lidarStreamDistance.setText(_translate("MainWindow", "Stream Distance"))
        self.simulationSelectFolder.setText(_translate("MainWindow", "Select Simulation Folder"))
        self.simulationRunSimulation.setText(_translate("MainWindow", "Run Simulation"))
        self.lidarEnableCheckBox.setText(_translate("MainWindow", "Enable Lidar"))
        self.simulationStartSavingNew.setText(_translate("MainWindow", "Start Saving New Simulation"))
        self.carDetectionEnableCheckBox.setText(_translate("MainWindow", "Enable Car Detection"))
        self.cameraEnableCheckBox.setText(_translate("MainWindow", "Enable Camera Stream"))
        self.carDetectionTitle.setText(_translate("MainWindow", "Car Detection"))
        self.menuSettings.setTitle(_translate("MainWindow", "Settings"))
        self.actionShow_Options.setText(_translate("MainWindow", "Show Options"))
        self.actionHide_Options.setText(_translate("MainWindow", "Hide Options"))


