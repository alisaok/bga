import cv2
import numpy as np

def calculate_distance(focal_length, real_width, pixel_width):
    return (real_width * focal_length) / pixel_width

def draw_rectangles(image, rectangles):
    colors = {
        "red": (0, 0, 255),
        "green": (0, 255, 0),
        "blue": (255, 0, 0),
        "black": (0, 0, 0),
        "orange": (0, 165, 255)
    }

for rect in rectangles:
        x, y, w, h, color = rect
        cv2.rectangle(image, (x, y), (x + w, y + h), colors[color], 2)
        cv2.putText(image, f"Distance: {rect[5]} cm", (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, colors[color], 2)

def process_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, threshold = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
 rectangles = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        color = ""
  
        if w > 50 and h > 50:
            roi = image[y:y + h, x:x + w]
            hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
            avg_hue = np.average(hsv[:, :, 0])
            
            if 0 <= avg_hue <= 15 or 165 <= avg_hue <= 180:
                color = "red"
            elif 25 <= avg_hue <= 45:
                color = "green"
            elif 90 <= avg_hue <= 120:
                color = "blue"
            elif avg_hue <= 5:
                color = "black"
            else:
                color = "orange"

            focal_length = 100  
            real_width = 10  
            pixel_width = w  

            distance = calculate_distance(focal_length, real_width, pixel_width)
            rectangles.append((x, y, w, h, color, round(distance, 2)))
  
  draw_rectangles(image, rectangles)

    color_counts = {
        "red": 0,
        "green": 0,
        "blue": 0,
        "black": 0,
        "orange": 0
    }

 for rect in rectangles:
        color_counts[rect[4]] += 1

    cv2.putText(image, f"Red: {color_counts['red']}", (10, image.shape[0] - 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    cv2.putText(image, f"Green: {color_counts['green']}", (10, image.shape[0] - 50),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    cv2.putText(image, f"Blue: {color_counts['blue']}", (10, image.shape[0] - 80),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
    cv2.putText(image, f"Black: {color_counts['black']}", (10, image.shape[0] - 110),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
    cv2.putText(image, f"Orange: {color_counts['orange']}", (10, image.shape[0] - 140),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 165, 255), 2)

    return image

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    processed_frame = process_image(frame)

    cv2.imshow("Webcam", processed_frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
