import cv2
import numpy as np
import matplotlib.pyplot as plt
import math

scoring_order = [6, 10, 15, 2, 17, 3, 19, 7, 16, 8, 11, 14, 9, 12, 5, 20, 1, 18, 4, 13]

image_path = "dartboard.jpg"
image = cv2.imread(image_path)
if image is None:
    raise FileNotFoundError(f"Image not found at {image_path}")

image = cv2.resize(image, (800, 800))

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

gray_blurred = cv2.GaussianBlur(gray, (5, 5), 2)

edges = cv2.Canny(gray_blurred, 50, 150)

contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
outer_circle = max(contours, key=cv2.contourArea)
(x, y), radius = cv2.minEnclosingCircle(outer_circle)
center = (int(x), int(y))
radius = int(radius)

double_outer_radius = int(radius * 0.76)
double_inner_radius = int(radius * 0.72)
triple_outer_radius = int(radius * 0.48)
triple_inner_radius = int(radius * 0.44)
bull_outer_radius = int(radius * 0.08)
bull_inner_radius = int(radius * 0.03)

def calculate_score(dart_x, dart_y):
    dx, dy = dart_x - center[0], dart_y - center[1]
    distance = math.sqrt(dx**2 + dy**2)
    angle = math.degrees(math.atan2(dy, dx)) % 360

    if distance <= bull_inner_radius:
        return 50
    elif distance <= bull_outer_radius:
        return 25
    elif distance <= triple_outer_radius and distance >= triple_inner_radius:
        ring = "triple"
    elif distance <= double_outer_radius and distance >= double_inner_radius:
        ring = "double"
    elif distance < double_inner_radius:
        ring = "single"
    else:
        return 0

    wedge_index = int((angle + 9) // 18) % 20
    base_score = scoring_order[wedge_index]

    if ring == "double":
        return base_score * 2
    elif ring == "triple":
        return base_score * 3
    else:
        return base_score

def on_click(event):
    dart_x, dart_y = int(event.xdata), int(event.ydata)
    if dart_x is None or dart_y is None:
        print("Clicked outside the dartboard")
        return
    score = calculate_score(dart_x, dart_y)
    print(f"Dart landed at ({dart_x}, {dart_y}) with a score of {score}")

for i in range(20):
    angle = (i * 18) - 9
    angle_rad = math.radians(angle)
    x_end = int(center[0] + double_outer_radius * math.cos(angle_rad))
    y_end = int(center[1] + double_outer_radius * math.sin(angle_rad))
    cv2.line(image, center, (x_end, y_end), (255, 0, 0), 1)

cv2.circle(image, center, double_outer_radius, (255, 0, 255), 2)
cv2.circle(image, center, double_inner_radius, (255, 0, 255), 2)
cv2.circle(image, center, triple_outer_radius, (0, 255, 255), 2)
cv2.circle(image, center, triple_inner_radius, (0, 255, 255), 2)
cv2.circle(image, center, bull_outer_radius, (255, 0, 0), 2)
cv2.circle(image, center, bull_inner_radius, (255, 0, 0), 2)

image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
fig, ax = plt.subplots()
ax.imshow(image_rgb)
ax.set_title("Dartboard Segments and Scoring")
fig.canvas.mpl_connect('button_press_event', on_click)
plt.axis("off")
plt.show()
