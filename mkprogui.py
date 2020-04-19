#! /home/trongphuong/Work/Flask/bin/python3

import os
import shutil
import sys
import json
from subprocess import run

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

config_file = "/home/trongphuong/Work/utils/mkcp_config.json"

class ErrorDialog(QDialog):
    def __init__(self, text, *arg, **kwarg):
        super().__init__(*arg, **kwarg)

        self.setWindowTitle("Error")

        label = QLabel(text)
        font = label.font()
        font.setPointSize(12)
        label.setFont(font)

        buttons = QDialogButtonBox.Ok
        buttonBox = QDialogButtonBox(buttons)
        buttonBox.accepted.connect(self.accept)

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addSpacing(10)
        layout.addWidget(buttonBox)

        self.setLayout(layout)


class OverridePrompt(QDialog):
    def __init__(self, path, *arg, **kwarg):
        super().__init__(*arg, **kwarg)

        self.path = path
        self.is_deleted = False

        self.setWindowTitle("Override existing directory")

        label = QLabel()
        font = label.font()
        font.setPointSize(10)
        label.setFont(font)
        label.setText(f"Directory {path} already exists.\nDo you want to override it?")

        buttons = QDialogButtonBox.Yes | QDialogButtonBox.No
        buttonBox = QDialogButtonBox(buttons)
        buttonBox.accepted.connect(self.yes_callback)
        buttonBox.rejected.connect(self.reject)


        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addSpacing(10)
        layout.addWidget(buttonBox)

        self.setLayout(layout)


    def yes_callback(self):
        # remove existing directory
        shutil.rmtree(self.path)
        
        self.is_deleted = True
        self.accept()


class PreferenceDialog(QDialog):
    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)

        self.template_directory = None

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
        with open(config_file, "r") as f:
            try:
                config = json.load(f)
                config["template_directory"] = self.template_directory
            except:
                config = {"template_directory": self.template_directory}

        with open("mkcp_config.json", "w") as f:
            json.dump(config, f)

        self.accept()


    def cancel_callback(self):
        self.template_directory = None
        self.reject()


    def button_path_callback(self):
        self.template_directory = QFileDialog.getExistingDirectory(self, 
                                                    "Open Directory",
                                                    "/home/trongphuong/Work")


class MainWindow(QMainWindow):
    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)

        self.add_bin = False
        self.add_docs = False
        self.add_test = False
        self.add_examples = False
        self.is_open = False

        self.directory = ""
        self.project_name = ""
        self.category = ""

        # create mkcp_config.json if not exists
        if not os.path.exists(config_file):
            f = open(config_file, "w")
            f.close()

        with open(config_file, "r") as f:
            try:
                self.template_directory = json.load(f)["template_directory"]
            except:
                self.template_directory = None

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
        self.combo_category = QComboBox()
        self.combo_category.currentTextChanged.connect(self.combo_category_callback)
        categories = self.getCategories()
        self.combo_category.addItem("")
        self.combo_category.addItems(sorted(categories))



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
        main_layout.addWidget(self.combo_category, 2, 3, 1, 2)

        main_layout.addWidget(check_open, 3, 2, 1, 1)
        main_layout.addWidget(button_create, 3, 3, 1, 1)
        main_layout.addWidget(button_preferences, 3, 4, 1, 1)


        main_group = QWidget()
        main_group.setLayout(main_layout)

        self.setCentralWidget(main_group)
        self.setGeometry(400, 400, 500, 0)


    def getCategories(self):
        categories = []

        if self.template_directory:
            for cat in os.listdir(self.template_directory):
                if os.path.isdir(os.path.join(self.template_directory, cat)):
                    categories.append(cat)

        return categories



    def button_directory_callback(self):
        self.directory = QFileDialog.getExistingDirectory(self, 
                                                    "Open Directory",
                                                    "/home/trongphuong/Work")
        self.line_directory.setText(self.directory)


    def button_preferences_callback(self):
        dialog = PreferenceDialog(self)
        dialog.exec()

        self.template_directory = dialog.template_directory or self.template_directory

        # update categories
        categories = self.getCategories()
        self.combo_category.clear()
        self.combo_category.addItem("")
        self.combo_category.addItems(sorted(categories))


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


    def button_create_callback(self):
        self.project_name = self.line_name.text()

        if self.directory == "":
            dialog = ErrorDialog("Missing directory")
            dialog.exec()
            return

        if self.project_name == "":
            dialog = ErrorDialog("Missing project name")
            dialog.exec()
            return

        if self.category == "":
            dialog = ErrorDialog("Missing category")
            dialog.exec()
            return

        full_path = os.path.join(self.directory, self.line_name.text())
        
        # check if directory is existed or not
        # delete it if user agrees
        if os.path.exists(full_path):
            prompt = OverridePrompt(full_path)
            prompt.exec()

            if prompt.is_deleted:
                self.createEntries(full_path)

        # create new directory after delete the old one
        else:
            self.createEntries(full_path)


    def createEntries(self, path):
        os.mkdir(path)
        os.chdir(path)

        os.mkdir('build')
        os.mkdir('include')
        os.mkdir('src')
        os.mkdir('lib')

        # add forder docs
        if self.add_docs:
            os.makedirs('docs/config')

            src = os.path.join(self.template_directory, "Doxyfile")
            shutil.copy2(src, "docs/config")

        # add forder bin
        if self.add_bin:
            os.mkdir('bin')

        # add forder exampless
        if self.add_examples:
            os.mkdir('examples')

        # add forder test
        if self.add_test:
            os.makedirs('test/bin')
            os.makedirs('test/build')


        # create file README
        file = open('README.md', 'w')
        file.close()

        # create git repo
        os.system("git init")

        # create .gitignore for git repository
        file = open('.gitignore', 'w')
        file.write("build/\n"
                    "bin/\n"
                    "*sublime*\n"
                    "sftp-mkcp_config.json\n")
        file.close()

        # Copy file CMakeLists.txt into project
        src = os.path.join(self.template_directory, self.category)
        src = os.path.join(src, 'CMakeLists.txt')
        shutil.copy2(src, '.')

        # TODO: improve this HARDCODE implementation for Tiva C project
        if self.category == 'tiva':
            # copy file startup_gcc.c into folder src
            src = os.path.join(self.template_directory, self.category)
            src = os.path.join(src, 'startup_gcc.c')
            shutil.copy2(src, 'src')

            # copy linker config file
            src = os.path.join(self.template_directory, self.category)
            src = os.path.join(src, 'linker_config.ld')
            shutil.copy2(src, '.')


        # copy sublime-project file to project
        src = os.path.join(self.template_directory, "x.sublime-project")
        dst = f"{self.project_name}.sublime-project"
        shutil.copy2(src, dst)

        # open project in Sublime Text
        if self.is_open:
            run(["subl", dst])



app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec()