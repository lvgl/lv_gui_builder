# LittlevGL Tree View Item subclass

from PyQt5.QtWidgets import QTreeWidgetItem, QTreeWidget
from PyQt5.QtCore import Qt
import lvgl
from utils import get_full_class_name, children_of, address_of


class LVGLTreeView(QTreeWidget):

    def __init__(self, contents):
        super().__init__(contents)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            #self.takeTopLevelItem(self.indexOfTopLevelItem(
            print("deleting object...")
            self.itemFromIndex(self.currentIndex()).get_lv_obj().del_()
            regenerate_lv_treeview(self)
            
        super().keyPressEvent(event)

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

    def __del__(self):
        #self.lv_obj.del_()
        pass

    def keyPressEvent(self, event):
        print(event.key())
        
    def get_lv_obj(self):
        return self.lv_obj


# Regenerates the LVGL object tree in given treeview widget
# TODO make this only update changes parts of the tree instead of regenerating the whole thing
def regenerate_lv_treeview(treeview):

    # Clear the treeview
    treeview.clear()

    # Recursive walk of LVGL object tree
    # Map lv parent objects to treeview parent objects
    lv_to_tv_parent_map = {address_of(None): treeview}

    for child in children_of(lvgl.scr_act()):
        child_tv_item  = LVGLTreeViewItem(child, lv_to_tv_parent_map[address_of(child.get_parent())])
        # Since the actual treeview object is unhashable
        # use the object's address as its key
        lv_to_tv_parent_map[address_of(child)] = child_tv_item

        if child.get_parent() is None:
            child_tv_item.setText(0, "screen")
        else:
            child_tv_item.setText(0, str(hex(id(child))))

        child_tv_item.setText(1, get_full_class_name(child))

        child_tv_item.setExpanded(True)
