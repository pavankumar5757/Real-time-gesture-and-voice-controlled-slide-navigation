from cvzone.HandTrackingModule import HandDetector
import cv2
import os
import numpy as np
import speech_recognition as sr

# Parameters for window size and gesture detection threshold
width, height = 1280, 520
gestureThreshold =400  #  threshold to detect gestures above the line
folderPath = ("ppp1")  # Folder containing presentation images in the form of .jpg or .png

# Camera Setup: initialize webcam and set resolution
cap = cv2.VideoCapture(0) # 0 is the default system camera
cap.set(3, width)  # Set width
cap.set(4, height)  # Set height

# Initialize speech recognizer for voice commands
recognizer = sr.Recognizer()

# Initialize hand detector with confidence threshold and max hands to detect
detectorHand = HandDetector(detectionCon=0.8, maxHands=1)

# Variables for managing annotations and UI states
imgList = []
delay = 20  # Delay to prevent multiple gesture triggers
buttonPressed = False  # Flag to indicate if a gesture button is pressed
counter = 0  # Counter for delay
drawMode = False  # Flag for drawing mode
imgNumber = 0  # Current slide index
delayCounter = 0  # Another delay counter (not used in this snippet)
annotations = [[]]  # List of lists to store annotations (drawings) per slide
annotationNumber = -1  # Current annotation index
annotationStart = False  # Flag to check if annotation drawing started
hs, ws = int(120 * 1), int(213 * 1)  # Size of the small webcam image preview

# Zoom Parameters
zoomScale = 1.0  # Initial zoom scale for slide images
zoomSpeed = 0.02  # Zoom increment/decrement speed

# Get sorted list of images from the folder (sorted by filename length)
pathImages = sorted(os.listdir(folderPath), key=len)
print(pathImages)  # Print the list of images

# Function to draw a circle on the image at the index finger position with given color
def drawOnImage(img, indexFinger, color):
    cv2.circle(img, indexFinger, 15, color, cv2.FILLED)

# Initial cursor position (not used in this snippet)
previousX, previousY = 0, 0

# Optional: Create a fullscreen window
'''
cv2.namedWindow("Slides", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Slides", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
'''

while True:
    # Capture frame from webcam
    success, img = cap.read()
    img = cv2.flip(img, 1)  # Flip image horizontally for mirror effect

    # Load current slide image and resize to fit window
    pathFullImage = os.path.join(folderPath, pathImages[imgNumber])
    imgCurrent = cv2.imread(pathFullImage)
    imgCurrent = cv2.resize(imgCurrent, (width, height))

    # Detect hands and landmarks in the webcam image
    hands, img = detectorHand.findHands(img)  # Returns list of hands and annotated image

    # Draw a green line as gesture threshold (to detect hand height)
    cv2.line(img, (0, gestureThreshold), (width, gestureThreshold), (0, 255, 0), 10)

    # If a hand is detected and no button is currently pressed
    if hands and buttonPressed is False:
        hand = hands[0]  # Get the first detected hand
        cx, cy = hand["center"]  # Center coordinates of the hand
        lmList = hand["lmList"]  # List of 21 hand landmarks (x,y)
        fingers = detectorHand.fingersUp(hand)  # List indicating which fingers are up (1) or down (0)

        # Map the index finger tip coordinates to screen coordinates for drawing
        xVal = int(np.interp(lmList[8][0], [width // 2, width], [0, width]))
        yVal = int(np.interp(lmList[8][1], [150, height-150], [0, height]))
        indexFinger = xVal, yVal

        # Gesture detection only if hand is above the gesture threshold line (near face)
        if cy <= gestureThreshold:
            # Gesture: Only thumb up (left swipe)
            if fingers == [1, 0, 0, 0, 0]:
                print("Left")
                buttonPressed = True
                if imgNumber > 0:
                    imgNumber -= 1  # Go to previous slide
                    annotations = [[]]  # Reset annotations for new slide
                    annotationNumber = -1
                    annotationStart = False

            # Gesture: Only pinky finger up (right swipe)
            if fingers == [0, 0, 0, 0, 1]:
                print("Right")
                buttonPressed = True
                if imgNumber < len(pathImages) - 1:
                    imgNumber += 1  # Go to next slide
                    annotations = [[]]  # Reset annotations for new slide
                    annotationNumber = -1
                    annotationStart = False

        # Gesture: Index and middle fingers up - show red circle on slide (hover effect)
        if fingers == [0, 1, 1, 0, 0]:
            cv2.circle(imgCurrent, indexFinger, 12, (0, 0, 255), cv2.FILLED)

        # Gesture: Only index finger up - start or continue annotation drawing
        if fingers == [0, 1, 0, 0, 0]:
            if annotationStart is False:
                annotationStart = True  # Start new annotation
                annotationNumber += 1
                annotations.append([])  # Add new annotation list
            print(annotationNumber)
            annotations[annotationNumber].append(indexFinger)  # Add current point to annotation
            cv2.circle(imgCurrent, indexFinger, 12, (0, 0, 255), cv2.FILLED)

        else:
            annotationStart = False  # Stop annotation if index finger is not up alone

        # Gesture: Index, middle, and ring fingers up - undo last annotation
        if fingers == [0, 1, 1, 1, 0]:
            if annotations:
                annotations.pop(-1)  # Remove last annotation
                annotationNumber -= 1
                buttonPressed = True  # Prevent multiple undo triggers

        # Zoom In Gesture: Index, middle, ring, and pinky fingers up
        if fingers == [0, 1, 1, 1, 1]:
            zoomScale += zoomSpeed  # Increase zoom scale
            print("Zoom In:", zoomScale)

        # Zoom Out Gesture: All fingers up
        if fingers == [1, 1, 1, 1, 1]:
            zoomScale -= zoomSpeed  # Decrease zoom scale
            if zoomScale < 1.0:
                zoomScale = 1.0  # Minimum zoom scale limit
            print("Zoom Out:", zoomScale)

        # Voice Command Gesture: Index finger and pinky finger up
        if fingers == [0, 1, 0, 0, 1]:
            buttonPressed = True
            print("Go to specific slide gesture detected")
            try:
                # Use microphone to listen for slide number voice command
                with sr.Microphone() as source:
                    print("Listening for slide number...")
                    audio = recognizer.listen(source)

                # Recognize speech using Google Speech Recognition
                command = recognizer.recognize_google(audio).lower()
                print("Voice Command:", command)

                # Extract slide number from the spoken command
                slide_number = int(command.split("slide")[-1].strip())

                # Check if slide number is valid and navigate to that slide
                if 0 <= slide_number < len(pathImages):
                    imgNumber = slide_number
                    annotations = [[]]  # Reset annotations for new slide
                    annotationNumber = -1
                    annotationStart = False
                    print(f"Going to slide {slide_number}")
                else:
                    print("Invalid slide number")

            except sr.UnknownValueError:
                print("Could not understand audio")
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")

    else:
        annotationStart = False  # Reset annotation start if no hand detected or button pressed

    # Manage delay to avoid multiple gesture triggers in quick succession
    if buttonPressed:
        counter += 1
        if counter > delay:
            counter = 0
            buttonPressed = False

    # Draw annotations (lines) on the current slide image
    for i, annotation in enumerate(annotations):
        for j in range(len(annotation)):
            if j != 0:
                cv2.line(imgCurrent, annotation[j - 1], annotation[j], (0, 0, 200), 12)

    # Apply zoom scaling to the current slide image
    imgCurrent = cv2.resize(imgCurrent, None, fx=zoomScale, fy=zoomScale)

    # Resize webcam image preview and place it on the slide image (bottom-right corner)
    imgSmall = cv2.resize(img, (ws, hs))
    h, w, _ = imgCurrent.shape
    imgCurrent[0:hs, w - ws: w] = imgSmall

    # Display the slide with annotations and webcam preview
    cv2.imshow("Slides", imgCurrent)
    #cv2.imshow("Image", img)  # Optional: show webcam image separately

    # Exit loop if 'q' key is pressed
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

# Release resources and close windows
cv2.destroyAllWindows()
