from typing import Dict, List
import numpy as np
from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

EMOTIONS: List[str] = [
    'Joy', 'Anger', 'Sadness', 'Jealousy',
    'Love', 'Fear', 'Curiosity', 'Disgust'
]


def plot_emotional_state(ax, emotions: Dict[str, float]) -> None:
    """Plot emotions on the provided axes."""
    ax.clear()
    labels = EMOTIONS
    values = [emotions.get(e, 0.0) for e in labels]
    # close the loop for radar
    values += values[:1]
    angles = np.linspace(0, 2 * np.pi, len(labels) + 1, endpoint=True)

    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    ax.set_rlabel_position(0)
    ax.set_ylim(-10, 10)

    ax.plot(angles, values, linewidth=2, linestyle='solid')
    ax.fill(angles, values, alpha=0.25)
    # dominant emotion label
    if emotions:
        dom = max(emotions, key=lambda k: emotions[k])
        ax.set_title(f'Dominant: {dom}')


class EmotionGraphWidget(QtWidgets.QWidget):
    def __init__(self, emotions: Dict[str, float], parent=None) -> None:
        super().__init__(parent)
        self.emotions = emotions
        layout = QtWidgets.QVBoxLayout()
        self.figure = Figure(figsize=(4, 4))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        self._plot()

    def update_emotions(self, emotions: Dict[str, float]) -> None:
        self.emotions = emotions
        self._plot()

    def _plot(self) -> None:
        ax = self.figure.add_subplot(111, polar=True)
        plot_emotional_state(ax, self.emotions)
        self.canvas.draw_idle()
