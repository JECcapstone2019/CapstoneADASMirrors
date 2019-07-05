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
        MainWindow.resize(1015, 659)
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
        self.imageViewer = QtWidgets.QLabel(self.centralwidget)
        self.imageViewer.setMinimumSize(QtCore.QSize(0, 0))
        self.imageViewer.setAutoFillBackground(False)
        self.imageViewer.setText("")
        self.imageViewer.setObjectName("imageViewer")
        self.horizontalLayout.addWidget(self.imageViewer)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.cameraEnableCheckBox = QtWidgets.QCheckBox(self.centralwidget)
        self.cameraEnableCheckBox.setObjectName("cameraEnableCheckBox")
        self.gridLayout.addWidget(self.cameraEnableCheckBox, 6, 0, 1, 1)
        self.cameraSelection = QtWidgets.QComboBox(self.centralwidget)
        self.cameraSelection.setObjectName("cameraSelection")
        self.gridLayout.addWidget(self.cameraSelection, 7, 0, 1, 1)
        self.line_10 = QtWidgets.QFrame(self.centralwidget)
        self.line_10.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_10.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_10.setObjectName("line_10")
        self.gridLayout.addWidget(self.line_10, 16, 2, 1, 1)
        self.line_9 = QtWidgets.QFrame(self.centralwidget)
        self.line_9.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_9.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_9.setObjectName("line_9")
        self.gridLayout.addWidget(self.line_9, 16, 0, 1, 1)
        self.carDetectionTitle = QtWidgets.QLabel(self.centralwidget)
        self.carDetectionTitle.setObjectName("carDetectionTitle")
        self.gridLayout.addWidget(self.carDetectionTitle, 8, 0, 1, 1)
        self.imageViewerTitle = QtWidgets.QLabel(self.centralwidget)
        self.imageViewerTitle.setObjectName("imageViewerTitle")
        self.gridLayout.addWidget(self.imageViewerTitle, 12, 0, 1, 1)
        self.imageViewerLabel = QtWidgets.QLabel(self.centralwidget)
        self.imageViewerLabel.setObjectName("imageViewerLabel")
        self.gridLayout.addWidget(self.imageViewerLabel, 14, 0, 1, 1)
        self.carDetectionSelection = QtWidgets.QComboBox(self.centralwidget)
        self.carDetectionSelection.setObjectName("carDetectionSelection")
        self.gridLayout.addWidget(self.carDetectionSelection, 11, 0, 1, 1)
        self.cameraTitle = QtWidgets.QLabel(self.centralwidget)
        self.cameraTitle.setObjectName("cameraTitle")
        self.gridLayout.addWidget(self.cameraTitle, 4, 0, 1, 1)
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridLayout.addWidget(self.line_2, 5, 0, 1, 1)
        self.imageViewerTextEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.imageViewerTextEdit.setEnabled(False)
        self.imageViewerTextEdit.setObjectName("imageViewerTextEdit")
        self.gridLayout.addWidget(self.imageViewerTextEdit, 14, 1, 1, 1)
        self.lidarSelection = QtWidgets.QComboBox(self.centralwidget)
        self.lidarSelection.setObjectName("lidarSelection")
        self.gridLayout.addWidget(self.lidarSelection, 3, 0, 1, 1)
        self.carDetectionEnableCheckBox = QtWidgets.QCheckBox(self.centralwidget)
        self.carDetectionEnableCheckBox.setObjectName("carDetectionEnableCheckBox")
        self.gridLayout.addWidget(self.carDetectionEnableCheckBox, 10, 0, 1, 1)
        self.lidarTitle = QtWidgets.QLabel(self.centralwidget)
        self.lidarTitle.setObjectName("lidarTitle")
        self.gridLayout.addWidget(self.lidarTitle, 0, 0, 1, 1)
        self.lidarEnableCheckBox = QtWidgets.QCheckBox(self.centralwidget)
        self.lidarEnableCheckBox.setObjectName("lidarEnableCheckBox")
        self.gridLayout.addWidget(self.lidarEnableCheckBox, 2, 0, 1, 1)
        self.line_7 = QtWidgets.QFrame(self.centralwidget)
        self.line_7.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_7.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_7.setObjectName("line_7")
        self.gridLayout.addWidget(self.line_7, 1, 1, 1, 1)
        self.lidarCheckProcessButton = QtWidgets.QPushButton(self.centralwidget)
        self.lidarCheckProcessButton.setObjectName("lidarCheckProcessButton")
        self.gridLayout.addWidget(self.lidarCheckProcessButton, 2, 1, 1, 1)
        self.lidarTextEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.lidarTextEdit.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lidarTextEdit.sizePolicy().hasHeightForWidth())
        self.lidarTextEdit.setSizePolicy(sizePolicy)
        self.lidarTextEdit.setObjectName("lidarTextEdit")
        self.gridLayout.addWidget(self.lidarTextEdit, 3, 1, 1, 1)
        self.line_6 = QtWidgets.QFrame(self.centralwidget)
        self.line_6.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_6.setObjectName("line_6")
        self.gridLayout.addWidget(self.line_6, 5, 1, 1, 1)
        self.simulationTitle = QtWidgets.QLabel(self.centralwidget)
        self.simulationTitle.setObjectName("simulationTitle")
        self.gridLayout.addWidget(self.simulationTitle, 15, 0, 1, 1)
        self.line_4 = QtWidgets.QFrame(self.centralwidget)
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.gridLayout.addWidget(self.line_4, 13, 0, 1, 1)
        self.line_8 = QtWidgets.QFrame(self.centralwidget)
        self.line_8.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_8.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_8.setObjectName("line_8")
        self.gridLayout.addWidget(self.line_8, 13, 1, 1, 1)
        self.line_3 = QtWidgets.QFrame(self.centralwidget)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.gridLayout.addWidget(self.line_3, 9, 0, 1, 1)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 1, 0, 1, 1)
        self.line_5 = QtWidgets.QFrame(self.centralwidget)
        self.line_5.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.gridLayout.addWidget(self.line_5, 9, 1, 1, 1)
        self.cameraCheckProcessButton = QtWidgets.QPushButton(self.centralwidget)
        self.cameraCheckProcessButton.setObjectName("cameraCheckProcessButton")
        self.gridLayout.addWidget(self.cameraCheckProcessButton, 6, 1, 1, 1)
        self.simulationRunSimulation = QtWidgets.QCheckBox(self.centralwidget)
        self.simulationRunSimulation.setEnabled(False)
        self.simulationRunSimulation.setObjectName("simulationRunSimulation")
        self.gridLayout.addWidget(self.simulationRunSimulation, 17, 0, 1, 1)
        self.carDetectionTextEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.carDetectionTextEdit.setEnabled(False)
        self.carDetectionTextEdit.setObjectName("carDetectionTextEdit")
        self.gridLayout.addWidget(self.carDetectionTextEdit, 11, 1, 1, 1)
        self.cameraTextEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.cameraTextEdit.setEnabled(False)
        self.cameraTextEdit.setObjectName("cameraTextEdit")
        self.gridLayout.addWidget(self.cameraTextEdit, 7, 1, 1, 1)
        self.line_11 = QtWidgets.QFrame(self.centralwidget)
        self.line_11.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_11.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_11.setObjectName("line_11")
        self.gridLayout.addWidget(self.line_11, 16, 1, 1, 1)
        self.carDetectionCheckProcessButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.carDetectionCheckProcessButton_2.setObjectName("carDetectionCheckProcessButton_2")
        self.gridLayout.addWidget(self.carDetectionCheckProcessButton_2, 10, 1, 1, 1)
        self.simulationSelectFolder = QtWidgets.QPushButton(self.centralwidget)
        self.simulationSelectFolder.setObjectName("simulationSelectFolder")
        self.gridLayout.addWidget(self.simulationSelectFolder, 18, 0, 1, 1)
        self.simulationFolderSelectedTextEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.simulationFolderSelectedTextEdit.setEnabled(True)
        self.simulationFolderSelectedTextEdit.setObjectName("simulationFolderSelectedTextEdit")
        self.gridLayout.addWidget(self.simulationFolderSelectedTextEdit, 18, 1, 1, 1)
        self.simulationTextEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.simulationTextEdit.setEnabled(False)
        self.simulationTextEdit.setObjectName("simulationTextEdit")
        self.gridLayout.addWidget(self.simulationTextEdit, 17, 1, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1015, 21))
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
        self.cameraEnableCheckBox.setText(_translate("MainWindow", "Enable Camera Stream"))
        self.carDetectionTitle.setText(_translate("MainWindow", "Car Detection"))
        self.imageViewerTitle.setText(_translate("MainWindow", "Image Viewer Thread"))
        self.imageViewerLabel.setText(_translate("MainWindow", "Thread Messages"))
        self.cameraTitle.setText(_translate("MainWindow", "Camera"))
        self.carDetectionEnableCheckBox.setText(_translate("MainWindow", "Enable Car Detection"))
        self.lidarTitle.setText(_translate("MainWindow", "Lidar"))
        self.lidarEnableCheckBox.setText(_translate("MainWindow", "Enable Lidar"))
        self.lidarCheckProcessButton.setText(_translate("MainWindow", "Check Process Is Alive"))
        self.simulationTitle.setText(_translate("MainWindow", "Simulation Runner"))
        self.cameraCheckProcessButton.setText(_translate("MainWindow", "Check Process Is Alive"))
        self.simulationRunSimulation.setText(_translate("MainWindow", "Run Simulation"))
        self.carDetectionCheckProcessButton_2.setText(_translate("MainWindow", "Check Process Is Alive"))
        self.simulationSelectFolder.setText(_translate("MainWindow", "Select Simulation Folder"))
        self.menuSettings.setTitle(_translate("MainWindow", "Settings"))
        self.actionShow_Options.setText(_translate("MainWindow", "Show Options"))
        self.actionHide_Options.setText(_translate("MainWindow", "Hide Options"))


