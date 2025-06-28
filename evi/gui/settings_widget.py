from PyQt5 import QtWidgets
from ..settings.settings_db import SettingsDB


class SettingsWidget(QtWidgets.QWidget):
    """Widget to edit application settings."""

    def __init__(self, settings: SettingsDB, parent=None) -> None:
        super().__init__(parent)
        self.settings = settings

        layout = QtWidgets.QFormLayout()

        self.api_key_edit = QtWidgets.QLineEdit()
        self.api_key_edit.setText(self.settings.get("llm_api_key", ""))
        layout.addRow("LLM API Key:", self.api_key_edit)

        self.context_edit = QtWidgets.QPlainTextEdit()
        self.context_edit.setPlainText(self.settings.get("context_prompt", ""))
        layout.addRow("Context Prompt:", self.context_edit)

        self.save_button = QtWidgets.QPushButton("Save")
        self.save_button.clicked.connect(self._save)
        layout.addRow(self.save_button)

        layout.addItem(QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Expanding,
                                             QtWidgets.QSizePolicy.Expanding))
        self.setLayout(layout)

    def _save(self) -> None:
        self.settings.set("llm_api_key", self.api_key_edit.text().strip())
        self.settings.set("context_prompt", self.context_edit.toPlainText().strip())
