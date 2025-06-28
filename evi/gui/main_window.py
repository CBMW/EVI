from typing import Dict
from PyQt5 import QtWidgets
from .hormone_widget import HormoneWidget
from .chat_widget import ChatWidget
from .emotion_graph import EmotionGraphWidget, EMOTIONS
from .settings_widget import SettingsWidget
from ..memory.memory_db import MemoryDB
from ..settings.settings_db import SettingsDB


def hormone_to_emotions(hormones: Dict[str, int]) -> Dict[str, float]:
    """Simple mapping from hormone levels (0-100) to emotions (-10 to 10)."""
    mapping = {
        'Joy': hormones.get('dopamine', 50),
        'Anger': hormones.get('adrenaline', 50),
        'Sadness': hormones.get('cortisol', 50),
        'Jealousy': hormones.get('testosterone', 50),
        'Love': hormones.get('oxytocin', 50),
        'Fear': int((hormones.get('adrenaline', 50) + hormones.get('cortisol', 50)) / 2),
        'Curiosity': hormones.get('dopamine', 50),
        'Disgust': hormones.get('serotonin', 50),
    }
    # scale 0-100 -> -10..10
    return {k: (v - 50) / 5 for k, v in mapping.items()}


class MainWindow(QtWidgets.QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("EVI Dashboard")
        self.resize(1000, 600)

        self.hormones: Dict[str, int] = {
            'adrenaline': 50,
            'dopamine': 50,
            'serotonin': 50,
            'cortisol': 50,
            'oxytocin': 50,
            'testosterone': 50,
            'estrogen': 50,
            'melatonin': 50,
        }
        self.memory = MemoryDB()
        self.settings = SettingsDB()

        self.tab_widget = QtWidgets.QTabWidget()

        dashboard = QtWidgets.QWidget()
        dash_layout = QtWidgets.QHBoxLayout()

        self.hormone_widget = HormoneWidget(self.hormones)
        self.chat_widget = ChatWidget(self.hormones, self.memory)
        self.emotion_widget = EmotionGraphWidget(hormone_to_emotions(self.hormones))

        self.hormone_widget.hormones_changed.connect(self._on_hormones_changed)

        dash_layout.addWidget(self.hormone_widget)
        dash_layout.addWidget(self.emotion_widget)
        dash_layout.addWidget(self.chat_widget)
        dashboard.setLayout(dash_layout)
        self.tab_widget.addTab(dashboard, "Dashboard")

        self.settings_widget = SettingsWidget(self.settings)
        self.tab_widget.addTab(self.settings_widget, "Settings")

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.tab_widget)
        self.setLayout(layout)

    def _on_hormones_changed(self, hormones: Dict[str, int]) -> None:
        emotions = hormone_to_emotions(hormones)
        self.emotion_widget.update_emotions(emotions)
