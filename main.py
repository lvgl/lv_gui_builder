# LVGL GUI Builder Main

from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
import lvgl_builder


class LVGLBuilderApp(QMainWindow, lvgl_builder.Ui_MainWindow):
    def __init__(self, parent=None):
        super(LVGLBuilderApp, self).__init__(parent)
        self.setupUi(self)


def main():
    app = QApplication(sys.argv)
    window = LVGLBuilderApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()