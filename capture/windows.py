"""
Script for capturing window screenshots on Windows.

Currently not agnostic to dpi scaling!
"""

import time
from datetime import datetime
import os

import numpy as np
import cv2

import mss
import win32gui  # pywin32


def capture_window(window_title=None, file_type="jpeg", img_quality=80, cooldown_secs=0):
    """Captures the given window and saves result."""
    # Get handle to window
    hwnd = None
    if window_title:
        hwnd = win32gui.FindWindow(None, window_title)
        if not hwnd:
            raise Exception("Window not found: " + window_title)

    # Get client area
    client_rect = win32gui.GetClientRect(hwnd)
    client_left, client_top, client_right, client_bottom = client_rect

    # Get screen coordinates
    client_pos = win32gui.ClientToScreen(hwnd, (client_left, client_top))
    left = client_pos[0]
    top = client_pos[1]
    width = client_right - client_left
    height = client_bottom - client_top
    monitor = {"top": top, "left": left, "width": width, "height": height}

    # Create output directory
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    directory_name = f"data/capture/imgs_{timestamp}"
    os.makedirs(directory_name)

    # Capture the window region
    with mss.mss() as sct:
        last_screenshot_time = 0

        while True:
            current_time = time.time()
            if current_time - last_screenshot_time < cooldown_secs:
                continue

            last_screenshot_time = current_time

            sct_img = sct.grab(monitor)

            # Convert the image to a format compatible with OpenCV
            img = np.array(sct_img)
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)  # Convert BGRA to BGR

            # Resize (small 16:9)
            img = cv2.resize(img, (853, 480), interpolation=cv2.INTER_AREA)

            # Display preview
            cv2.imshow("capture", img)

            # Save image
            ts = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
            if file_type == "jpeg":
                cv2.imwrite(f"{directory_name}/img{ts}.jpeg", img,
                            [int(cv2.IMWRITE_JPEG_QUALITY), img_quality])
            else:
                cv2.imwrite(f"{directory_name}/img{ts}.png", img)

            # Break loop
            if cv2.waitKey(1) == ord("q"):
                break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    capture_window("UFO 50", file_type="jpeg", quality=80, cooldown_secs=0.5)
