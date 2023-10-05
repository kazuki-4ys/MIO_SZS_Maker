from MIO_SZS_Maker_core import *
from tpl_encoder import *
from PyQt6 import QtCore, QtWidgets
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QTabWidget, QHBoxLayout, QVBoxLayout
from PyQt6.QtGui import QPixmap
import ctypes
import time
import locale

class ResultWindow(QtWidgets.QWidget):
    def __init__(self):
        super(ResultWindow, self).__init__()
        self.isLangJPN = False
        try:
            if "JAPAN" in locale.getlocale()[0].upper():
                self.isLangJPN = True
                pass
        except:
            pass
        self.setWindowTitle("result")
        self.setGeometry(300, 50, 300, 300)
        self.setFixedWidth(300)
        self.setFixedHeight(300)
        self.line1Label = QtWidgets.QLabel("", self)
        self.line1Label.setGeometry(10, 10, 300, 20)
        self.line2Label = QtWidgets.QLabel("", self)
        self.line2Label.setGeometry(10, 30, 300, 20)
        self.errMsgDisplay = QtWidgets.QTextEdit(self)
        self.errMsgDisplay.setReadOnly(True)
        self.errMsgDisplay.setGeometry(10, 50, 280, 230)
    def setResult(self, errMsg, proc):
        if len(errMsg) == 0:
            if self.isLangJPN:
                self.line1Label.setText("szsの作成が正常に完了しました")
                self.errMsgDisplay.setText("エラーはありません")
            else:
                self.line1Label.setText("")
                self.errMsgDisplay.setText("No error has occurred.")
        else:
            if self.isLangJPN:
                self.line1Label.setText("エラーが発生しました")
                self.line2Label.setText("現在の処理: " + proc)
            else:
                self.line1Label.setText("An error has occurred.")
                self.line2Label.setText("Current process: " + proc)
            self.errMsgDisplay.setText(errMsg)


class Tab2Widget(QTabWidget):
    def __init__(self, mainWindow):
        super(Tab2Widget, self).__init__()
        self.mainWindow = mainWindow
        self.isLangJPN = False
        self.isFirstOpen = True
        try:
            if "JAPAN" in locale.getlocale()[0].upper():
                self.isLangJPN = True
                #pass
        except:
            pass
        self.Tab2InitUI()
        self.isIconDelete = True
        self.srcImagePath = ""
        self.srcSzsDir = ""
        self.destSzsDir = ""
        self.tplEncodeSetting = TPLEncodeSetting()
        self.resizeSetting = (256, 256)
        self.useResize = False
    def srcSzsDirButtonPushed(self):
        tmpPath = ""
        if self.isLangJPN:
            tmpPath = self.selectFolderDialog("ベースになるszsのフォルダを選択")
        else:
            tmpPath = self.selectFolderDialog("select base szs directory")
        if len(tmpPath) == 0:
            return
        if tmpPath == self.destSzsDir:
            self.showSrcDestSameMessage()
            return
        self.srcSzsDir = tmpPath
        self.srcSzsDirLineEdit.setText(self.srcSzsDir)
    def destSzsDirButtonPushed(self):
        tmpPath = ""
        if self.isLangJPN:
            tmpPath = self.selectFolderDialog("szsの保存先フォルダを選択")
        else:
            tmpPath = self.selectFolderDialog("select output szs directory")
        if len(tmpPath) == 0:
            return
        if tmpPath == self.srcSzsDir:
            self.showSrcDestSameMessage()
            return
        if len(os.listdir(tmpPath)) != 0:
            if self.showDestNotEmptyMessage() == False:
                return
        self.destSzsDir = tmpPath
        self.destSzsDirLineEdit.setText(self.destSzsDir)
    def miiIDLineEditEditingFinished(self):
        miiIdLineTmpText = self.miiIDLineEdit.text()
        miiIDTmp = self.stoh(miiIdLineTmpText)
        if miiIDTmp > -1:
            self.miiID = miiIDTmp & 0xFFFFFFFF
        self.miiIDLineEdit.setText("%08x" % (self.miiID))
    def selectFolderDialog(self, title):
        initialDir = ""
        if self.isFirstOpen:
            initialDir = System.getThisScriptDir()
            self.isFirstOpen = False
        return QtWidgets.QFileDialog.getExistingDirectory(self, title, "")
    def openFileDialog(self, title, filter):
        initialDir = ""
        if self.isFirstOpen:
            initialDir = System.getThisScriptDir()
            self.isFirstOpen = False
        path, _ = QtWidgets.QFileDialog.getOpenFileName(self, title, "", filter)
        return path
    def Tab2InitUI(self):
        self.line1Label = QtWidgets.QLabel("base szs directory:", self)
        self.line1Label.setGeometry(10, 10, 350, 20)
        self.srcSzsDirButton = QtWidgets.QPushButton("...", self)
        self.srcSzsDirButton.clicked.connect(self.srcSzsDirButtonPushed)
        self.srcSzsDirButton.setGeometry(600, 10, 50, 20)
        self.srcSzsDirLineEdit = QtWidgets.QLineEdit("", self)
        self.srcSzsDirLineEdit.setGeometry(190, 10, 400, 20)
        self.srcSzsDirLineEdit.setReadOnly(True)
        self.line2Label = QtWidgets.QLabel("Mii ID to delete (8digits, hex):", self)
        self.line2Label.setGeometry(10, 50, 300, 20)
        self.miiIDLineEdit = QtWidgets.QLineEdit("", self)
        self.miiIDLineEdit.setGeometry(170, 50, 110, 20)
        self.miiIDLineEdit.setText("851d56e2")
        self.miiIDLineEdit.editingFinished.connect(self.miiIDLineEditEditingFinished)
        self.miiID = 0x851d56e2
        self.line7Label = QtWidgets.QLabel("output szs directory:", self)
        self.line7Label.setGeometry(10, 220, 350, 20)
        self.destSzsDirButton = QtWidgets.QPushButton("...", self)
        self.destSzsDirButton.clicked.connect(self.destSzsDirButtonPushed)
        self.destSzsDirButton.setGeometry(600, 220, 50, 20)
        self.destSzsDirLineEdit = QtWidgets.QLineEdit("", self)
        self.destSzsDirLineEdit.setGeometry(190, 220, 400, 20)
        self.destSzsDirLineEdit.setReadOnly(True)
        self.szsMakeButton = QtWidgets.QPushButton("Make SZS!!", self)
        self.szsMakeButton.setGeometry(200, 280, 300, 50)
        self.szsMakeButton.clicked.connect(self.szsMakeButtonPushed)
        if self.isLangJPN:
            self.line1Label.setText("ベースになるszsのフォルダ:")
            self.line2Label.setText("削除するMii ID (8桁16進数):")
            self.line7Label.setText("szsの保存先フォルダ:")
            self.szsMakeButton.setText("SZSを作成")
    def disableAllUI(self):
        self.srcSzsDirButton.setEnabled(False)
        self.srcSzsDirLineEdit.setEnabled(False)
        self.miiIDLineEdit.setEnabled(False)
        self.destSzsDirButton.setEnabled(False)
        self.destSzsDirLineEdit.setEnabled(False)
        self.szsMakeButton.setEnabled(False)
    def enableAllUI(self):
        self.srcSzsDirButton.setEnabled(True)
        self.srcSzsDirLineEdit.setEnabled(True)
        self.miiIDLineEdit.setEnabled(True)
        self.destSzsDirButton.setEnabled(True)
        self.destSzsDirLineEdit.setEnabled(True)
        self.szsMakeButton.setEnabled(True)
        if self.isLangJPN:
            self.szsMakeButton.setText("SZSを作成")
        else:
            self.szsMakeButton.setText("Make SZS!!")
    def szsMakeButtonPushed(self):
        self.isIconDelete = True
        if len(self.srcSzsDir) == 0:
            if self.isLangJPN:
                QtWidgets.QMessageBox.information(None, "MIO SZS Maker", "ベースとなるszsのフォルダが選択されてません。", QtWidgets.QMessageBox.StandardButton.Yes)
            else:
                QtWidgets.QMessageBox.information(None, "MIO SZS Maker", "base szs directory is not selected", QtWidgets.QMessageBox.StandardButton.Yes)
            return
        if len(self.destSzsDir) == 0:
            if self.isLangJPN:
                QtWidgets.QMessageBox.information(None, "MIO SZS Maker", "szsの保存先フォルダが選択されてません。", QtWidgets.QMessageBox.StandardButton.Yes)
            else:
                QtWidgets.QMessageBox.information(None, "MIO SZS Maker", "output szs directory is not selected", QtWidgets.QMessageBox.StandardButton.Yes)
            return
        self.mainWindow.makeSzs(self)
    def setCurTaskDisplay(self, proc):
        self.szsMakeButton.setText(proc)
    def showSrcDestSameMessage(self):
        if self.isLangJPN:
            QtWidgets.QMessageBox.information(None, "MIO SZS Maker", "ベースとなるszsのフォルダとszsの保存先フォルダを同じにすることはできません。", QtWidgets.QMessageBox.StandardButton.Yes)
        else:
            QtWidgets.QMessageBox.information(None, "MIO SZS Maker", "base szs directory is same as output szs directory.", QtWidgets.QMessageBox.StandardButton.Yes)
    def showDestNotEmptyMessage(self):
        result = False
        msgBoxResult = None
        if self.isLangJPN:
            msgBoxResult = QtWidgets.QMessageBox.information(None, "MIO SZS Maker", "保存先szsフォルダが空ではありません。保存先フォルダの中身を全て削除してもよろしいですか?", QtWidgets.QMessageBox.StandardButton.Yes, QtWidgets.QMessageBox.StandardButton.No)
        else:
            msgBoxResult = QtWidgets.QMessageBox.information(None, "MIO SZS Maker", "This folder is not empty!!\nAre you sure you want to delete the contents of this folder completely?", QtWidgets.QMessageBox.StandardButton.Yes, QtWidgets.QMessageBox.StandardButton.No)
        if msgBoxResult == QtWidgets.QMessageBox.StandardButton.Yes:
            result = True
        return result
    #文字列を10進数に変換
    def ston(self, a):
        string = a.replace(" ", "").replace("　", "")
        dec = 0
        num = 0
        for i in range(len(string)):
            dec = self.getDec(string[i])
            if dec == -1:
                return -1
            num = num * 10 + dec
        return num
    def getDec(self, char):
        if char == "0" or char == "０":
            return 0
        elif char == "1" or char == "１":
            return 1
        elif char == "2" or char == "２":
            return 2
        elif char == "3" or char == "３":
            return 3
        elif char == "4" or char == "４":
            return 4
        elif char == "5" or char == "５":
            return 5
        elif char == "6" or char == "６":
            return 6
        elif char == "7" or char == "７":
            return 7
        elif char == "8" or char == "８":
            return 8
        elif char == "9" or char == "９":
            return 9
        return  -1
    #文字列を16進数に変換
    def stoh(self, a):
        string = a.replace(" ", "").replace("　", "").replace("-", "").replace("ー", "")
        hex = 0
        num = 0
        for i in range(len(string)):
            hex = self.getHex(string[i])
            if (hex == -1):
                return -1
            num = num * 16 + hex
        return num

    def getHex(self, char):
        if char == "0" or char == "０":
            return 0
        elif char == "1" or char == "１":
            return 1
        elif char == "2" or char == "２":
            return 2
        elif char == "3" or char == "３":
            return 3
        elif char == "4" or char == "４":
            return 4
        elif char == "5" or char == "５":
            return 5
        elif char == "6" or char == "６":
            return 6
        elif char == "7" or char == "７":
            return 7
        elif char == "8" or char == "８":
            return 8
        elif char == "9" or char == "９":
            return 9
        elif char == "A" or char == "Ａ" or char == "a" or char == "ａ":
            return 10
        elif char == "B" or char == "Ｂ" or char == "b" or char == "ｂ":
            return 11
        elif char == "C" or char == "Ｃ" or char == "c" or char == "ｃ":
            return 12
        elif char == "D" or char == "Ｄ" or char == "d" or char == "ｄ":
            return 13
        elif char == "E" or char == "Ｅ" or char == "e" or char == "ｅ":
            return 14
        elif char == "F" or char == "Ｆ" or char == "f" or char == "ｆ":
            return 15
        return  -1

 
class Tab1Widget(Tab2Widget):
    def __init__(self, mainWindow):
        super(Tab1Widget, self).__init__(mainWindow)
        self.isIconDelete = False
        self.line2Label.setGeometry(10, 50, 300, 20)
        self.line2Label.setText("Mii ID to add (8digits, hex):")
        self.line3Label = QtWidgets.QLabel("image icon to add:", self)
        self.line3Label.setGeometry(300, 50, 300, 20)
        self.addImageView = QtWidgets.QLabel(self)
        self.addImageView.setGeometry(420, 55, 100, 100)
        self.addImageButton = QtWidgets.QPushButton("select", self)
        self.addImageButton.setGeometry(360, 130, 50, 20)
        self.addImageButton.clicked.connect(self.selectAddImage)
        self.line4Label = QtWidgets.QLabel("tpl encode setting:", self)
        self.line4Label.setGeometry(10, 160, 300, 20)
        self.line5Label = QtWidgets.QLabel("resize image", self)
        self.line5Label.setGeometry(30, 180, 300, 20)
        self.imageResizeCheckbox = QtWidgets.QCheckBox(self)
        self.imageResizeCheckbox.move(120, 185)
        self.imageResizeCheckbox.clicked.connect(self.imageResizeCheckboxPushed)
        self.imageResizeCheckbox.setChecked(True)
        self.imageResizeWidthLineEdit = QtWidgets.QLineEdit("256", self)
        self.imageResizeWidthLineEdit.setGeometry(210, 180, 50, 20)
        self.imageResizeWidthLineEdit.editingFinished.connect(self.imageResizeWidthLineEditEditingFinished)
        self.line6Label = QtWidgets.QLabel("x", self)
        self.line6Label.setGeometry(270, 180, 20, 20)
        self.imageResizeHeightLineEdit = QtWidgets.QLineEdit("256", self)
        self.imageResizeHeightLineEdit.setGeometry(300, 180, 50, 20)
        self.imageResizeHeightLineEdit.editingFinished.connect(self.imageResizeHeightLineEditEditingFinished)
        self.formatLabel = QtWidgets.QLabel("format:", self)
        self.formatLabel.setGeometry(370, 180, 60, 20)
        self.tplFormat = QtWidgets.QComboBox(self)
        self.tplFormat.setGeometry(430, 180, 100, 20)
        self.TPLFormatSelectCombo = ["I4", "I8", "IA4", "IA8", "RGB565", "RGB5A3", "RGBA32"]
        for TPLFormatSelectComboOne in self.TPLFormatSelectCombo:
            self.tplFormat.addItem(TPLFormatSelectComboOne)
        self.tplFormat.setCurrentIndex(5)
        self.tplFormat.currentIndexChanged.connect(self.tplFormatCurrentIndexChanged)
        if self.isLangJPN:
            self.line2Label.setText("追加するMii ID (8桁16進数):")
            self.line3Label.setText("追加するアイコン画像:")
            self.line4Label.setText("TPLエンコード設定:")
            self.line5Label.setText("画像をリサイズする")
            self.addImageButton.setText("選択")
            self.formatLabel.setText("フォーマット:")
    def selectAddImage(self):
        tmpPath = ""
        if self.isLangJPN:
            tmpPath = self.openFileDialog("追加する画像選択", "Image Files (*.png;*.jpg;*.bmp)")
        else:
            tmpPath = self.openFileDialog("select image to add", "Image Files (*.png;*.jpg;*.bmp)")
        if len(tmpPath) == 0:
            return
        try:
            pix = QPixmap(tmpPath)
            pix = pix.scaledToWidth(100)
            pix = pix.scaledToHeight(100)
            self.addImageView.setPixmap(pix)
            self.srcImagePath = tmpPath
        except:
            pass
    def checkStateToFT(self, state):
        if state == QtCore.Qt.CheckState.Checked:
            return True
        return False
    def imageResizeCheckboxPushed(self):
        if self.checkStateToFT(self.imageResizeCheckbox.checkState()):
            self.enableImageResizeLineEdit()
            self.tplEncodeSetting.size = self.resizeSetting
        else:
            self.tplEncodeSetting.size = None
            self.disableImageResizeLineEdit()
    def imageResizeHeightLineEditEditingFinished(self):
        tmp = self.ston(self.imageResizeHeightLineEdit.text())
        if tmp > -1 and tmp < 65536:
            self.resizeSetting = (self.resizeSetting[0], tmp)
        self.imageResizeHeightLineEdit.setText("%d" % (self.resizeSetting[1]))
        self.tplEncodeSetting.size = self.resizeSetting
    def imageResizeWidthLineEditEditingFinished(self):
        tmp = self.ston(self.imageResizeWidthLineEdit.text())
        if tmp > -1 and tmp < 65536:
            self.resizeSetting = (tmp, self.resizeSetting[1])
        self.imageResizeWidthLineEdit.setText("%d" % (self.resizeSetting[0]))
        self.tplEncodeSetting.size = self.resizeSetting
    def disableImageResizeLineEdit(self):
        self.imageResizeWidthLineEdit.setEnabled(False)
        self.imageResizeHeightLineEdit.setEnabled(False)
    def enableImageResizeLineEdit(self):
        self.imageResizeWidthLineEdit.setEnabled(True)
        self.imageResizeHeightLineEdit.setEnabled(True)
    def tplFormatCurrentIndexChanged(self, value):
        self.tplEncodeSetting.format = TPLFormat(value)
    def szsMakeButtonPushed(self):
        if len(self.srcSzsDir) == 0:
            if self.isLangJPN:
                QtWidgets.QMessageBox.information(None, "MIO SZS Maker", "ベースとなるszsのフォルダが選択されてません。", QtWidgets.QMessageBox.StandardButton.Yes)
            else:
                QtWidgets.QMessageBox.information(None, "MIO SZS Maker", "base szs directory is not selected", QtWidgets.QMessageBox.StandardButton.Yes)
            return
        if len(self.destSzsDir) == 0:
            if self.isLangJPN:
                QtWidgets.QMessageBox.information(None, "MIO SZS Maker", "szsの保存先フォルダが選択されてません。", QtWidgets.QMessageBox.StandardButton.Yes)
            else:
                QtWidgets.QMessageBox.information(None, "MIO SZS Maker", "output szs directory is not selected", QtWidgets.QMessageBox.StandardButton.Yes)
            return
        if len(self.srcImagePath) == 0:
            if self.isLangJPN:
                QtWidgets.QMessageBox.information(None, "MIO SZS Maker", "追加する画像ファイルが選択されてません。", QtWidgets.QMessageBox.StandardButton.Yes)
            else:
                QtWidgets.QMessageBox.information(None, "MIO SZS Maker", "Image file is not selected", QtWidgets.QMessageBox.StandardButton.Yes)
            return
        self.isIconDelete = False
        if self.checkStateToFT(self.imageResizeCheckbox.checkState()):
            self.tplEncodeSetting.size = self.resizeSetting
        else:
            self.tplEncodeSetting.size = None
        self.mainWindow.makeSzs(self)
    def disableAllUI(self):
        self.srcSzsDirButton.setEnabled(False)
        self.srcSzsDirLineEdit.setEnabled(False)
        self.miiIDLineEdit.setEnabled(False)
        self.destSzsDirButton.setEnabled(False)
        self.destSzsDirLineEdit.setEnabled(False)
        self.szsMakeButton.setEnabled(False)
        self.addImageButton.setEnabled(False)
        self.imageResizeCheckbox.setEnabled(False)
        self.imageResizeWidthLineEdit.setEnabled(False)
        self.imageResizeHeightLineEdit.setEnabled(False)
        self.tplFormat.setEnabled(False)
    def enableAllUI(self):
        self.srcSzsDirButton.setEnabled(True)
        self.srcSzsDirLineEdit.setEnabled(True)
        self.miiIDLineEdit.setEnabled(True)
        self.destSzsDirButton.setEnabled(True)
        self.destSzsDirLineEdit.setEnabled(True)
        self.szsMakeButton.setEnabled(True)
        if self.isLangJPN:
            self.szsMakeButton.setText("SZSを作成")
        else:
            self.szsMakeButton.setText("Make SZS!!")
        self.addImageButton.setEnabled(True)
        self.imageResizeCheckbox.setEnabled(True)
        if self.checkStateToFT(self.imageResizeCheckbox.checkState()):
            self.imageResizeWidthLineEdit.setEnabled(True)
            self.imageResizeHeightLineEdit.setEnabled(True)
        self.tplFormat.setEnabled(True)
    

class MainWindow(QtWidgets.QWidget):
    taskFinshResultShowSignal = pyqtSignal()
    def __init__(self):
        super(MainWindow, self).__init__()
        self.isLangJPN = False
        try:
            if "JAPAN" in locale.getlocale()[0].upper():
                self.isLangJPN = True
                pass
        except:
            pass
        self.taskFinshResultShowSignal.connect(self.taskFinshResultShow)
        self.s = System()
        self.isTaskRunning = False
        self.setWindowTitle("MIO SZS Maker v0.1")
        self.setGeometry(300, 50, 400, 350)
        self.setFixedWidth(700)
        self.setFixedHeight(400)
        qtab = QTabWidget()
        self.tab1 = Tab1Widget(self)
        self.tab2 = Tab2Widget(self)
        if self.isLangJPN:
            qtab.addTab(self.tab1, "アイコン追加")
            qtab.addTab(self.tab2, "アイコン削除")
        else:
            qtab.addTab(self.tab1, "add icon")
            qtab.addTab(self.tab2, "delete icon")
        hbox = QHBoxLayout()
        hbox.addWidget(qtab)
        self.setLayout(hbox)
        self.userDefineTPLEncodeSetting = TPLEncodeSetting()
        self.mst = None
        self.run1frT = RunFunc1FrThreading(self)
        self.run1frT.start()
    def taskFinshResultShow(self):
        self.rw = ResultWindow()
        self.rw.show()
        self.rw.setResult(self.mst.error, self.mst.curProcess)
    def openFileDialog(self, title, filter):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(self, title, "", filter)
        return path
    def selectFolderDialog(self, title):
        return QtWidgets.QFileDialog.getExistingDirectory(self, title, "")
    def enableAllButton(self):
        pass
    def disableAllButton(self):
        pass
    def closeEvent(self, event):
        if self.mst is not None and self.isTaskRunning:
            if QtWidgets.QMessageBox.information(None, "MIO SZS Maker", "SZS modifying process in running. Do you want to force termination?", QtWidgets.QMessageBox.StandardButton.Yes, QtWidgets.QMessageBox.StandardButton.No) == QtWidgets.QMessageBox.StandardButton.No:
                event.ignore()
                return
            if self.mst is not None:
                self.mst.raiseExceptionToStop()
                self.mst.join()
        #System.delDir(System.getThisScriptDir() + "/tmp")
        event.accept()
    def makeSzs(self, tab):
        if self.isTaskRunning:
            return
        self.mst = MIO_SZS_Task()
        self.mst.srcSzsDir = tab.srcSzsDir
        self.mst.srcPngPath = tab.srcImagePath
        self.mst.miiId = tab.miiID
        self.mst.destSzsDir = tab.destSzsDir
        self.mst.tplEncodeSetting = tab.tplEncodeSetting
        self.mst.isIconDelete = tab.isIconDelete
        self.mst.taskDone = False
        self.isTaskRunning = True
        self.tab1.disableAllUI()
        self.tab2.disableAllUI()
        self.mst.start()
    def run1fr(self):
        if self.isTaskRunning == False:
            return
        if self.mst is None:
            return
        if self.mst.taskDone:
            self.taskFinshResultShowSignal.emit()
            self.isTaskRunning = False
            self.tab1.enableAllUI()
            self.tab2.enableAllUI()
            return
        self.tab1.setCurTaskDisplay(self.mst.curProcess)
        self.tab2.setCurTaskDisplay(self.mst.curProcess)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec())