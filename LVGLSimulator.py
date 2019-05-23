# LVGL Simulator Widget

from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene
from PyQt5.QtGui import QPainter, QPixmap, QImage, QColor
from PyQt5.QtCore import *
import lvgl

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

    def update(self):
        self.scene.invalidate(self.scene.sceneRect(), QGraphicsScene.BackgroundLayer)

    def mousePressEvent(self, event):
        # Send events to lvgl subsystem
        lvgl.send_mouse_event(event.pos().x(), event.pos().y(), event.buttons() & Qt.LeftButton)
        # Find out which object(s) were focused by that click

    def mouseReleaseEvent(self, event):
        lvgl.send_mouse_event(event.pos().x(), event.pos().y(), False)

    def mouseMoveEvent(self, event):
        lvgl.send_mouse_event(event.pos().x(), event.pos().y(), False)