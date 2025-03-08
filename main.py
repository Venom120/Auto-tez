import time,cv2
from vision import Vision
from WindowCapture import Capturer

def display_fps(prev_time):
    # Calculate FPS
    fps = 1 / (time.time() - prev_time)
    print(f"FPS: {fps:.2f}")
    return time.time()

"""

GIVE THE PATH TO YOUR NEEDLE IMAGE HERE

"""
"""

GIVE THE PATH TO YOUR NEEDLE IMAGE HERE

"""
# Load and preprocess
vision = Vision("data/ball_2.jpg")  # Load the needle image
vision = Vision("data/ball_2.jpg")  # Load the needle image
capturer = Capturer()

title = "RMX2151"  # Replace with your target window's title
geom = capturer.get_window_geometry_from_wmctrl(title)  # Find the target window's geometry
if not geom:
    print("Window not found!")
    exit(1)

x, y, width, height, found_title = geom

# Adjust for the initial offset and reduce the window size for better performance
offset_x=150
offset_y=520
x+=offset_x
y+=offset_y
width=width-offset_x-120
height=height-offset_y-270
geom = x, y, width, height, found_title
# Draw line for ball crossing
Scords, Ecords = (180,550), (250,550) # according to full w and h of the window
Scords, Ecords = (Scords[0]-offset_x, Scords[1]-offset_y), (Ecords[0]-offset_x, Ecords[1]-offset_y)

print(f"Found window '{(x, y, width, height, found_title)}'")


prev_time = time.time()
with open("log.txt", "w") as f:
    f.write(f"Window: {found_title}\n")

cnt=1
sav=True
clicked=0
click_counter=0
while True:
    cv_img = capturer.get_screenshot(x, y, width, height)  # Get the screenshot (BGR format)
    rgb_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)  # Convert to RGB for OpenCV
    if clicked==0:
        if sav: 
            cv2.imwrite(f"images/ss_{cnt}.jpg", rgb_img)  # Save screenshot for debugging
            cnt+=1
            save=False
        gray_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)  # Convert to grayscale for template matching

        """
        
        DO YOU WANT TO TRY TO FIND THE NEEDLE IMG FIRST??
        
        """
        want_needle = False  # Set to True to enable needle finding

        if want_needle:
            # Perform template matching
            max_loc = vision.find(gray_img, is_grayscale=True)

            # Draw rectangle
            start_x, start_y, end_x, end_y = max_loc
            cv2.rectangle(rgb_img, (start_x, start_y), (end_x, end_y), thickness=2, color=(255, 0, 0))

        # Using template matching to find the needle
        max_loc = vision.find(gray_img, is_grayscale=True)
        # Perform ADB click if the needle is found
        if max_loc is not None:
            capturer.adb_click(542, 2185)  # Perform ADB click
            print("CLICKED!!!")
            with open ("log.txt", "a") as f:
                f.write(f"clicked\n")
            clicked=500 if click_counter<=20 else 200
            click_counter+=1
        else:
            clicked=0

        # Using ball crossing to find the needle
        # crossing_index = vision.ball_crossed(rgb_img[Scords[1]][Scords[0]:Ecords[0]])
        # if crossing_index is not None:
        #     capturer.adb_click(542, 2185)  # Perform ADB click
        #     with open ("log.txt", "a") as f:
        #         f.write(f"clicked\n")
            #     f.write(f"ball detected {cnt}\n")
            #     f.write(f"{list(cv_img[580][185:300])}\n")
            #     cv2.imwrite(f"images/detected_ball.png", cv_img[400:700][185:300])

        # cv2.line(rgb_img, Scords, Ecords, thickness=2, color=(0, 0, 200))
        
        
        # else:
            # print("No needle found")
    else:
        clicked-=1
    # Display the result
    cv2.putText(rgb_img, f"{clicked}" ,(10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (50, 50, 50))
    cv2.imshow("Computer Vision", rgb_img)

    # prev_time = display_fps(prev_time)  # Display FPS and update prev_time for next frame
    if cv2.waitKey(1) == ord('q'):
        cv2.destroyAllWindows()
        break
print("done")
print("Log saved to log.txt")
print()
print("I clicked", click_counter, "times")