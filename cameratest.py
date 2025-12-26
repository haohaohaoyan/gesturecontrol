import cv2, mediapipe, pyautogui, mouse 

camera = cv2.VideoCapture(0)

SPEED = 2

# get monitor size 
screenx, screeny = pyautogui.size()

last_x,last_y, current_x, current_y = 0,0,0,0

def display_result(result, output_image, timestamp_ms):
    global last_x,last_y, current_x, current_y
    try:
        index = 0
        for gesture in result.gestures:
            current_gesture = gesture[0].category_name
            current_hand = index # flip-flop the checking between each hand

            current_x, current_y = result.hand_landmarks[current_hand][8].x, result.hand_landmarks[current_hand][8].y
            if current_gesture == "Pointing_Up":
                mouse.move((current_x - last_x) * screenx * SPEED, (current_y - last_y) * screeny * SPEED, absolute=False, duration=0)
            if current_gesture == "Closed_Fist":
                if mouse.is_pressed():
                    mouse.move((current_x - last_x) * screenx * SPEED, (current_y - last_y) * screeny * SPEED, absolute=False, duration=0)
                else:
                    pyautogui.mouseDown()
            if current_gesture != "Closed_Fist" and mouse.is_pressed(): 
                pyautogui.mouseUp()
            last_x, last_y = current_x, current_y
            index += 1
    except IndexError:
        pass

recognizer_options = mediapipe.tasks.vision.GestureRecognizerOptions(
    base_options=mediapipe.tasks.BaseOptions(model_asset_path='gesture_recognizer.task'),
    running_mode=mediapipe.tasks.vision.RunningMode.LIVE_STREAM,
    num_hands=2,
    result_callback=display_result)

recognizer = mediapipe.tasks.vision.GestureRecognizer.create_from_options(recognizer_options)

timer = 0

while True:
    # Main loop
    # get frame 
    ret, frame = camera.read()

    if not ret:
        print("oh dang uhh this frame wasn't captured")

    frame = cv2.flip(frame, 1) # Unflip my horrible camera

    # format image, process

    mp_image = mediapipe.Image(image_format=mediapipe.ImageFormat.SRGB, data=frame)
    recognizer.recognize_async(mp_image, timer)
    
    cv2.imshow("Camera", frame)

    if cv2.waitKey(50) & 0xFF == ord('q'):
        break

    timer += 1

camera.release()
cv2.destroyAllWindows()
