import qrcode
from qrcode.image.base import BaseImage
from .canvas import Canvas,Prefixes

from qrcode.image.base import BaseImage

class QRBrailleCanvasFactory(BaseImage):
    def __init__(self, border, width, box_size, *args, **kwargs):
        super().__init__(border, width, box_size, *args, **kwargs)
        
    def new_image(self, **kwargs):
        """Create a new canvas with the correct pixel dimensions"""
        pixel_width = self.pixel_size
        pixel_height = self.pixel_size
        
        self.canvas = Canvas(pixel_width, pixel_height, **kwargs)
        return self.canvas
    
    def drawrect(self, row, col):
        """Draw a single QR module at position (row, col)"""
        x0_pixels = (col + self.border) * self.box_size
        y0_pixels = (row + self.border) * self.box_size
        x1_pixels = x0_pixels + self.box_size
        y1_pixels = y0_pixels + self.box_size
        
        self.canvas.draw_box(x0_pixels,y0_pixels,int(x1_pixels)-1,int(y1_pixels)-1,filled=True)
    
    def save(self, stream, kind=None):
        """Save the canvas"""
        return self.canvas.save(stream, format=kind)
def qrcode_demo():
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.ERROR_CORRECT_L,
        box_size=1,
        border=2,
    )
    qr.add_data(f'https://www.youtube.com/watch?v={"QcXgW9w4wQd"[::-1]}')
    img = qr.make_image(image_factory=QRBrailleCanvasFactory)
    img.canvas.draw_border()
    img.canvas.set_str_prefix(Prefixes.bold)
    print(img.canvas)