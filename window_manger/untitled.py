from Quartz import CoreGraphics, CGWindowListCopyWindowInfo, kCGWindowListOptionAll, kCGNullWindowID, ImageIO
import Foundation
import ctypes
from PIL import Image

def save_cgimage_to_path(image, file_path, file_type='public.png'):
    url = Foundation.NSURL.fileURLWithPath_(file_path)
    dest = ImageIO.CGImageDestinationCreateWithURL(url, file_type, 1, None)
    if dest:
        ImageIO.CGImageDestinationAddImage(dest, image, None)
        success = ImageIO.CGImageDestinationFinalize(dest)
        if not success:
            print("Failed to save image to", file_path)
        else:
            print("Image saved successfully to", file_path)
    else:
        print("Failed to create image destination for", file_path)

def get_window_id(window_name):
    window_info = CGWindowListCopyWindowInfo(kCGWindowListOptionAll, kCGNullWindowID)

    for window in window_info:
        if window.get('kCGWindowName') == window_name:
            return window.get('kCGWindowNumber')

    return None

def capture_window(window_id):
    url = CoreGraphics.CGWindowListCreateImage(
        CoreGraphics.CGRectNull,
        CoreGraphics.kCGWindowListOptionIncludingWindow,
        window_id,
        CoreGraphics.kCGWindowImageBoundsIgnoreFraming
    )
    return url

# def main():
#     window_id = get_window_id("Minesweeper")  # Replace with the actual window ID

#     # Capture the window
#     cgimage = capture_window(window_id)
    
#     save_cgimage_to_path(cgimage, 'assets/game.png')

#     # Now you can process the image using PIL
#     # For example, save the image to a file

# main()