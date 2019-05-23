# LVGL GUI Builder Main

from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
import lvgl_builder
import lvgl
from introspector import list_lv_object_types
from LVGLTreeViewItem import regenerate_lv_treeview


class LVGLBuilderApp(QMainWindow, lvgl_builder.Ui_MainWindow):
    def __init__(self, parent=None):
        super(LVGLBuilderApp, self).__init__(parent)
        self.setupUi(self)


def populate_widget_box(window):
    for w_name in list_lv_object_types():
        window.listWidget.addItem(w_name)


def main():
    app = QApplication(sys.argv)
    window = LVGLBuilderApp()
    window.show()

    populate_widget_box(window)

    scrn1 = lvgl.scr_act()
    scrn1.set_style(lvgl.style_plain)

    b1 = lvgl.Btn(lvgl.scr_act())
    b1.set_size(150, 50)
    b1.align(b1.get_parent(), lvgl.ALIGN.IN_TOP_MID, 0, 10)

    l1 = lvgl.Label(b1)
    l1.set_text('Hello World!')

    st1 = lvgl.style_t(lvgl.style_plain)
    st1.line.width = 10
    st1.line.color = {'full': 0x258 }
    wheely = lvgl.Preload(scrn1)
    wheely.set_size(200, 200)
    wheely.set_style(lvgl.PRELOAD_STYLE.MAIN, st1)
    wheely.align(scrn1, lvgl.ALIGN.CENTER, 0, 0)

    regenerate_lv_treeview(window.treeWidget)

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()