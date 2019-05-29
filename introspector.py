# LVGL Widget Element - builds th

import lvgl
import inspect

# Functions that duplicate other functions
ignored_functions = [
    'set_fit',
    'set_fit2',
    'set_x',
    'set_y'
]


# Turn these utility functions into a class called like `Introspector` or something
def list_lv_object_types():
    lv_object_types = []
    for key,val in lvgl.__dict__.items():
        try:
            val.__mro__
        except AttributeError:
            continue  # This one doesn't have any ancestors, skip scanning it

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


def get_editable_properties(lv_obj):
    editable = []

    def get_arg_list(fn):
        signature = inspect.getdoc(fn)

        # Throw away functions with blank doc strings
        if not signature:
            return None

        # Capture the argument list
        signature = signature[signature.find('(') + 1:]
        arg_list = signature[:-1].split(',')
        for i, arg in enumerate(arg_list):
            arg = arg.strip()
            arg_list[i] = arg.split(' ')[0] # get rid of the variable name
        arg_list = arg_list[1:] # Remove the first element (always lv_obj_t*)
        return arg_list

    for name, fn in inspect.getmembers(lv_obj):
        if 'set' in name and '__' not in name:  # Remove private functions
            if name not in ignored_functions:
                # Unimplemented functions may not have an arg list, ignore them
                arg_list = get_arg_list(fn)
                if arg_list:
                    editable.append((name, arg_list))

    return editable



if __name__ == "__main__":
    lv_types = list_lv_object_types()
    for t in lv_types:
        print(t)