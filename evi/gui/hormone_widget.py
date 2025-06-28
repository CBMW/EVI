from PyQt5 import QtWidgets, QtCore
from typing import Dict

class HormoneWidget(QtWidgets.QWidget):
    """Widget containing sliders for hormone levels."""
    hormones_changed = QtCore.pyqtSignal(dict)

    def __init__(self, hormones: Dict[str, int], parent=None) -> None:
        super().__init__(parent)
        self.hormones = hormones
        layout = QtWidgets.QVBoxLayout()
        self.sliders: Dict[str, QtWidgets.QSlider] = {}
        for name, level in self.hormones.items():
            label = QtWidgets.QLabel(f"{name}: {level}")
            slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
            slider.setMinimum(0)
            slider.setMaximum(100)
            slider.setValue(level)
            slider.valueChanged.connect(lambda value, n=name, l=label: self._update_hormone(n, value, l))
            layout.addWidget(label)
            layout.addWidget(slider)
            self.sliders[name] = slider
        layout.addStretch()
        self.setLayout(layout)

    def _update_hormone(self, name: str, value: int, label: QtWidgets.QLabel) -> None:
        label.setText(f"{name}: {value}")
        self.hormones[name] = value
        self.hormones_changed.emit(self.hormones)
