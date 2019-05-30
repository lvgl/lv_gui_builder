# LVGL GUI Builder Main

from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeWidgetItem
import sys
import lvgl_builder
import lvgl
from introspector import list_lv_object_types, get_editable_properties
from LVGLTreeViewItem import regenerate_lv_treeview
from utils import iter_tree_widget


class LVGLBuilderApp(QMainWindow, lvgl_builder.Ui_MainWindow):
    def __init__(self, parent=None):
        super(LVGLBuilderApp, self).__init__(parent)
        self.setupUi(self)


def populate_widget_box(window):
    for w_name in list_lv_object_types():
        # Disallow placing a bare "Obj"
        if w_name == "Obj":
            continue
        window.listWidget.addItem(w_name)

def main():
    app = QApplication(sys.argv)
    window = LVGLBuilderApp()
    window.show()

    def populate_properties(lvgl_obj):
        window.property_tree.clear()
        # Skip population for None
        if not lvgl_obj:
            return

        properties = get_editable_properties(lvgl_obj)
        for p in properties:
            getter, setter, arg_list = properties[p]
            tv_item = QTreeWidgetItem(window.property_tree)
            tv_item.setText(0, p)
            try:
                tv_item.setText(1, str(getter()))
            except (NotImplementedError, TypeError) as e:
                # Catch unimplemented functions and hide them
                tv_item.setHidden(True)

    # Called when a new lvgl object is selected in the LVGLSimulator view
    def new_selection_cb(selected_lvgl_obj):
        window.object_tree.clearSelection()
        # Select the associated treeview item
        for item in iter_tree_widget(window.object_tree):
            if item.get_lv_obj() is selected_lvgl_obj:
                item.setSelected(True)

    # Called when an item is selected in the treeview
    # Since the above new_selection_cb modifies the selection
    # of the treeview, this callback is subsequently executed
    def tv_selection_changed(selected, deselected):
        indexes = selected.indexes()
        selected_item = None
        if len(indexes) > 0:
            # Get the selected tree view item
            selected_item = window.object_tree.itemFromIndex(selected.indexes()[0]).get_lv_obj()

        window.LVGLSimWindow.set_selected(selected_item)
        populate_properties(selected_item)

    window.LVGLSimWindow.set_new_selection_cb(new_selection_cb)
    window.object_tree.selectionModel().selectionChanged.connect(tv_selection_changed)

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

    regenerate_lv_treeview(window.object_tree)

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()