from PIL import Image

import matplotlib
matplotlib.use('WXAgg')

# Matplotlib elements used to draw the bounding rectangle
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt

import wx


class RectangleSelectImagePanel(wx.Panel):
    def __init__(self, parent, pathToImage = None):
        wx.Panel.__init__(self, parent)

        # Intitialise the matplotlib figure
        # self.figure = plt.figure() # it has it's own event loop.
        self.figure = matplotlib.figure.Figure()

        # Create an axes, turn off the labels and add them to the figure
        self.axes = plt.Axes(self.figure, [0, 0, 1, 1])
        self.axes.set_axis_off() 
        self.figure.add_axes(self.axes) 

        # Add the figure to the wxFigureCanvas
        self.canvas = FigureCanvas(self, -1, self.figure)

        # Initialise the rectangle
        self.rect = Rectangle((0,0), 1, 1, facecolor='None', edgecolor='green')
        self.x0 = None
        self.y0 = None
        self.x1 = None
        self.y1 = None
        self.axes.add_patch(self.rect)
        
        # Sizer to contain the canvas
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 3, wx.ALL)
        self.SetSizer(self.sizer)
        self.Fit()
        
        # Connect the mouse events to their relevant callbacks
        self.canvas.mpl_connect('button_press_event', self._onPress)
        self.canvas.mpl_connect('button_release_event', self._onRelease)
        self.canvas.mpl_connect('motion_notify_event', self._onMotion)
        
        # Lock to stop the motion event from behaving badly when the mouse isn't pressed
        self.pressed = False

        # If there is an initial image, display it on the figure
        if pathToImage is not None:
            self.setImage(pathToImage)

    def _onPress(self, event):
        # Check the mouse press was actually on the canvas
        if event.xdata is not None and event.ydata is not None:

            # Upon initial press of the mouse record the origin and record the mouse as pressed
            self.pressed = True
            self.rect.set_linestyle('dashed')
            self.x0 = event.xdata
            self.y0 = event.ydata

    def _onRelease(self, event):
        # Check that the mouse was actually pressed on the canvas to begin with and this isn't a rouge mouse
        # release event that started somewhere else
        if self.pressed:

            # Upon release draw the rectangle as a solid rectangle
            self.pressed = False
            self.rect.set_linestyle('solid')

            # Check the mouse was released on the canvas, and if it wasn't then just leave the width and 
            # height as the last values set by the motion event
            if event.xdata is not None and event.ydata is not None:
                self.x1 = event.xdata
                self.y1 = event.ydata

            # Set the width and height and origin of the bounding rectangle
            self.boundingRectWidth =  self.x1 - self.x0
            self.boundingRectHeight =  self.y1 - self.y0
            self.bouningRectOrigin = (self.x0, self.y0)

            # Draw the bounding rectangle
            self.rect.set_width(self.boundingRectWidth)
            self.rect.set_height(self.boundingRectHeight)
            self.rect.set_xy((self.x0, self.y0))
            self.canvas.draw()

    def _onMotion(self, event):
        # If the mouse has been pressed draw an updated rectangle when the mouse is moved so
        # the user can see what the current selection is
        if self.pressed:

            # Check the mouse was released on the canvas, and if it wasn't then just leave the width and 
            # height as the last values set by the motion event
            if event.xdata is not None and event.ydata is not None:
                self.x1 = event.xdata
                self.y1 = event.ydata
            
            # Set the width and height and draw the rectangle
            self.rect.set_width(self.x1 - self.x0)
            self.rect.set_height(self.y1 - self.y0)
            self.rect.set_xy((self.x0, self.y0))
            self.canvas.draw()

    def setImage(self, pathToImage):
        image = matplotlib.image.imread(pathToImage)
        imPIL = Image.open(pathToImage) 

        self.imageSize = imPIL.size
        
        self.axes.imshow(image, aspect='equal')
        self.canvas.draw()


# test
if __name__ == "__main__":

    app = wx.App()

    fr = wx.Frame(None, title='test')
    panel = RectangleSelectImagePanel(fr, '../screenshot/maxdome_main.jpg')
    
    fr.Show()
    app.MainLoop()
