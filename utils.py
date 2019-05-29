# Utility functions
import lvgl

from PyQt5 import QtWidgets

# Thanks stack overflow :)
def iter_tree_widget(root):
    iterator = QtWidgets.QTreeWidgetItemIterator(root)
    while True:
        item = iterator.value()
        if item is not None:
            yield item
            iterator += 1
        else:
            break

# List occurrences of ch in s
def list_occurences(s, ch):
    return [i for i, letter in enumerate(s) if letter == ch]


def get_full_class_name(obj):
    # obj.__class__ comes out like "<class 'lv.Obj'>"
    # So strip all the other junk
    dirty_name = str(obj.__class__)
    single_qs = list_occurences(dirty_name, '\'')
    return dirty_name[single_qs[0]+1:single_qs[1]]


def address_of(some_obj):
    return hex(id(some_obj))


# Recursive generator for traversing the LVGL object tree
# Generates the object itself (at index 0) and all its children
def children_of(parent):
    yield parent
    for child in parent.get_children():
        yield from children_of(child)


# Yields all parents of a given child lv_obj
def all_parents_of(child):
    if child is not None:
        yield child.get_parent()
        yield from all_parents_of(child.get_parent())


# Gets the absolute (screen) position of a given lv_obj
# @retval tuple(x,y)
def get_absolute_position(lv_obj):
    x = lv_obj.get_x()
    y = lv_obj.get_y()
    for parent in all_parents_of(lv_obj):
        if parent != lvgl.scr_act() and parent is not None:
            x = x + parent.get_x()
            y = y + parent.get_y()

    return x, y
