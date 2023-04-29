import sys
import os
import site

site_packages = site.getsitepackages()

for site_package in site_packages:
    pyqt5_path = os.path.join(site_package, "PyQt5")
    if os.path.isdir(pyqt5_path):
        sys.path.append(pyqt5_path)
        break

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QListWidget, QCheckBox,
                             QPushButton, QListWidgetItem, QInputDialog)

class TodoList(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Todo List')

        self.todo_list = QListWidget(self)
        self.todo_list.setFocusPolicy(Qt.NoFocus)
        self.todo_list.itemDoubleClicked.connect(self.edit_todo)

        self.load_todos()

        self.todo_input = QLineEdit(self)
        self.todo_input.returnPressed.connect(self.add_todo)

        vbox = QVBoxLayout()
        vbox.addWidget(QLabel('Todo List'))
        vbox.addWidget(self.todo_list)
        vbox.addWidget(self.todo_input)

        self.setGeometry(100, 100, 300, 400)
        self.setLayout(vbox)

    def load_todos(self):
        home = os.path.expanduser("~")
        todo_file = os.path.join(home, 'todos.txt')
        if os.path.exists(todo_file):
            with open(todo_file, 'r') as f:
                todos = f.read().splitlines()
            for todo in todos:
                todo_text, checked = todo.split("||")  # 변경
                self.add_checkbox(todo_text.strip(), checked == "True")  # 변경
                print(f"Loaded todo: {todo_text.strip()}")  # 추가

    def save_todos(self):
        home = os.path.expanduser("~")
        todo_file = os.path.join(home, 'todos.txt')
        with open(todo_file, 'w') as f:
            todos = []
            for i in range(self.todo_list.count()):
                item = self.todo_list.item(i)
                widget = self.todo_list.itemWidget(item)
                if widget:
                    layout = widget.layout()
                    for j in range(layout.count()):
                        checkbox = layout.itemAt(j).widget()
                        if isinstance(checkbox, QCheckBox):
                            todos.append(f"{checkbox.text()}||{checkbox.isChecked()}")  # 변경
            f.write('\n'.join(todos))

    def add_todo(self):
        todo = self.todo_input.text()
        if todo:
            self.add_checkbox(todo.strip())
            self.todo_input.clear()
            self.save_todos()

    def add_checkbox(self, todo, checked=False):  # 변경
        checkbox = QCheckBox(todo)
        checkbox.setChecked(checked)  # 변경
        checkbox.stateChanged.connect(self.save_todos)

        delete_button = QPushButton('-')
        delete_button.setFixedWidth(25)
        delete_button.clicked.connect(lambda: self.delete_todo(delete_button))

        widget = QWidget()
        hbox = QHBoxLayout()
        hbox.addWidget(checkbox)
        hbox.addWidget(delete_button)
        hbox.setContentsMargins(0, 0, 0, 0)
        widget.setLayout(hbox)

        item = QListWidgetItem(self.todo_list)
        self.todo_list.setItemWidget(item, widget)
        item.setSizeHint(widget.sizeHint())

    def delete_todo(self, button):
        for i in range(self.todo_list.count()):
            item = self.todo_list.item(i)
            widget = self.todo_list.itemWidget(item)
            if widget and widget.layout().indexOf(button) != -1:
                self.todo_list.takeItem(i)
                self.save_todos()
                i -= 1  # 인덱스 감소
                break

    def edit_todo(self, item):
        widget = self.todo_list.itemWidget(item)
        if widget:
            layout = widget.layout()
            for i in range(layout.count()):
                checkbox = layout.itemAt(i).widget()
                if isinstance(checkbox, QCheckBox):
                    new_text, ok = QInputDialog.getText(self, 'Edit Todo', 'Edit todo:', text=checkbox.text())
                    if ok and new_text:
                        checkbox.setText(new_text.strip())
                        self.save_todos()
                        break

    def closeEvent(self, event):
        self.save_todos()
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    todo_list = TodoList()
    todo_list.show()
    sys.exit(app.exec_())
