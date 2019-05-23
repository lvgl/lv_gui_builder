# LVGL Widget Element - builds th

import lvgl
import inspect

# Turn these utility functions into a class called like `Introspector` or something
def list_lv_object_types():
    lv_object_types = []
    for key,val in lvgl.__dict__.items():
        try:
            val.__mro__
        except AttributeError:
            continue # This one doesn't have any ancestors, skip scanning it

        parent_class_types = inspect.getmro(lvgl.__dict__[key])
        for parent in parent_class_types:
            if 'lvgl.Obj' in str(parent):
                lv_object_types.append(key)

    return lv_object_types

# Generate a preview screen using a separate lvgl display?
def get_lv_obj_preview(lv_type):
    # Create an instance of the type
    instance = lv_type.__init__(lvgl.scr_act())
    instance.set_pos(0, 0)
    instance.del_()


if __name__ == "__main__":
    lv_types = list_lv_object_types()
    for t in lv_types:
        print(t)