# Widges for each property type

from PyQt5 import QtWidgets
from PyQt5 import QtGui

class BasePropertyWidget():

    # Initialize a base property widget
    # @param[in] property_setter Pointer to method that sets
    # the value associated with this widget
    def __init__(self, property_setter):
        self.setter = property_setter

    def get_value(self):
        pass

    def set_value(self, new_value):
        pass

    def update_linked_property(self, new_value):
        # Ignore type errors at this point
        try:
            self.setter(new_value)
        except TypeError as e:
            pass


class BasicLineWidget(BasePropertyWidget, QtWidgets.QLineEdit):

    def __init__(self, property_setter, initial_value, parent=None):
        BasePropertyWidget.__init__(self, property_setter)
        QtWidgets.QLineEdit.__init__(self, parent)
        self.set_value(initial_value)
        self.textChanged.connect(self.update_linked_property)

    def get_value(self):
        return self.text()

    def set_value(self, new_value):
        self.setText(str(new_value))


class IntegerLineWidget(BasicLineWidget):

    def __init__(self, property_setter, initial_value, parent=None):
        BasicLineWidget.__init__(self, property_setter, initial_value, parent)
        self.setValidator(QtGui.QIntValidator())

    def update_linked_property(self, new_value):
        try:
            self.setter(int(new_value))
        except (TypeError, ValueError) as e:
            pass


class EightBitLineWidget(IntegerLineWidget):

    def __init__(self, property_setter, initial_value, parent=None):
        BasicLineWidget.__init__(self, property_setter, initial_value, parent)
        self.setValidator(QtGui.QIntValidator(0, 255))

class SixteenBitLineWidget(IntegerLineWidget):

    def __init__(self, property_setter, initial_value, parent=None):
        BasicLineWidget.__init__(self, property_setter, initial_value, parent)
        self.setValidator(QtGui.QIntValidator(0, 65535))

class BoolCheckboxWidget(BasePropertyWidget, QtWidgets.QCheckBox):

    def __init__(self, property_setter, initial_value, parent=None):
        BasePropertyWidget.__init__(self, property_setter)
        QtWidgets.QCheckBox.__init__(self, parent)
        self.set_value(initial_value)
        self.toggled.connect(self.update_linked_property)

    def get_value(self):
        return self.isChecked()

    def set_value(self, new_value):
        self.setChecked(new_value)




def get_associated_widget(type_name):
    # Just in case it's not a string already
    type_name = str(type_name)
    widget = IntegerLineWidget  # default widget type
    try:
        widget = property_widget_map[type_name]
    except KeyError:
        pass  # Ignore if a widget type isn't associated

    return widget


property_widget_map = {
    'bool': BoolCheckboxWidget,
    'char*': BasicLineWidget,
    'lv_coord_t': IntegerLineWidget,
    'uint8_t': EightBitLineWidget,
    'uint16_t': SixteenBitLineWidget
}