from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout, QMainWindow, QDesktopWidget, QStatusBar, \
    QFileDialog
from PyQt5.QtGui import QPixmap
import cv2
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread, QTimer
import numpy as np


class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)
    change_video_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self.video_change = False
        self.video_path = ""
        self.rec_vid = False

    def run(self):
        self.video_change = False
        self.rec_vid = False
        self.cap = cv2.VideoCapture(self.video_path)
        self.frame_width = int(self.cap.get(3))
        self.frame_height = int(self.cap.get(4))
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.out_RGB = cv2.VideoWriter('output_RGB.avi', self.fourcc, self.fps,
                                  (self.frame_width, self.frame_height))
        self.out_Gray = cv2.VideoWriter('output_GRAY.avi', self.fourcc, self.fps, (self.frame_width,self.frame_height),0)

        while self.cap.isOpened():
            ret, cv_img = self.cap.read()
            self.usleep(int(1000000 / self.fps))
            if ret:
                if not self.video_change:
                    self.change_pixmap_signal.emit(cv_img)

                if self.video_change:
                    self.change_video_signal.emit(cv_img)

        # shut down capture system
        self.cap.release()

    def vid_change_True(self):
        self.video_change = True

    def vid_change_False(self):
        self.video_change = False

    def rec_vid_True(self):
        self.rec_vid = True

    def rec_vid_False(self):
        self.rec_vid = False


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        self.thread = VideoThread()
        Form.resize(940, 580)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.gridLayout_5 = QtWidgets.QGridLayout()
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.groupBox_main = QtWidgets.QGroupBox(Form)
        self.groupBox_main.setMinimumSize(QtCore.QSize(0, 480))
        self.groupBox_main.setTitle("")
        self.groupBox_main.setObjectName("groupBox_main")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox_main)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(-1, -1, -1, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEdit_open = QtWidgets.QLineEdit(self.groupBox_main)
        self.lineEdit_open.setObjectName("lineEdit_open")
        self.horizontalLayout.addWidget(self.lineEdit_open)
        self.btn_open = QtWidgets.QPushButton(self.groupBox_main)
        self.btn_open.setObjectName("btn_open")
        self.btn_open.clicked.connect(self.onClicked_open_file)

        self.horizontalLayout.addWidget(self.btn_open)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.comboBox = QtWidgets.QComboBox(self.groupBox_main)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("select")
        self.comboBox.addItem("tracking 1")
        self.comboBox.addItem("tracking 2")
        self.comboBox.addItem("Convert to Gray")
        self.comboBox.addItem("Record Video")
        self.comboBox.activated[str].connect(self.onClicked_groupBox)

        self.verticalLayout.addWidget(self.comboBox)
        self.groupBox_1 = QtWidgets.QGroupBox(self.groupBox_main)
        self.groupBox_1.setMinimumSize(QtCore.QSize(0, 150))
        self.groupBox_1.setObjectName("groupBox_1")
        self.groupBox_1.setVisible(False)

        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox_1)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.btn_1_1 = QtWidgets.QPushButton(self.groupBox_1)
        self.btn_1_1.setObjectName("btn_1_1")
        self.gridLayout.addWidget(self.btn_1_1, 0, 2, 1, 1)
        self.lineEdit_1_1 = QtWidgets.QLineEdit(self.groupBox_1)
        self.lineEdit_1_1.setObjectName("lineEdit_1_1")
        self.gridLayout.addWidget(self.lineEdit_1_1, 0, 0, 1, 1)
        self.btn_1_2 = QtWidgets.QPushButton(self.groupBox_1)
        self.btn_1_2.setObjectName("btn_1_2")
        self.gridLayout.addWidget(self.btn_1_2, 1, 2, 1, 1)
        self.lineEdit_1_2 = QtWidgets.QLineEdit(self.groupBox_1)
        self.lineEdit_1_2.setObjectName("lineEdit_1_2")
        self.gridLayout.addWidget(self.lineEdit_1_2, 1, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 1, 1, 1)
        self.verticalLayout_4.addLayout(self.gridLayout)
        self.verticalLayout.addWidget(self.groupBox_1)
        self.groupBox_2 = QtWidgets.QGroupBox(self.groupBox_main)
        self.groupBox_2.setMinimumSize(QtCore.QSize(0, 150))
        self.groupBox_2.setObjectName("groupBox_2")
        self.groupBox_2.setVisible(False)

        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.btn_2_1 = QtWidgets.QPushButton(self.groupBox_2)
        self.btn_2_1.setObjectName("btn_2_1")
        self.gridLayout_2.addWidget(self.btn_2_1, 0, 2, 1, 1)
        self.lineEdit_2_1 = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_2_1.setObjectName("lineEdit_2_1")
        self.gridLayout_2.addWidget(self.lineEdit_2_1, 0, 0, 1, 1)
        self.btn_2_2 = QtWidgets.QPushButton(self.groupBox_2)
        self.btn_2_2.setObjectName("btn_2_2")
        self.gridLayout_2.addWidget(self.btn_2_2, 1, 2, 1, 1)
        self.lineEdit_2_2 = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_2_2.setObjectName("lineEdit_2_2")
        self.gridLayout_2.addWidget(self.lineEdit_2_2, 1, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem2, 0, 1, 1, 1)
        self.verticalLayout_5.addLayout(self.gridLayout_2)
        self.verticalLayout.addWidget(self.groupBox_2)
        self.groupBox_3 = QtWidgets.QGroupBox(self.groupBox_main)
        self.groupBox_3.setObjectName("groupBox_3")
        self.groupBox_3.setVisible(False)

        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.checkBox = QtWidgets.QCheckBox(self.groupBox_3)
        self.checkBox.setObjectName("checkBox")
        self.verticalLayout_6.addWidget(self.checkBox)
        self.verticalLayout.addWidget(self.groupBox_3)
        self.groupBox_4 = QtWidgets.QGroupBox(self.groupBox_main)
        self.groupBox_4.setObjectName("groupBox_4")
        self.groupBox_4.setVisible(False)

        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.groupBox_4)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.checkBox_rec = QtWidgets.QCheckBox(self.groupBox_4)
        self.checkBox_rec.setObjectName("checkBox_rec")


        self.verticalLayout_7.addWidget(self.checkBox_rec)
        self.lineEdit_rec = QtWidgets.QLineEdit(self.groupBox_4)
        self.lineEdit_rec.setText("")
        self.lineEdit_rec.setPlaceholderText("")
        self.lineEdit_rec.setObjectName("lineEdit_rec")
        self.verticalLayout_7.addWidget(self.lineEdit_rec)
        self.verticalLayout.addWidget(self.groupBox_4)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem3)
        self.gridLayout_7 = QtWidgets.QGridLayout()
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem4)
        self.btn_start = QtWidgets.QPushButton(self.groupBox_main)
        self.btn_start.setObjectName("btn_start")
        self.btn_start.clicked.connect(self.ClickStartVideo)


        self.horizontalLayout_2.addWidget(self.btn_start)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem5)
        self.btn_stop = QtWidgets.QPushButton(self.groupBox_main)
        self.btn_stop.setObjectName("btn_stop")
        self.btn_stop.clicked.connect(self.set_checkBox_False)
        self.btn_stop.clicked.connect(self.set_checkBoc_rec_False)
        self.btn_stop.clicked.connect(self.set_btn_stop_True)



        self.horizontalLayout_2.addWidget(self.btn_stop)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem6)
        self.gridLayout_7.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_7)
        self.verticalLayout_3.addLayout(self.verticalLayout)
        self.gridLayout_5.addWidget(self.groupBox_main, 0, 2, 1, 1)
        self.label = QtWidgets.QLabel(Form)
        self.label.setMinimumSize(QtCore.QSize(640, 480))
        self.label.setFrameShape(QtWidgets.QLabel.Box)
        self.label.setFrameShadow(QtWidgets.QLabel.Raised)
        self.label.setObjectName("label")
        self.gridLayout_5.addWidget(self.label, 0, 0, 1, 1)
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_5.addItem(spacerItem7, 0, 1, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout_5)
        spacerItem8 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem8)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def check(self):
        self.checkBox.isChecked()
        if self.checkBox.isChecked():
            self.thread.change_video_signal.connect(self.update_image_GRAY)
            self.thread.start()
            self.thread.vid_change_True()
        if not self.checkBox.isChecked():
            self.thread.change_video_signal.disconnect(self.update_image_GRAY)
            self.thread.vid_change_False()
    def check_rec(self):
        self.checkBox_rec.isChecked()
        self.checkBox.isChecked()
        if self.checkBox_rec.isChecked() and self.checkBox.isChecked():
            self.btn_start.setEnabled(False)
            self.btn_start.clicked.connect(self.ClickStartVideo)
            self.thread.change_video_signal.disconnect(self.update_image_GRAY)
            self.thread.rec_vid_True()
            self.thread.change_video_signal.connect(self.update_image_GRAY)
            self.thread.start()
            self.thread.vid_change_True()
            self.btn_start.clicked.disconnect(self.ClickStartVideo)
        elif not self.checkBox_rec.isChecked() and self.checkBox.isChecked():
            self.btn_start.setEnabled(False)
            self.btn_start.clicked.connect(self.ClickStartVideo)
            self.thread.change_video_signal.connect(self.update_image)
            self.thread.rec_vid_False()
            self.thread.change_video_signal.disconnect(self.update_image)
            self.btn_start.clicked.disconnect(self.ClickStartVideo)



    def set_btn_stop_True(self):
        self.btn_start.setEnabled(True)
    def set_checkBox_False(self):
        self.checkBox.setChecked(False)
    def set_checkBoc_rec_False(self):
        self.checkBox_rec.setChecked(False)

    def ClickStartVideo(self):
        self.checkBox.stateChanged.connect(self.check)
        if not self.checkBox.isChecked():
            self.btn_start.clicked.disconnect(self.ClickStartVideo)
            self.btn_start.setText('Stoped')
            self.thread.change_pixmap_signal.connect(self.update_image)
            self.thread.start()
            self.btn_start.clicked.connect(self.ClickStopVideo)
            self.thread.vid_change_False()

    def ClickStopVideo(self):

        if not self.checkBox.isChecked():
            self.thread.change_pixmap_signal.disconnect(self.update_image)
            self.btn_start.setText('Start')
            self.btn_start.clicked.disconnect(self.ClickStopVideo)
            self.btn_start.clicked.connect(self.ClickStartVideo)

    def update_image(self, cv_img):
        qt_img = self.convert_cv_qt(cv_img)
        self.label.setPixmap(qt_img)

    def convert_cv_qt(self, cv_img):
        self.checkBox_rec.stateChanged.connect(self.check_rec)
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(640, 480, Qt.KeepAspectRatio)
        if self.checkBox_rec.isChecked():
            out_RGB = self.thread.out_RGB
            out_RGB.write(cv_img)

        return QPixmap.fromImage(p)

    ######################### RGB to GRAY ####################

    def update_image_GRAY(self, cv_img):
        qt_img = self.convert_BGR_GRAY(cv_img)
        self.label.setPixmap(qt_img)

    def convert_BGR_GRAY(self, cv_img):
        self.checkBox_rec.stateChanged.connect(self.check_rec)
        gray_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
        h, w = gray_image.shape
        convert_to_Qt_format = QtGui.QImage(gray_image.data, w, h, QtGui.QImage.Format_Grayscale8)
        p = convert_to_Qt_format.scaled(640, 480, Qt.KeepAspectRatio)
        if self.checkBox_rec.isChecked():
            out_Gray = self.thread.out_Gray
            out_Gray.write(gray_image)
        return QPixmap.fromImage(p)

    ######################### RGB to GRAY ####################

    def onClicked_open_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fname = QFileDialog.getOpenFileName(None, 'Open Video', '', 'All Files (*)', options=options)
        self.lineEdit_open.setText(fname[0])
        self.thread.video_path = self.lineEdit_open.text()

    def onClicked_groupBox(self, choice):
        if choice == "select":
            self.groupBox_1.setVisible(False)
            self.groupBox_2.setVisible(False)
            self.groupBox_3.setVisible(False)
            self.groupBox_4.setVisible(False)
        elif choice == "tracking 1":
            self.groupBox_1.setVisible(True)
            self.groupBox_2.setVisible(False)
            self.groupBox_3.setVisible(False)
        elif choice == "tracking 2":
            self.groupBox_1.setVisible(False)
            self.groupBox_2.setVisible(True)
            self.groupBox_3.setVisible(False)
        elif choice == "Convert to Gray":
            self.groupBox_1.setVisible(False)
            self.groupBox_2.setVisible(False)
            self.groupBox_3.setVisible(True)
        elif choice == "Record Video":
            self.groupBox_1.setVisible(False)
            self.groupBox_2.setVisible(False)
            self.groupBox_4.setVisible(True)

        else:
            print("error")

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.btn_open.setText(_translate("Form", "OPEN"))
        self.groupBox_1.setTitle(_translate("Form", "1"))
        self.btn_1_1.setText(_translate("Form", "SET"))
        self.btn_1_2.setText(_translate("Form", "SET"))
        self.groupBox_2.setTitle(_translate("Form", "2"))
        self.btn_2_1.setText(_translate("Form", "SET"))
        self.btn_2_2.setText(_translate("Form", "SET"))
        self.groupBox_3.setTitle(_translate("Form", "Convert RGB TO GRAY"))
        self.checkBox.setText(_translate("Form", "RGB to Gray"))
        self.groupBox_4.setTitle(_translate("Form", "Record Video"))
        self.checkBox_rec.setText(_translate("Form", "Record"))
        self.btn_start.setText(_translate("Form", "Start"))
        self.btn_stop.setText(_translate("Form", "Stop Events"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

