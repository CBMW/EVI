from PyQt5 import QtWidgets
from evi.gui.main_window import MainWindow


def main() -> None:
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
