import cv2, mediapipe, mouse, ctypes

camera = cv2.VideoCapture(0)

# get monitor size 
user32 = ctypes.windll.user32
screenx, screeny = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

def display_result(result, output_image, timestamp_ms):
    try:
        current_gesture = result.gestures[0][0].category_name
        # print(result)
        if current_gesture == "Pointing_Up":
            mouse.move(result.hand_landmarks[0][8].x * (screenx), result.hand_landmarks[0][8].y * (screeny), absolute = True, duration = 0)
            print(result.hand_landmarks[0][8].x * (screenx * 2))
        if current_gesture == "Closed_Fist":
            mouse.click()
            # todo: add drag
    except IndexError:
        pass

recognizer_options = mediapipe.tasks.vision.GestureRecognizerOptions(
    base_options=mediapipe.tasks.BaseOptions(model_asset_path='gesture_recognizer.task'),
    running_mode=mediapipe.tasks.vision.RunningMode.LIVE_STREAM,
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
        quit()

    timer += 1

camera.release()
cv2.destroyAllWindows()
