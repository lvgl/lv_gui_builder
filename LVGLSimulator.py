# LVGL Simulator Widget

from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import lvgl
from utils import address_of, children_of, get_absolute_position, get_full_class_name

import inspect


# Returns a list of lvgl objects under coordinates at x,y
def get_objects_under_coords(x, y):
    clicked = []
    # Go through every lvgl object and find those intersecting the mouse click
    for child in children_of(lvgl.scr_act()):
        # TODO: use: coords = child.get_coords()
        if child is lvgl.scr_act():
            continue
        lv_x, lv_y = get_absolute_position(child)
        bounding_rect = QRect(lv_x, lv_y, child.get_width(), child.get_height())
        if bounding_rect.contains(x, y):
            clicked.append(child)

    return clicked


class LVGLScene(QGraphicsScene):
    def __init__(self, args):
        super().__init__(args)

    def drawBackground(self, painter, rect):

        # Poll lvgl and display the framebuffer
        for i in range(10):
            lvgl.poll()

        data = bytes(lvgl.framebuffer)
        img = QImage(data, lvgl.HOR_RES, lvgl.VER_RES, QImage.Format_RGB16)
        pm = QPixmap.fromImage(img)
        painter.drawPixmap(self.sceneRect(), pm, QRectF(pm.rect()))


class LVGLSimulator(QGraphicsView):
    def __init__(self, args):
        super().__init__(args)
        self.setMinimumSize(lvgl.HOR_RES, lvgl.VER_RES)
        self.setMaximumSize(lvgl.HOR_RES, lvgl.VER_RES)

        # Set the scene...
        self.scene = LVGLScene(self)
        self.scene.setSceneRect(0, 0, lvgl.HOR_RES, lvgl.VER_RES)
        self.setScene(self.scene)

        # Start frame update timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(10)
        self.show()

        self.new_selection_cb = None
        self.selection_box = None


    def update(self):
        self.scene.invalidate(self.scene.sceneRect(), QGraphicsScene.BackgroundLayer)

    # Creates a new lv object. LV objects to be tracked MUST be created using this method
    def create_lv_object(self, lv_obj_type, args):
        lv_obj = lv_obj_type.__init__(args)

    def mousePressEvent(self, event):
        # Send events to lvgl subsystem
        lvgl.send_mouse_event(event.pos().x(), event.pos().y(), event.buttons() & Qt.LeftButton)
        # Find out which object(s) were focused by that click and select one
        selected_item = self.select_object(get_objects_under_coords(event.pos().x(), event.pos().y()))

        # Create a box around the selected item (if not None)
        # Now handled by associated treeview selection change event handler
        #self.highlight_selected(selected_item)

        # Call the application handler
        if self.new_selection_cb:
            self.new_selection_cb(selected_item)

    def mouseDoubleClickEvent(self, event):
        #TODO refactor this to get rid of duplication of mousePressEvent code

        # Find out which object(s) were focused by that click and select one
        selected_item = self.select_object(get_objects_under_coords(event.pos().x(), event.pos().y()), True)
        
        # Create a box around the selected item (if not None)
        # Now handled by associated treeview selection change event handler
        #self.highlight_selected(selected_item)

        # Get the offset of the mouse click from the object's top-left corner (actual position)
        for m in inspect.getmembers(selected_item):
            print(m)

        # Call the application handler
        if self.new_selection_cb:
            self.new_selection_cb(selected_item)

    def mouseReleaseEvent(self, event):
        lvgl.send_mouse_event(event.pos().x(), event.pos().y(), False)

    def mouseMoveEvent(self, event):
        lvgl.send_mouse_event(event.pos().x(), event.pos().y(), False)

    #@param[in] lvgl object to select
    def highlight_selected(self, selected_item):
        # Create a box around the selected item (if not None)
        if selected_item and selected_item is not lvgl.scr_act():
            if self.selection_box:
                self.scene.removeItem(self.selection_box)
                self.selection_box = None
            # TODO - access cached values on corresponding treeview item
            lv_x, lv_y = get_absolute_position(selected_item)
            bounding_box = QRectF(lv_x, lv_y, selected_item.get_width(), selected_item.get_height())
            self.selection_box = self.scene.addRect(bounding_box, QPen(Qt.red, 5), QBrush())
        else:  # Delete the selection box
            if self.selection_box:
                self.scene.removeItem(self.selection_box)
                self.selection_box = None


    # Encapsulates logic for item selection
    # for now it just returns the first item in the list of possible objects
    def select_object(self, obj_list, double_clicked = False):
        if len(obj_list) == 0:
            return None

        # TODO this algorithm (below) works for now, but should be revisited in the future

        # If it wasn't a double click, just return the first object
        if not double_clicked or len(obj_list) is 1:
            return obj_list[0]
        else:
            # Prioritize label objects
            for o in obj_list:
                if "Label" in get_full_class_name(o):
                    return o

            # If no labels were found, return the second object
            return obj_list[1]

    # Setter for application to set selected lvgl object
    #@param[in] selected_item LVGL object that should be highlighted
    def set_selected(self, selected_item):
        self.highlight_selected(selected_item)

    # Application callback to be executed when a new lvgl object is selected
    def set_new_selection_cb(self, cb):
        self.new_selection_cb = cb

