from PIL import Image
import time,cv2,subprocess,ctypes
import numpy as np
from vision import Vision
from WindowCapture import Capturer

def display_fps(prev_time):
    # Calculate FPS
    fps = 1 / (time.time() - prev_time)
    print(f"FPS: {fps:.2f}")
    return time.time()
def get_window_geometry_from_wmctrl(target_title):
    """
    Uses wmctrl -lG to find a window whose title contains target_title.
    Returns (x, y, width, height, title) if found, otherwise None.
    """
    # Specify a substring that uniquely identifies your window
    try:
        output = subprocess.check_output(["wmctrl", "-lG"]).decode("utf-8")
    except Exception as e:
        print("Failed to run wmctrl:", e)
        return None

    for line in output.splitlines():
        # wmctrl -lG output is expected to have 8 fields:
        # window_id, desktop, x, y, width, height, host, title
        parts = line.split(None, 7)
        if len(parts) < 8:
            continue
        win_id, desktop, x, y, width, height, host, title = parts
        if target_title in title:
            return int(x), int(y), int(width), int(height), title
    return None
def get_screenshot(x, y, width, height) -> np.ndarray:
    # --- Set up ctypes to call the C function ---
    # Load the shared library (ensure ss.so is in the current directory)
    lib = ctypes.CDLL("./ss.so")
    # Define the argument types for getScreen:
    # void getScreen(const int xx, const int yy, const int W, const int H, unsigned char *data)
    lib.getScreen.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int,
                                ctypes.POINTER(ctypes.c_ubyte)]
    buf_size = width * height * 3
    buffer = (ctypes.c_ubyte * buf_size)()
    lib.getScreen(x, y, width, height, buffer)
    # Convert the C buffer into a NumPy array and reshape to (height, width, 3)
    img = np.frombuffer(buffer, dtype=np.uint8).reshape((height, width, 3))
    img = img[:, :, [2, 1, 0]]
    return img



title = "RMX2151"  # Replace with your target window's title
geom = get_window_geometry_from_wmctrl(title)  # Find the target window's geometry
if not geom:
    print("Window not found!")
    exit(1)

x, y, width, height, found_title = geom
print(f"Found window '{found_title}' of width={width} and height={height}'")

# Load and preprocess
vision = Vision("data/needle.png")  # Load the needle image
capturer = Capturer()

prev_time = time.time()
with open("log.txt", "w") as f:
    f.write(f"Window: {found_title}\n")

display_img=None
cnt=0
while True:
    cv_img = get_screenshot(x, y, width, height)  # Get the screenshot (BGR format for cv2)
    cv_img = cv2.cvtColor(cv_img, cv2.COLOR_RGB2BGR)  # Convert back to RGB for display

    # Perform template matching
    max_loc = vision.find(cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY))

    display_img=cv_img.copy()
    # Draw rectangle around the found needle if any
    if max_loc is not None:
        # Draw rectangle correctly
        start_x, start_y, end_x, end_y = max_loc
        # cv2.rectangle(display_img, (start_x, start_y), (end_x, end_y), thickness=2, color=(255, 0, 0))

        # Draw line for ball crossing
        Scords, Ecords = (183,547), (300,547)
        cv2.line(display_img, Scords, Ecords, thickness=2, color=(0, 0, 200))

        # Check if ball has crossed the line
        crossing_index = vision.ball_crossed(cv_img[Scords[1]][Scords[0]:Ecords[0]])
        if crossing_index is not None:
            capturer.adb_click(542, 2185)  # Perform ADB click
            # with open ("log.txt", "a") as f:
            #     f.write(f"clicked\n")
            #     cnt+=1
            #     f.write(f"ball detected {cnt}\n")
            #     f.write(f"{list(cv_img[580][185:300])}\n")
            #     cv2.imwrite(f"images/detected_ball.png", display_img[400:700][185:300])

    
    
    else:
        # prev_time = display_fps(prev_time)  # Display FPS and update prev_time for next frame
        # print("No needle found")
        pass
    # Display the result
    cv2.imshow("Computer Vision", display_img)
    if cv2.waitKey(1) == ord('q'):
        cv2.destroyAllWindows()
        break
print("done")