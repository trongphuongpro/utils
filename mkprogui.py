#! /home/trongphuong/Work/Flask/bin/python3

import os
import os.path
import sys
import json

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class ErrorDialog(QDialog):
    def __init__(self, text, *arg, **kwarg):
        super().__init__(*arg, **kwarg)

        self.setWindowTitle("Error")

        label = QLabel(text)
        font = label.font()
        font.setPointSize(15)
        label.setFont(font)

        buttons = QDialogButtonBox.Ok
        buttonBox = QDialogButtonBox(buttons)
        buttonBox.accepted.connect(self.accept)

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addSpacing(10)
        layout.addWidget(buttonBox)

        self.setLayout(layout)



class PreferenceDialog(QDialog):
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
        with open("config.json", "r") as f:
            config = json.load(f)
            config["template_directory"] = self.template_directory


        with open("config.json", "w") as f:
            json.dump(config, f)

        self.accept()


    def cancel_callback(self):
        self.reject()


    def button_path_callback(self):
        self.template_directory = QFileDialog.getExistingDirectory(self, 
                                                    "Open Directory",
                                                    "/home/trongphuong/Work")


cmakeTemplatesDir = '/CMake_templates/'
doxygenTemplatesDir = '/Doxygen_templates/'
sublimeTemplatesDir = '/Sublime_templates/'
tivaTemplatesDir = '/TivaC_templates/'


class DataModel(QAbstractListModel):
    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)

        #self.categories = 


    def data(self, index, role):
        if role == Qt.DisplayRole:
            text = self.categories[index.row()]

            return text


    def rowCount(self, index):
        return len(self.categories)


class MainWindow(QMainWindow):
    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)

        self.add_bin = False
        self.add_docs = False
        self.add_test = False
        self.add_examples = False
        self.is_open = False

        self.directory = None
        self.category = None

        with open("config.json", "r") as f:
            self.template_directory = json.load(f)["template_directory"]

        # Create options group box
        group_options = QGroupBox("Options")
        group_options.setAlignment(Qt.AlignCenter)

        check_test = QCheckBox("test")
        check_test.clicked.connect(self.check_test_callback)

        check_docs = QCheckBox("docs")
        check_docs.clicked.connect(self.check_docs_callback)

        check_example = QCheckBox("examples")
        check_example.clicked.connect(self.check_example_callback)

        check_bin = QCheckBox("bin")
        check_bin.clicked.connect(self.check_bin_callback)


        layout_options = QVBoxLayout()
        layout_options.addWidget(check_bin)
        layout_options.addWidget(check_docs)
        layout_options.addWidget(check_example)
        layout_options.addWidget(check_test)

        group_options.setLayout(layout_options)

        # Create text input fields
        label_directory = QLabel("In directory:")
        self.line_directory = QLineEdit()

        button_directory = QPushButton("Browse...")
        button_directory.pressed.connect(self.button_directory_callback)

        label_name = QLabel("Project name:")
        self.line_name = QLineEdit()
        self.line_name.setMaxLength(20)
        self.line_name.setPlaceholderText("Type project name here")

        label_category = QLabel("Category:")
        combo_category = QComboBox()
        combo_category.currentTextChanged.connect(self.combo_category_callback)
        categories = [f.split('-')[0] for f in os.listdir(self.template_directory + cmakeTemplatesDir)]
        combo_category.addItem("")
        combo_category.addItems(sorted(categories))



        check_open = QCheckBox("Open project")
        check_open.clicked.connect(self.check_open_callback)

        button_create = QPushButton("Create")
        button_create.pressed.connect(self.button_create_callback)

        button_preferences = QPushButton("Preferences")
        button_preferences.pressed.connect(self.button_preferences_callback)

        main_layout = QGridLayout()
        main_layout.setColumnMinimumWidth(1, 10)

        main_layout.addWidget(group_options, 0, 0, 4, 1)

        main_layout.addWidget(label_directory, 0, 2, 1, 1)
        main_layout.addWidget(self.line_directory, 0, 3, 1, 1)
        main_layout.addWidget(button_directory, 0, 4, 1, 1)

        main_layout.addWidget(label_name, 1, 2, 1, 1)
        main_layout.addWidget(self.line_name, 1, 3, 1, 2)

        main_layout.addWidget(label_category, 2, 2, 1, 1)
        main_layout.addWidget(combo_category, 2, 3, 1, 2)

        main_layout.addWidget(check_open, 3, 2, 1, 1)
        main_layout.addWidget(button_create, 3, 3, 1, 1)
        main_layout.addWidget(button_preferences, 3, 4, 1, 1)


        main_group = QWidget()
        main_group.setLayout(main_layout)

        self.setCentralWidget(main_group)
        self.setGeometry(400, 400, 500, 0)


    def button_directory_callback(self):
        self.directory = QFileDialog.getExistingDirectory(self, 
                                                    "Open Directory",
                                                    "/home/trongphuong/Work")
        self.line_directory.setText(self.directory)


    def button_preferences_callback(self):
        dialog = PreferenceDialog(self)
        dialog.exec()

        self.template_directory = dialog.template_directory


    def button_create_callback(self):
        if self.directory is None:
            dialog = ErrorDialog("Missing directory")
            dialog.exec()
            return

        if self.line_name.text() == "":
            dialog = ErrorDialog("Missing project name")
            dialog.exec()
            return

        if self.category == "":
            dialog = ErrorDialog("Missing category")
            dialog.exec()
            return

        full_path = os.path.join(self.directory, self.line_name.text())
        print(full_path)


    def check_open_callback(self, state):
        self.is_open = state


    def check_bin_callback(self, state):
        self.add_bin = state


    def check_test_callback(self, state):
        self.add_test = state


    def check_example_callback(self, state):
        self.add_examples = state


    def check_docs_callback(self, state):
        self.add_docs = state


    def combo_category_callback(self, text):
        self.category = text

        


app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec()