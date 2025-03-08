import subprocess, ctypes, numpy as np
class Capturer:
    def adb_click(self, x, y):
        subprocess.run(["adb", "shell", f"input tap {x} {y}"])
    def get_window_geometry_from_wmctrl(self, target_title):
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
    def get_screenshot(self, x, y, width, height) -> np.ndarray:
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