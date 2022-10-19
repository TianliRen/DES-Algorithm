from PyQt5.QtWidgets import QDialog, QMessageBox, QFileDialog
from PyQt5 import QtWidgets, uic, QtGui
from run import *
import sys


# This class handles the GUI section, which avails the interaction between users and the application
class MyWin(QDialog):
    def __init__(self):
        super(MyWin, self).__init__()
        uic.loadUi('design_02.ui', self)
        self.setWindowTitle("DES")

        # bind buttons with their respective methods
        self.encryptButton.clicked.connect(self.click_encrypt)
        self.decryptButton.clicked.connect(self.click_decrypt)
        self.fileUploadButton.clicked.connect(self.click_file)
        self.fileDownloadButton.clicked.connect(self.click_download)

    # Clicking encrypt button brings functions related to encryption.
    def click_encrypt(self):
        origin_text = self.originEncryptEditer.toPlainText()
        key = self.keyEncryptEditer.toPlainText()
        if origin_text == '':
            alert_message("Original Text cannot be empty")
        elif key == '':
            alert_message("Key for encryption cannot be empty")
        else:
            self.resultEncryptBrowser.setText(execute_des(origin_text, key, 'en'))

    # Clicking decrypt button brings functions related to decryption.
    def click_decrypt(self):
        result_text = self.resultDecryptEditer.toPlainText()
        key = self.keyDecryptEditer.toPlainText()
        if result_text == '':
            alert_message("Encrypted Text cannot be empty")
        elif key == '':
            alert_message("Key for decryption cannot be empty")
        else:
            self.originDecryptBrowser.setText(execute_des(result_text, key, 'de'))

    # click file button to upload a file
    def click_file(self):
        try:
            file_path, ok = QFileDialog.getOpenFileName(self,
                                                        "Select One File",
                                                        "D:/",
                                                        "All Files (*)")
            with open(file_path, 'rb') as f:
                self.originEncryptEditer.setText(str(base64.b64encode(f.read()), encoding='UTF-8'))
        except:
            print("You should choose a file")

    # clicking download button could download the file
    def click_download(self):
        origin_text = self.originDecryptBrowser.toPlainText()
        if origin_text == '':
            alert_message("Origin cannot be empty")
        else:
            save_path_name, file_type = QFileDialog.getSaveFileName(self,
                                                                    "Select saving directory",
                                                                    "D:/")
            with open(save_path_name, 'wb') as f:
                f.write(base64.b64decode(bytes(origin_text, 'UTF-8')))


def display_win():
    app = QtWidgets.QApplication(sys.argv)
    myWin = MyWin()
    myWin.show()
    sys.exit(app.exec())


# Remind users of operating mistakes
def alert_message(message: str):
    box = QtWidgets.QMessageBox()
    box.setWindowTitle("ALERT")
    box.setText(message)
    box.addButton('Confirm', QMessageBox.YesRole)
    box.exec_()


if __name__ == '__main__':
    display_win()
