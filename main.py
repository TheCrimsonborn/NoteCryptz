import sys
import os
from PySide6.QtWidgets import (QApplication, QMainWindow, QTextEdit, 
                               QFileDialog, QMessageBox, QInputDialog, QLineEdit)
from PySide6.QtGui import QAction, QKeySequence, QFont
from crypto_core import CryptoCore

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.current_file = ""
        self.current_password = ""
        
        self.init_ui()

    def init_ui(self):
        self.resize(800, 600)
        self.update_title()

        # Text Editor setup
        self.text_edit = QTextEdit(self)
        self.text_edit.setFont(QFont("Consolas", 14))
        self.text_edit.setStyleSheet(
            "QTextEdit { background-color: #2b2b2b; color: #f8f8f2; border: none; padding: 10px; }"
        )
        self.setCentralWidget(self.text_edit)
        
        # Window styling
        self.setStyleSheet(
            "QMainWindow { background-color: #1e1e1e; } "
            "QMenuBar { background-color: #1e1e1e; color: #f8f8f2; } "
            "QMenuBar::item:selected { background-color: #3e3d32; } "
            "QMenu { background-color: #1e1e1e; color: #f8f8f2; } "
            "QMenu::item:selected { background-color: #3e3d32; }"
        )

        self.create_menus()

    def update_title(self):
        filename = os.path.basename(self.current_file) if self.current_file else "Untitled"
        self.setWindowTitle(f"NoteCryptz - {filename}")

    def create_menus(self):
        menubar = self.menuBar()
        
        # File Menu
        file_menu = menubar.addMenu("&File")

        open_act = QAction("&Open...", self)
        open_act.setShortcut(QKeySequence.Open)
        open_act.triggered.connect(self.open_file)
        file_menu.addAction(open_act)

        save_act = QAction("&Save", self)
        save_act.setShortcut(QKeySequence.Save)
        save_act.triggered.connect(self.save_file)
        file_menu.addAction(save_act)

        save_as_act = QAction("Save &As...", self)
        save_as_act.setShortcut(QKeySequence.SaveAs)
        save_as_act.triggered.connect(self.save_file_as)
        file_menu.addAction(save_as_act)

        file_menu.addSeparator()

        exit_act = QAction("E&xit", self)
        exit_act.setShortcut(QKeySequence.Quit)
        exit_act.triggered.connect(self.close)
        file_menu.addAction(exit_act)

        # Security Menu
        security_menu = menubar.addMenu("&Security")
        
        set_pwd_act = QAction("Set &Password...", self)
        set_pwd_act.triggered.connect(self.set_password)
        security_menu.addAction(set_pwd_act)

    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Open Encrypted File", "", "NoteCryptz Files (*.ncz);;All Files (*)"
        )
        if not file_name:
            return

        pwd = self.current_password
        if not pwd:
            pwd, ok = QInputDialog.getText(
                self, "Password", "Enter password to decrypt:", QLineEdit.Password
            )
            if not ok or not pwd:
                return
        else:
            pwd, ok = QInputDialog.getText(
                self, "Password", "Enter password to decrypt:", QLineEdit.Password, text=self.current_password
            )
            if not ok or not pwd:
                return

        try:
            with open(file_name, "rb") as f:
                encrypted_data = f.read()

            decrypted_text = CryptoCore.decrypt(encrypted_data, pwd)
            self.text_edit.setPlainText(decrypted_text)
            
            self.current_file = file_name
            self.current_password = pwd
            self.update_title()
            
            QMessageBox.information(self, "Success", "File decrypted securely.")
        except Exception as e:
            QMessageBox.critical(self, "Decryption Error", f"Failed to decrypt the file.\n{str(e)}")

    def save_file(self):
        if not self.current_file:
            self.save_file_as()
        else:
            self.save_to_file(self.current_file)

    def save_file_as(self):
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Save Encrypted File", "", "NoteCryptz Files (*.ncz);;All Files (*)"
        )
        if not file_name:
            return
            
        if self.save_to_file(file_name):
            self.current_file = file_name
            self.update_title()

    def set_password(self):
        pwd, ok = QInputDialog.getText(
            self, "Set Password", "Enter new password for encryption:", 
            QLineEdit.Password, text=self.current_password
        )
        if ok and pwd:
            self.current_password = pwd
            QMessageBox.information(self, "Password Set", "Password has been updated in memory for the next save.")

    def save_to_file(self, file_name: str) -> bool:
        pwd = self.current_password
        if not pwd:
            pwd, ok = QInputDialog.getText(
                self, "Password", "Enter password to encrypt:", QLineEdit.Password
            )
            if not ok or not pwd:
                QMessageBox.warning(self, "Warning", "Saving cancelled: Password is required.")
                return False
            self.current_password = pwd
        else:
            pwd, ok = QInputDialog.getText(
                self, "Password", "Re-enter password to encrypt:", QLineEdit.Password, text=self.current_password
            )
            if not ok or not pwd:
                return False
            self.current_password = pwd

        plaintext = self.text_edit.toPlainText()
        
        try:
            encrypted_data = CryptoCore.encrypt(plaintext, self.current_password)
            
            with open(file_name, "wb") as f:
                f.write(encrypted_data)
                
            QMessageBox.information(self, "Success", "File saved and securely encrypted.")
            return True
        except Exception as e:
            QMessageBox.critical(self, "Encryption Error", f"Failed to encrypt data.\n{str(e)}")
            return False

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("NoteCryptz")
    app.setApplicationVersion("2.0.0")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())
