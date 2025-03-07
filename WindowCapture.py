import subprocess
class Capturer:
    def adb_click(self, x, y):
        subprocess.run(["adb", "shell", f"input tap {x} {y}"])