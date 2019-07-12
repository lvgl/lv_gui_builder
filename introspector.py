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
            split_args = arg.split(' ')
            arg_type = split_args[0] # Typically, the arg type will be the first element here
            arg_name = split_args[1]
            if 'const' in arg_type:  # 'const' may shift that to the second element
                arg_type = split_args[1]
                arg_name = split_args[2]

            if '*' in arg_name: # Retain the pointer *
                arg_type += '*'

            arg_list[i] = arg_type

        arg_list = arg_list[1:] # Remove the first element (always lv_obj_t*)
        return arg_list

    # Get the getters
    members = inspect.getmembers(lv_obj)
    getters = {}
    setters = {}
    for name, fn in members:
        if 'get' in name and '__' not in name: # Remove private functions
            if name not in ignored_functions:
                getters[name] = fn

    # Get the setters
    for name, fn in inspect.getmembers(lv_obj):
        if 'set' in name and '__' not in name:  # Remove private functions
            if name not in ignored_functions:
                setters[name] = fn

    # Find the properties with getters and setters
    larger_list = getters
    smaller_list = setters
    prefix = "get_"
    other_prefix = "set_"
    if len(setters) > len(getters):
        larger_list = setters
        smaller_list = getters
        prefix = "set_"
        other_prefix = "get_"

    common = {}
    for name, fn in larger_list.items():
        # Remove the prefix
        prop_name = name.replace(prefix, "")
        # Check if it's in the other list
        for other_name, other_fn in smaller_list.items():
            # Found a property with a getter and setter
            if (other_prefix + prop_name) == other_name:
                getter = getters["get_"+prop_name]
                setter = setters["set_"+prop_name]
                arg_list = get_arg_list(setter)
                # Unimplemented functions may not have an arg list, ignore them
                if arg_list:
                    common[prop_name] = (getter, setter, arg_list)

    return common



if __name__ == "__main__":
    lv_types = list_lv_object_types()
    for t in lv_types:
        print(t)

    btn1 = lvgl.Btn(lvgl.scr_act())
    props = get_editable_properties(btn1)
    for key in props:
        print(key)
        getter,setter,arg_list = props[key]
        print("\t"+str(getter))
        print("\t"+str(setter))
        print("\t"+str(arg_list))