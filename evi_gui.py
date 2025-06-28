import json
import os
from PyQt5 import QtWidgets, QtCore

MEMORY_FILE = "history.json"

class MemoryDB:
    """Simple JSON based memory stub."""

    def __init__(self, path=MEMORY_FILE):
        self.path = path
        self.data = []
        self._load()

    def _load(self):
        if os.path.exists(self.path):
            try:
                with open(self.path, 'r') as f:
                    self.data = json.load(f)
            except Exception:
                self.data = []

    def save(self):
        with open(self.path, 'w') as f:
            json.dump(self.data, f, indent=2)

    def add_message(self, sender, text, hormones):
        entry = {
            "sender": sender,
            "text": text,
            "hormones": hormones.copy(),
        }
        self.data.append(entry)
        self.save()

class HormoneWidget(QtWidgets.QWidget):
    """Widget containing sliders for hormone levels."""

    hormones_changed = QtCore.pyqtSignal(dict)

    def __init__(self, hormones, parent=None):
        super().__init__(parent)
        self.hormones = hormones
        layout = QtWidgets.QVBoxLayout()
        self.sliders = {}
        for name, level in hormones.items():
            label = QtWidgets.QLabel(f"{name}: {level}")
            slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
            slider.setMinimum(0)
            slider.setMaximum(100)
            slider.setValue(level)
            slider.valueChanged.connect(lambda value, n=name, l=label: self._update_hormone(n, value, l))
            layout.addWidget(label)
            layout.addWidget(slider)
            self.sliders[name] = slider
        self.setLayout(layout)

    def _update_hormone(self, name, value, label):
        label.setText(f"{name}: {value}")
        self.hormones[name] = value
        self.hormones_changed.emit(self.hormones)

class ChatWidget(QtWidgets.QWidget):
    """Widget for chat interface."""

    def __init__(self, hormones, memory, parent=None):
        super().__init__(parent)
        self.hormones = hormones
        self.memory = memory
        layout = QtWidgets.QVBoxLayout()

        self.display = QtWidgets.QPlainTextEdit()
        self.display.setReadOnly(True)

        self.input = QtWidgets.QLineEdit()
        self.input.returnPressed.connect(self.handle_input)
        self.input.textChanged.connect(self.check_interrupt)

        layout.addWidget(self.display)
        layout.addWidget(self.input)
        self.setLayout(layout)

    def append_message(self, sender, text):
        self.display.appendPlainText(f"{sender}: {text}")
        self.memory.add_message(sender, text, self.hormones)

    def handle_input(self):
        text = self.input.text().strip()
        if not text:
            return
        self.append_message("User", text)
        self.input.clear()
        # Placeholder for AI response
        response = "(AI would respond here)"
        self.append_message("EVI", response)

    def check_interrupt(self, text):
        """If adrenaline is high, interrupt with a warning."""
        if self.hormones.get("adrenaline", 0) > 80:
            self.append_message("EVI", "Please take a deep breath...")
            # reset slider as a simple effect
            self.hormones["adrenaline"] = 50

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EVI Dashboard")
        self.hormones = {
            "adrenaline": 50,
            "dopamine": 50,
            "serotonin": 50,
        }
        self.memory = MemoryDB()

        layout = QtWidgets.QHBoxLayout()
        self.hormone_widget = HormoneWidget(self.hormones)
        self.chat_widget = ChatWidget(self.hormones, self.memory)

        layout.addWidget(self.hormone_widget)
        layout.addWidget(self.chat_widget)
        self.setLayout(layout)


def main():
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
