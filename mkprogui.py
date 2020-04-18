#! /home/trongphuong/Work/Flask/bin/python3

import os
import os.path
import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class Dialog(QDialog):
    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)

        self.setWindowTitle("Preferences")

        button_path = QPushButton("Set template path")
        button_path.pressed.connect(self.button_path_callback)

        buttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        buttonBox = QDialogButtonBox(buttons)
        buttonBox.accepted.connect(self.ok_callback)
        buttonBox.rejected.connect(self.cancel_callback)

        layout_button = QVBoxLayout()
        layout_button.addWidget(button_path)
        layout_button.addSpacing(10)
        layout_button.addWidget(buttonBox)

        self.setLayout(layout_button)


    def ok_callback(self):
        self.accept()


    def cancel_callback(self):
        self.reject()


    def button_path_callback(self):
        self.directory = QFileDialog.getExistingDirectory(self, 
                                                    "Open Directory",
                                                    "/home/trongphuong/Work")
        print(self.directory)


class MainWindow(QMainWindow):
    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)

        button_preferences = QPushButton("Preferences")
        button_preferences.pressed.connect(self.button_preferences_callback)

        group_options = QGroupBox("Options")
        group_options.setAlignment(Qt.AlignCenter)

        check_test = QCheckBox("test")
        check_docs = QCheckBox("docs")
        check_example = QCheckBox("examples")
        check_bin = QCheckBox("bin")

        layout_options = QVBoxLayout()
        layout_options.addWidget(check_bin)
        layout_options.addWidget(check_docs)
        layout_options.addWidget(check_test)
        layout_options.addWidget(check_example)

        group_options.setLayout(layout_options)

        label_directory = QLabel("In directory:")
        line_directory = QLineEdit()

        button_directory = QPushButton("Browse...")
        button_directory.pressed.connect(self.button_directory_callback)

        label_name = QLabel("Project name:")
        line_name = QLineEdit()
        line_name.setMaxLength(20)
        line_name.setPlaceholderText("Type project name here")

        label_category = QLabel("Category:")
        combo_category = QComboBox()

        check_open = QCheckBox("Open project")
        button_create = QPushButton("Create")

        main_layout = QGridLayout()
        main_layout.setColumnMinimumWidth(1, 10)

        main_layout.addWidget(group_options, 0, 0, 4, 1)

        main_layout.addWidget(label_directory, 0, 2, 1, 1)
        main_layout.addWidget(line_directory, 0, 3, 1, 1)
        main_layout.addWidget(button_directory, 0, 4, 1, 1)

        main_layout.addWidget(label_name, 1, 2, 1, 1)
        main_layout.addWidget(line_name, 1, 3, 1, 2)

        main_layout.addWidget(label_category, 2, 2, 1, 1)
        main_layout.addWidget(combo_category, 2, 3, 1, 2)

        main_layout.addWidget(check_open, 3, 2, 1, 1)
        main_layout.addWidget(button_create, 3, 3, 1, 1)
        main_layout.addWidget(button_preferences, 3, 4, 1, 1)


        main_group = QWidget()
        main_group.setLayout(main_layout)

        self.setCentralWidget(main_group)


    def button_directory_callback(self):
        self.directory = QFileDialog.getExistingDirectory(self, 
                                                    "Open Directory",
                                                    "/home/trongphuong/Work")


    def button_preferences_callback(self):
        dialog = Dialog(self)
        dialog.exec()
        


app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec()