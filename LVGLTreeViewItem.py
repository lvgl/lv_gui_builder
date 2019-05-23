# LittlevGL Tree View Item subclass

from PyQt5.QtWidgets import QTreeWidgetItem
import lvgl
from utils import get_full_class_name


class LVGLTreeViewItem(QTreeWidgetItem):

    # Lazily keep track of user types
    user_types = {}

    def __init__(self, lv_obj, parent):
        self.lv_obj = lv_obj
        # If there's no entry in the user_types dictionary for this type yet, insert it
        obj_class_name = lv_obj.__class__.__name__
        if obj_class_name not in LVGLTreeViewItem.user_types:
            LVGLTreeViewItem.user_types[obj_class_name] = QTreeWidgetItem.UserType + len(LVGLTreeViewItem.user_types)

        super().__init__(parent, type=LVGLTreeViewItem.user_types[obj_class_name])

    def get_lv_obj(self):
        return self.lv_obj


# Regenerates the LVGL object tree in given treeview widget
# TODO make this only update changes parts of the tree instead of regenerating the whole thing
def regenerate_lv_treeview(treeview):

    # Clear the treeview
    treeview.clear()

    # Recursive walk of LVGL object tree
    # @param[in] lv_obj LVGL object to walk children of
    # @param[in] parent_tv_item Parent treeview item of this lv_obj
    def walk_obj_children(child_lv_obj, parent_tv_item):

        child_tv_item = LVGLTreeViewItem(child_lv_obj, parent_tv_item)

        # This is the first item, kind of cheating using python here :-)
        if parent_tv_item == treeview:
            child_tv_item.setText(0, "screen")
        else:
            child_tv_item.setText(0, str(hex(id(child_lv_obj))))

        child_tv_item.setText(1, get_full_class_name(child_lv_obj))

        child_tv_item.setExpanded(True)

        for child in child_lv_obj.get_children():
            walk_obj_children(child, child_tv_item)

    root = lvgl.scr_act()
    walk_obj_children(root, treeview)
