from PyQt5 import QtWidgets
from typing import Dict
from ..memory.memory_db import MemoryDB

class ChatWidget(QtWidgets.QWidget):
    """Widget for chat interface."""

    def __init__(self, hormones: Dict[str, int], memory: MemoryDB, parent=None) -> None:
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

    def append_message(self, sender: str, text: str) -> None:
        self.display.appendPlainText(f"{sender}: {text}")
        self.memory.add_message(sender, text, self.hormones)

    def handle_input(self) -> None:
        text = self.input.text().strip()
        if not text:
            return
        self.append_message("User", text)
        self.input.clear()
        # Placeholder for AI response
        response = "(AI would respond here)"
        self.append_message("EVI", response)

    def check_interrupt(self, text: str) -> None:
        """If adrenaline is high, interrupt with a warning."""
        if self.hormones.get("adrenaline", 0) > 80:
            self.append_message("EVI", "Please take a deep breath...")
            # reset slider as a simple effect
            self.hormones["adrenaline"] = 50
